# Cloud Exit

Local skeleton for [cloudexit.org](https://cloudexit.org/), built with Hugo and
[Oink 0.8.0](https://github.com/pgsty/oink/releases/tag/v0.8.0).

> Status: **v0.1 skeleton**. The information architecture, bilingual landing
> page, editorial contracts, and route placeholders exist. The cost ledger now
> ships three versioned data snapshots and detailed compute, block-storage,
> object-storage, and price-history pages. Provider ratings, badges, and
> case-study claims are not published yet.

## Single responsibility

Turn cloud exit from a signed opinion into a verifiable public standard and a
checkable body of evidence.

The site is not a second copy of [vonng.com/cloud](https://vonng.com/cloud/):
the latter is the authored essay archive; this repository is the method,
dataset, registry, and operational handbook that other people can cite or
challenge.

## Argument chain

1. **Standard** — who is charging rent through lock-in?
2. **Ledger** — how large is that rent under explicit assumptions?
3. **Evidence** — what failures and lock-in mechanisms are on record?
4. **Cases** — who has exited, partially exited, or failed to exit?
5. **Playbook** — what can a team do next Monday?

See [`docs/DESIGN.md`](docs/DESIGN.md) for the full site outline and
[`docs/CONTENT-MAP.md`](docs/CONTENT-MAP.md) for the migration map from the
existing research and essay corpus.

## Local preview

```bash
hugo mod get github.com/pgsty/oink@v0.8.0
hugo server -D
```

Production-style validation:

```bash
make check
```

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
