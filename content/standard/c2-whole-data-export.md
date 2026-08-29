---
title: C2 · Whole-data export
linkTitle: C2 · Whole-data export
description: Test whether all customer-owned data and required metadata can be exported in usable form and bounded time.
weight: 20
---

> [!CAUTION]
> Draft criterion, version 0.1. No provider result is implied by this page.

## Definition {#definition}

A service passes C2 when the customer can export all customer-owned data plus
the metadata required to use it elsewhere, in documented formats and within a
bounded duration. A dashboard download of only the current visible state is not
a whole-data export when history, schema, permissions, versions, or logs are
required to reconstruct the service.

## How to verify {#verify}

Inventory primary data, schema, identities and ACLs, versions, audit logs,
configuration, keys, and derived indexes. Run an export, restore it into an
independent environment, verify counts and checksums, and record elapsed time,
rate limits, downtime, and missing semantics.

## Worked example {#example}

An object store with every object copied but without version history or legal
hold metadata is reported as a partial export when those features are in use.
A database dump that restores rows but loses roles, extensions, or scheduled
jobs is likewise partial, not complete.

## Boundaries and objections {#boundaries}

- Provider-owned telemetry and proprietary internal models are outside scope unless contracted as customer data.
- A documented transformation is acceptable when the target format preserves required meaning.
- Export existence is insufficient: throughput and restore verification are part of the test.

