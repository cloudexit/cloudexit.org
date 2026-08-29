---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: Cloud Exit Playbook
linkTitle: Playbook
description: Reversible, staged practices for measuring and improving exit capability without beginning with a migration.
weight: 50
type: docs
icon: fa-solid fa-compass
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
cascade:
  theme_color: '#4d3a78'
  theme_color_dark: '#c0abe9'
  type: docs
  navbar_autohide: false
  footer_style: slim
  comments: false
  feedback: false
---

The playbook supports an operational conclusion: **cloud exit is a staged,
reversible engineering capability, not a leap into the dark.** Begin by
measuring recovery somewhere else; decide whether to migrate only after the
constraints are visible.

## Five practices {#practices}

1. [Exit drill](/playbook/exit-drill/) — restore a complete critical dataset elsewhere and time it.
2. [Data first](/playbook/data-first/) — separate custody and recoverability from application migration.
3. [Inventory](/playbook/inventory/) — map dependencies, semantics, contracts, and owners.
4. [Staging](/playbook/staging/) — move through replay, shadow, partial traffic, and reversible cutover.
5. [Negotiation](/playbook/negotiation/) — turn measured exit options into better contract terms.

The call to action is the first drill. It is useful even when the final decision
is to stay with the current provider.

