# Blog editorial system and audit

This document records the editorial pass applied to the 158-article archive
imported from `vonng.com` at commit `c3facf78d7de25d002839afb48d0714891c78d0c`.
It separates deterministic corrections from links that remain uncertain.

## Columns

Every article belongs to exactly one long-lived editorial column. `categories`
stores the canonical ID; localized taxonomy pages provide the public title.

| ID | English | 中文 | Articles |
| --- | --- | --- | ---: |
| `cloud-exit-economics` | Cloud Exit Economics | 云成本与下云 | 18 |
| `failures-postmortems` | Failures & Postmortems | 故障与复盘 | 34 |
| `security-control-risks` | Security, Privacy & Control Risks | 安全、隐私与控制风险 | 19 |
| `cloud-business` | Cloud Business & Industry | 云产业与商业评论 | 20 |
| `cloud-databases` | Cloud Databases | 云数据库 | 15 |
| `self-hosting` | Self-Hosting Playbooks | 自建实践 | 20 |
| `sovereignty-open-ecosystems` | Data Sovereignty & Open Ecosystems | 数据主权与开放生态 | 21 |
| `infrastructure-engineering` | Infrastructure Engineering & Organizations | 基础设施工程与组织 | 11 |

The blog landing page exposes these columns as cards. Article URLs remain
`/blog/<slug>/` and `/zh/blog/<slug>/`.

## Controlled tags

The archive uses 147 canonical tag IDs rather than separate translated values.
Each term has an English and Chinese display page. IDs encode four dimensions:

- entities: `vendor-*`, `org-*`, and `person-*`;
- resources and services: `resource-*`, `service-*`, `tech-*`, and `product-*`;
- themes: `topic-*`;
- article form and tone: `form-*` and `tone-*`.

Each article has 4–8 tags, at least one primary form, no more than three entity
tags, and no more than one tone. `Oracle Cloud` and `Oracle Database`, for
example, are deliberately different terms. The complete reviewed mapping lives
in `data/blog/editorial.yaml`; term names and aliases live in
`data/blog/taxonomy.yaml`.

## Markdown and typography pass

The pass covered 239 localized article pages and 39,259 source lines.

- repaired malformed emphasis, empty links, heading jumps, body-level H1s,
  unlabeled code fences, pasted bullet/number lists, adjacent links, image/text
  collisions, and imported hard-break escapes;
- normalized front matter so every page has `authors`, `summary`, one category,
  canonical tags, and traced `archive_source` metadata;
- ran AutoCorrect 2.14.0 with spellcheck disabled and fenced code excluded;
- verified fenced code, inline code, link destinations, raw URLs, and math were
  unchanged by the automated prose pass;
- replaced 1,012 empty, generic, or filename-only image alternatives with
  article/section-aware descriptions;
- removed the stale `content/blog/rds/rds.en.md` page resource while preserving
  its import digest in the manifest.

`scripts/check-blog-markdown.py` enforces the structural contract and
`scripts/check-blog-editorial.rb` enforces classification parity.

## Link audit

The dated external audit examined 648 non-WeChat HTTP targets on 2026-08-29.

| Classification | Count | Treatment |
| --- | ---: | --- |
| Live / valid redirect | 488 | Kept |
| GET-confirmed 404 | 34 | Corrected, internalized, unlinked, or replaced |
| Blocked (`403` / `451`) | 8 | Kept as uncertain |
| Timeout | 115 | Kept as uncertain |
| Connection / protocol error | 3 | Kept as uncertain |

Only a GET-confirmed `404`/`410` is considered hard failure. Authentication,
anti-bot responses, rate limits, TLS/network errors, and timeouts are not
silently removed. The original probe evidence is stored in
`data/blog/external-link-audit.json`; the build-time snapshot check ensures no
confirmed-dead URL remains.

The WeChat audit normalized 414 URL strings into article entities using the
local 567-article public-account archive and historical audit data. Of 732
high-confidence occurrences, 649 cross-article references now point to the
local blog. Eighty-three self-source links remain external intentionally as
publication provenance. Ambiguous and third-party WeChat links were retained.

Deterministic mappings and overrides are recorded in:

- `data/blog/wechat-map.json`;
- `data/blog/link-fixes.json`;
- `data/blog/link-overrides.json`.

## Repeatable workflow

```bash
python3 scripts/apply-blog-editorial.py --write
python3 scripts/apply-blog-links.py
python3 scripts/normalize-blog-markdown.py --write
npx --yes autocorrect-node@2.14.0 --fix content/blog
python3 scripts/improve-blog-image-alt.py --write
python3 scripts/refresh-blog-manifest.py
make check
```

The network audit is a dated observation, not a permanent truth. Recheck it
before future publication or whenever a cited provider reorganizes its site.

## Publication review, 2026-11-08

The imported Dify setup examples contained a literal signing/encryption secret
in both languages. The examples now require a newly generated secret. The
manifest retains the original import hashes and records the edited files.
The external-link audit above remains a 2026-08-29 snapshot; passing the local
checks does not establish that every external URL is currently reachable.

The archive retains image references to `pigsty.io`, `pigsty.cc`, and
`asciinema.org`, plus an HTTPS video embed from `player.bilibili.com`. These
are external runtime dependencies. Output security review permits these
existing third-party embeds while checking URL schemes and inline handlers.
