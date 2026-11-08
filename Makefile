THEME_DIR ?= ../oink
HUGO ?= hugo
HUGO_ENV = env -u HUGO_MODULE_REPLACEMENTS -u HUGO_PANICONWARNING GOWORK=off HUGO_MODULE_WORKSPACE=off
.PHONY: serve build data blog-editorial check clean

serve:
	$(HUGO_ENV) $(HUGO) server -D

build:
	$(HUGO_ENV) $(HUGO) --gc --minify --environment production --printPathWarnings --printI18nWarnings

data:
	python3 scripts/build-ledger-assets.py

blog-editorial:
	python3 scripts/apply-blog-editorial.py --write
	python3 scripts/apply-blog-links.py
	python3 scripts/normalize-blog-markdown.py --write
	npx --yes autocorrect-node@2.14.0 --fix content/blog
	python3 scripts/improve-blog-image-alt.py --write
	python3 scripts/refresh-blog-manifest.py

check:
	HUGO="$(HUGO)" ./scripts/check-site.sh

clean:
	rm -rf public resources

.PHONY: dev
dev:
	env -u HUGO_PANICONWARNING GOWORK=off HUGO_MODULE_WORKSPACE=off HUGO_MODULE_REPLACEMENTS='github.com/pgsty/oink -> $(abspath $(THEME_DIR))' $(HUGO) server --bind 127.0.0.1 --renderToMemory
