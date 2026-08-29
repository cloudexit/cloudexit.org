---
title: Data first
linkTitle: Data first
description: Establish independent custody, export, verification, and restore before moving application traffic.
weight: 20
---

Data is usually the slowest, heaviest, and least replaceable part of an exit.
Separate its custody from the application cutover.

## Sequence {#sequence}

1. Define ownership, retention, recovery point, and deletion requirements.
2. Maintain a documented export or replica outside the original control plane.
3. Verify completeness with checksums and semantic tests.
4. Rehearse restore on an independent implementation.
5. Measure lag, throughput, cost, and the largest bounded recovery window.
6. Only then design application replay or cutover.

“Data first” does not mean copying bytes while losing roles, schemas, versions,
policies, keys, or audit context. C2 defines the completeness test.

