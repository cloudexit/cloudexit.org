---
title: Staged migration
linkTitle: Staging
description: Move through replay, shadow, partial traffic, bounded cutover, and rollback with explicit gates.
weight: 40
---

Do not make the first real test a full production cutover.

## Gates {#gates}

1. **Offline restore:** data and configuration rebuild successfully elsewhere.
2. **Replay:** recorded or synthetic workload verifies semantics and performance.
3. **Shadow:** target receives a copy of live changes without serving users.
4. **Partial traffic:** a bounded cohort uses the target with measurable rollback.
5. **Cutover:** recovery point, freeze window, decision owner, and abort threshold are explicit.
6. **Stabilize:** run both observability and recovery procedures for the agreed window.
7. **Decommission:** remove old dependencies only after retention, rollback, and contract gates close.

Every gate has success evidence, an owner, an abort threshold, and a tested path
back. A hybrid end state can be a deliberate architecture, not a failed exit.

