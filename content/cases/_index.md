---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: Cloud Exit Cases
linkTitle: Cases
description: Comparable accounts of successful, partial, abandoned, and reversed cloud exits.
weight: 40
type: docs
icon: fa-solid fa-route
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
cascade:
  theme_color: '#355d34'
  theme_color_dark: '#9bd096'
  type: docs
  navbar_autohide: false
  footer_style: fat
  comments: false
  feedback: false
---
Cloud exit is not a religious ideology; it is a pragmatic engineering trade-off grounded in economics and operational capabilities.

Public discourse often oscillates between two extreme caricatures: the sensationalist promise that "anyone can self-host and immediately save millions," or the vendor scare tactic that "bare metal will consume all your engineering headcount." Production engineering is far more nuanced.

The **Case Library** provides a common review template for successful, partial, abandoned, and reversed migrations. Completed case assessments have not yet been published; the essay archive preserves source commentary for future review.

## The Six Essential Questions {#six}

Every rigorous postmortem must answer these six fundamental dimensions:

| Dimension | Focus Area | Observable Facts |
| :--- | :--- | :--- |
| **1. What Moved?** | Migration Scope | Database, object storage, Kubernetes clusters, or stateful data? Which layers decoupled first? |
| **2. What Stayed?** | Deliberate Retention | Which managed primitives (e.g. edge CDN, Anycast DNS, IAM) were retained, and why? |
| **3. What Did It Cost?** | Total TCO | Server procurement, colocation power/space, cross-connects, labor, and parallel transition burn. |
| **4. How Long Did It Take?** | Realistic Timelines | Time elapsed from initial RFC to proof-of-concept, canary cutover, and final payback break-even. |
| **5. Where Did It Stumble?** | Friction & Failures | Unexpected hardware bottlenecks, automation gaps, team skill deficits, and scoped-down goals. |
| **6. What Would Change?** | Team Hindsight | The engineering team's unfiltered retrospective on what they would do differently today. |
{.wide .expand}

## Evidence Labels & Calibration Candidates {#labels}

Every case study explicitly labels its verification rigor: **First-Party Engineering Report**, **Audited Financial Statements**, **Reproducible Cost Models**, or **Editorial Architecture Analysis**. Modeled projections are never conflated with realized accounting savings.

Initial calibration candidates are 37signals, Ahrefs, Tantan, and publicly documented partial or reversed exits. Sources, cost definitions, and timelines must be reconciled before any candidate becomes a completed case. Reported savings and hypothetical cloud costs will remain distinct.

