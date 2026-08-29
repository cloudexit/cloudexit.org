---
title: The exit drill
linkTitle: Exit drill
description: Restore a complete critical dataset somewhere else, verify it, time it, and record every dependency.
weight: 10
---

The exit drill is the smallest useful measure of cloud exit capability. It does
not change production traffic and should not require a migration project.

## Objective {#objective}

Produce a verified, usable copy of one critical dataset in an environment that
does not depend on the original service's control plane. Record elapsed time,
human effort, cost, missing semantics, and every dependency that prevented a
clean restore.

## One-afternoon version {#afternoon}

1. **Choose one dataset.** Prefer important, bounded, and already backed up.
2. **Declare success.** Counts, checksums, schema, permissions, recovery point, and one application query.
3. **Choose elsewhere.** Another provider, a local host, colocation, or an independent open implementation.
4. **Start the clock.** Include export preparation, transfer, restore, and verification.
5. **Do not improvise silently.** Log missing credentials, undocumented steps, rate limits, and manual support.
6. **Verify independently.** Use checksums plus semantic checks; “the command exited zero” is insufficient.
7. **Record the number.** Report elapsed time, hands-on time, data age, total cost, and blockers.
8. **Clean up safely.** Confirm retention and deletion requirements before removing the drill copy.

## Scorecard {#scorecard}

| Field | Record |
| --- | --- |
| Dataset and size | What was actually included |
| Recovery point | Age of the restored data |
| Elapsed time | Start to verified usable copy |
| Hands-on time | Human effort, by role |
| Direct cost | Export, transfer, compute, storage, support |
| Missing semantics | Roles, versions, policies, jobs, logs, keys |
| Blocking dependencies | Provider-only services, identities, approvals, tools |
| Repeatability | Scripted, documented, or one-off |

## Safety boundary {#safety}

Use non-production credentials and an isolated target. Do not weaken retention,
encryption, privacy, or access controls to make the drill pass. A failed drill
is a useful result; it identifies the next capability to build.

