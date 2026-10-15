THEME_DIR ?= ../oink
.PHONY: serve build data check clean

serve:
	hugo server -D

build:
	hugo --gc --minify

data:
	python3 scripts/build-ledger-assets.py

check:
	./scripts/check-site.sh

clean:
	rm -rf public resources

.PHONY: dev
dev:
	GOWORK=off HUGO_MODULE_WORKSPACE=off HUGO_MODULE_REPLACEMENTS='github.com/pgsty/oink -> $(abspath $(THEME_DIR))' hugo server --bind 127.0.0.1 --renderToMemory
