#!/usr/bin/env bash
set -euo pipefail

site_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$site_root"

unset HUGO_MODULE_REPLACEMENTS HUGO_PANICONWARNING
export GOWORK=off HUGO_MODULE_WORKSPACE=off
hugo="${HUGO:-hugo}"

command -v "$hugo" >/dev/null
command -v go >/dev/null
command -v python3 >/dev/null
command -v ruby >/dev/null
command -v rg >/dev/null

hugo_version="$("$hugo" version)"
if [[ ! "$hugo_version" =~ ^hugo\ v0\.168\.0(-[0-9a-f]+)?\+extended(\+withdeploy)?[[:space:]] ]]; then
  printf 'expected Hugo Extended 0.168.0, got: %s\n' "$hugo_version" >&2
  exit 1
fi
if [[ "$(go env GOVERSION)" != 'go1.27.3' ]]; then
  printf '%s\n' 'expected Go 1.27.3' >&2
  exit 1
fi
printf '%s\n' "$hugo_version" "$(go version)"

ruby scripts/check-home-parity.rb
ruby -rjson -e 'JSON.parse(File.read("schemas/vendor.schema.json")); puts "vendor schema JSON OK"'
python3 scripts/verify-ledger-assets.py
python3 scripts/verify-blog-import.py
ruby scripts/check-blog-editorial.rb
python3 scripts/check-blog-markdown.py
python3 scripts/check-blog-external-snapshot.py

module_graph="$("$hugo" mod graph)"
if ! printf '%s\n' "$module_graph" | rg -q '^[^[:space:]]+ github[.]com/pgsty/oink@v1[.]5[.]1$'; then
  printf '%s\n' 'Oink module is not pinned to v1.5.1' >&2
  exit 1
fi

while IFS= read -r source_page; do
  case "$source_page" in
    content/blog/*|content/authors/*)
      page_name="${source_page##*/}"
      if [[ "$page_name" != "index.md" && "$page_name" != "_index.md" ]]; then
        continue
      fi
      ;;
  esac
  translated_page="${source_page%.md}.zh.md"
  if [[ ! -f "$translated_page" ]]; then
    printf 'missing Chinese pair: %s\n' "$source_page" >&2
    exit 1
  fi
done < <(find content -type f -name '*.md' ! -name '*.zh.md' | sort)

if rg -n '/Users/|/home/' content data layouts static \
  -g '!content/blog/**' -g '!content/authors/**' -g '!data/blog/**' >/dev/null; then
  printf '%s\n' 'absolute local filesystem path found in publishable source' >&2
  exit 1
fi

build_root="$(mktemp -d)"
trap 'rm -rf "$build_root"' EXIT
HUGO_RESOURCEDIR="$build_root/resources" "$hugo" --gc --minify --environment production \
  --printPathWarnings --printI18nWarnings --destination "$build_root/public"

for route in \
  index.html zh/index.html \
  standard/index.html zh/standard/index.html \
  ledger/index.html zh/ledger/index.html \
  evidence/index.html zh/evidence/index.html \
  cases/index.html zh/cases/index.html \
  playbook/exit-drill/index.html zh/playbook/exit-drill/index.html \
  blog/index.html zh/blog/index.html \
  blog/rds/index.html zh/blog/rds/index.html \
  blog/local-ai-inference/index.html zh/blog/local-ai-inference/index.html \
  zh/blog/better-rds-alternative/index.html \
  llms.txt navigation.json; do
  if [[ ! -f "$build_root/public/$route" ]]; then
    printf 'missing generated route: %s\n' "$route" >&2
    exit 1
  fi
done

python3 scripts/check-links.py "$build_root/public"

printf '%s\n' 'site checks OK'
