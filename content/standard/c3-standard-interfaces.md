---
title: C3 · Standard interfaces
linkTitle: C3 · Standard interfaces
description: Test whether core data-plane operations can be reproduced through public, implementable interfaces.
weight: 30
---

> [!CAUTION]
> Draft criterion, version 0.1. No provider result is implied by this page.

## Definition {#definition}

A service passes C3 when the core operations needed to continue the workload
are exposed through documented interfaces that independent implementations can
reasonably reproduce. “Standard” means open enough to implement and test, not
merely widely used under one vendor's control.

## How to verify {#verify}

List every operation on the critical path, map it to a published specification,
exercise the same workload against an independent implementation or adapter,
and record incompatible semantics, undocumented extensions, and control-plane
dependencies.

## Worked example {#example}

An S3-compatible data plane may reduce migration work, but compatibility is a
test result, not a label. Versioning, multipart upload, retention, checksums,
events, and identity semantics must be tested when the workload uses them.

## Boundaries and objections {#boundaries}

- A proprietary control plane can coexist with a portable data plane; report both.
- An adapter counts only when it is maintained, testable, and does not discard required semantics.
- Commodity protocols do not guarantee operational portability; configuration and identity may still lock the workload in.

