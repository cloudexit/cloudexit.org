#!/usr/bin/env bash
set -euo pipefail

site_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$site_root"

command -v hugo >/dev/null
command -v python3 >/dev/null
command -v ruby >/dev/null

ruby scripts/check-home-parity.rb
ruby -rjson -e 'JSON.parse(File.read("schemas/vendor.schema.json")); puts "vendor schema JSON OK"'
python3 scripts/verify-ledger-assets.py

module_graph="$(hugo mod graph)"
if [[ "$module_graph" != *"github.com/pgsty/oink@v1.5.0"* ]]; then
  printf '%s\n' 'Oink module is not pinned to v1.5.0' >&2
  exit 1
fi

while IFS= read -r source_page; do
  translated_page="${source_page%.md}.zh.md"
  if [[ ! -f "$translated_page" ]]; then
    printf 'missing Chinese pair: %s\n' "$source_page" >&2
    exit 1
  fi
done < <(find content -type f -name '*.md' ! -name '*.zh.md' | sort)

if rg -n '/Users/|/home/' content data layouts static >/dev/null; then
  printf '%s\n' 'absolute local filesystem path found in publishable source' >&2
  exit 1
fi

build_root="$(mktemp -d)"
trap 'rm -rf "$build_root"' EXIT
hugo --gc --minify --destination "$build_root/public"

for route in \
  index.html zh/index.html \
  standard/index.html zh/standard/index.html \
  ledger/index.html zh/ledger/index.html \
  evidence/index.html zh/evidence/index.html \
  cases/index.html zh/cases/index.html \
  playbook/exit-drill/index.html zh/playbook/exit-drill/index.html \
  llms.txt navigation.json; do
  if [[ ! -f "$build_root/public/$route" ]]; then
    printf 'missing generated route: %s\n' "$route" >&2
    exit 1
  fi
done

python3 scripts/check-links.py "$build_root/public"

printf '%s\n' 'site checks OK'
