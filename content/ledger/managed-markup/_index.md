---
title: Managed-service markup
linkTitle: Managed markup
description: Separate resource cost from the value and price of operations supplied by a managed service.
weight: 60
---

> [!NOTE]
> Planned public model. PostgreSQL-compatible managed databases are the first calibration target.

## Split price from value {#split}

The model first estimates equivalent resource cost, then itemizes operations the
managed service supplies: provisioning, patching, backups, failover, monitoring,
support, compliance, control plane, and service risk. The residual price is not
automatically waste; it is the amount that must be justified by delivered value.

## Questions the page must answer {#questions}

- Which responsibilities actually move to the provider, and which remain shared?
- Which features are used, and what would they cost to reproduce at the required coverage?
- What restrictions, missing extensions, or control-plane dependencies reduce value?
- How do commitment, outage remedy, and exit cost change the apparent markup?

Seed essay: [Is a cloud database an intelligence tax?](https://vonng.com/cloud/rds/).
Current model outputs will replace its historical prices while keeping the
original argument and period visible.

