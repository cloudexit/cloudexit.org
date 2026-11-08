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
  footer_style: fat
  comments: false
  feedback: false
---
Exit capability is not a reckless leap off a cliff; it is an escape parachute you pack carefully and test regularly.

You do not need to greenlight a massive architectural overhaul, nor do you need to purchase a fleet of servers upfront. **Next Monday afternoon, run a four-hour exit drill**:
Spin up a single clean machine outside your primary cloud, restore your core database from cold backup, time the operation to the second, and log every proprietary cloud API that throws an error.

The time it takes to restore is your real recovery capability; the point where it crashes is your actual vendor lock-in.

## Five Practical Disciplines {#practices}

{{< cards >}}
  {{< card title="1 · Exit Drill" link="/playbook/exit-drill/" icon="fa-solid fa-stopwatch" badge="First Step" >}}
Restore an authoritative snapshot on neutral compute, measure actual RTO, and document breaking proprietary dependencies.
  {{< /card >}}
  {{< card title="2 · Data First" link="/playbook/data-first/" icon="fa-solid fa-database" badge="Decoupling" >}}
Establish independent custody and external recovery pipelines for databases before touching stateless application workloads.
  {{< /card >}}
  {{< card title="3 · Dependency Inventory" link="/playbook/inventory/" icon="fa-solid fa-list-check" badge="Auditing" >}}
Map proprietary message brokers, custom authorization layers, hosted filers, and operational runbooks against open alternatives.
  {{< /card >}}
  {{< card title="4 · Staged Cutover" link="/playbook/staging/" icon="fa-solid fa-layer-group" badge="Safe Rollout" >}}
Plan shadow traffic or staged cutovers, verify consistency, and measure rollback time before touching production.
  {{< /card >}}
  {{< card title="5 · Contract Negotiation" link="/playbook/negotiation/" icon="fa-solid fa-handshake" badge="Commercials" >}}
Translate verified recovery drills into credible commercial leverage to eliminate punitive renewal terms and extract discounts.
  {{< /card >}}
{{< /cards >}}

> [!TIP]
> Even if your organization ultimately decides to remain on public cloud, this drill is profoundly valuable: **staying is only a genuine strategic choice if leaving remains an operational reality.**

