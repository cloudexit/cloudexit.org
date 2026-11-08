---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: Cloud Exit Standard
linkTitle: Standard
description: Five falsifiable tests for whether a service preserves a customer's practical ability to leave.
weight: 10
type: docs
icon: fa-solid fa-scale-balanced
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
cascade:
  theme_color: '#164b63'
  theme_color_dark: '#78c5e6'
  type: docs
  navbar_autohide: false
  footer_style: fat
  comments: false
  feedback: false
---

Entering the cloud is frictionless by design; leaving is where artificial barriers emerge. The difficulty of cloud exit rarely stems from application code, but from proprietary APIs, punitive bandwidth egress tolls, and predatory contract locks.

The **Cloud Exit Standard** is an open, falsifiable engineering framework designed to audit infrastructure sovereignty. We ignore vendor marketing and focus on a single operational test: **if your organization chooses to leave tomorrow, does this service preserve your practical ability to escape?**

## Five Core Criteria {#criteria}

Every production cloud service must withstand these five baseline engineering checks:

| Criterion | Dimension | Core Verification Question | Evidence to Collect |
| :--- | :--- | :--- | :--- |
| **[C1 · No Exit Tolls](/standard/c1-no-exit-toll/)** | Economics | Does migrating data out trigger punitive egress or extraction fees? | Total export cost, ordinary delivery cost, waivers and eligibility; thresholds await calibration |
| **[C2 · Whole-Data Export](/standard/c2-whole-data-export/)** | Data Assets | Can the entire usable dataset be exported within bounded time? | Data and required metadata, restore verification, elapsed time and rate limits |
| **[C3 · Standard Interfaces](/standard/c3-standard-interfaces/)** | Architecture | Can core storage and compute operations be run via open protocols? | Published specifications, independent implementations and required semantic differences |
| **[C4 · No Commitment Lock](/standard/c4-no-commitment-lock/)** | Contracts | Do volume commitments turn into legal indentures with exit penalties? | Term, utilization, unused obligations, refunds, transfers and cancellation rules |
| **[C5 · Accountable Downtime](/standard/c5-accountable-downtime/)** | Reliability | Are major outage timelines, RCAs, and financial penalties auditable? | Incident timeline, impact, explanation, corrective action and promised contractual remedy |
{.wide .expand}

Every criterion follows the exact same engineering structure: **Definition → Verification Command → Worked Example → Boundaries & Objections**. Scored results apply only to specified products, regions, tiers, and review dates—never an immutable brand verdict.

## What This Standard Is Not {#not}

- **Not an anti-cloud crusade**: Public cloud remains unmatched for early-stage velocity and high-variance spikes. We challenge synthetic extraction barriers, not compute itself.
- **Not a sales ranking or security badge**: We do not evaluate feature depth or commercial footprint.
- **Not judged by vendor brand power**: Big cloud or challenger, every provider is evaluated strictly by reproducible technical behavior and public ledgers.

The [method](/standard/method/) defines evidence, review, expiry, and appeal. The [registry](/standard/registry/) is intentionally empty until an assessment clears that process; no provider ratings have been published.
