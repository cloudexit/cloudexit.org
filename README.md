# Cloud Exit

Local skeleton for [cloudexit.org](https://cloudexit.org/), built with Hugo and
[Oink 1.6.0](https://github.com/pgsty/oink/releases/tag/v1.6.0).

> Status: **v0.1 evidence site with essay archive**. The information
> architecture, bilingual landing page, editorial contracts, and route
> placeholders exist. The cost ledger ships three versioned data snapshots and
> detailed compute, block-storage, object-storage, and price-history pages. The
> blog contains a traced snapshot of the existing essay corpus. Provider
> ratings, badges, and case-study claims are not published yet.

## Single responsibility

Turn cloud exit from a signed opinion into a verifiable public standard and a
checkable body of evidence.

The site's evidence sections remain distinct from authored commentary. The
method, datasets, registry, and operational handbook are assets other people
can cite or challenge; `/blog/` is an explicitly labeled archive of the full
[vonng.com Cloud column](https://vonng.com/cloud/) plus selected essays on data
sovereignty and self-hosting.

## Argument chain

1. **Standard** — who is charging rent through lock-in?
2. **Ledger** — how large is that rent under explicit assumptions?
3. **Evidence** — what failures and lock-in mechanisms are on record?
4. **Cases** — who has exited, partially exited, or failed to exit?
5. **Playbook** — what can a team do next Monday?

See [`docs/DESIGN.md`](docs/DESIGN.md) for the full site outline and
[`docs/CONTENT-MAP.md`](docs/CONTENT-MAP.md) for the migration map from the
existing research and essay corpus.

The taxonomy, formatting rules, internal-link recovery, and dated dead-link
results are documented in [`docs/BLOG-EDITORIAL.md`](docs/BLOG-EDITORIAL.md).

The blog snapshot is reproducible from a local `vonng.com` checkout with
`scripts/import-vonng-blog.py`. `data/blog/imports.json` records the source
commit, selection reason, language coverage, file inventory, byte counts, and
SHA-256 digest of every copied file. `make check` verifies that inventory.

## Local preview

Use Hugo and the Go version declared in `go.mod` (OINK `v1.6.0`, plain CSS).
Run `make dev` to preview against a sibling theme checkout and `make check-local`
to validate it; set `THEME_DIR` to select another checkout.

```bash
make serve
```

Production-style validation:

```bash
make check
```

`serve`, `build`, and `check` disable both workspaces and local theme
replacements. `check` reports the toolchain, verifies the published theme pin,
and builds to a temporary directory outside the repository.

The generated static site is written to `public/`. Local build success is not
deployment, DNS, or production-rendering proof.

Ledger data releases are rebuilt from the sibling `../cloud/research/`
workspace with `scripts/build-ledger-assets.py`; `make check` verifies their
checksums and headline values.

## Publication gates

- Every numeric claim names its source, collection date, currency, unit, and
  applicability boundary.
- Every provider result carries a review date and expires rather than silently
  remaining current.
- Every case distinguishes reported facts, modeled values, and editorial
  inference.
- Conflicts of interest are disclosed on the home page and repeated wherever a
  named commercial tool could benefit.
- English is the canonical public standard; Chinese is maintained in parity for
  the standard, method, registry, and core playbook.

Preview screenshots and one-off design helpers stay local and are ignored.
Article images and author portraits are source assets with hashes recorded in
`data/blog/imports.json`; they are part of the published archive.
