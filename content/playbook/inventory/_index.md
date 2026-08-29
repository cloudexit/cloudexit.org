---
title: Dependency inventory
linkTitle: Inventory
description: Map data, APIs, identities, control planes, contracts, people, and recovery ownership before planning a move.
weight: 30
---

An exit plan is only as complete as its dependency map.

## Inventory layers {#layers}

- **Data:** stores, size, growth, versions, retention, backup, keys, owners.
- **Interfaces:** protocols, SDK calls, provider extensions, quotas, events.
- **Identity:** users, roles, policies, federation, secrets, break-glass access.
- **Control plane:** provisioning, deployment, observability, DNS, certificates, billing.
- **Operations:** on-call, runbooks, support paths, recovery objectives, drills.
- **Commercial:** contracts, credits, commitments, notice periods, termination, licenses.
- **People:** accountable owner, domain expert, approver, and replacement skill.

Mark each dependency **portable**, **adaptable**, **replaceable**, **retained**, or
**unknown**. Unknowns are the first work queue, not a reason to invent certainty.

