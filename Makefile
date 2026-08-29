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
