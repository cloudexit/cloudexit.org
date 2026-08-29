# Methodology

Self-hosted monthly cost is modeled as hardware amortization plus discrete
facility, fabric, base-transit, spare, and replication steps. Cloud comparisons
use the 2026-08-22 public-price snapshot.

Key conventions:

- Compute uses stable business vCPU demand and reports active plus spare servers.
- Object storage distinguishes four-node lower bound, eight-node production
  baseline, dual-site, three-site, and 20-rack Vault topologies.
- Cash and 8% economic-annuity costs remain separate.
- First crossing means one fill interval becomes cheaper; durable crossing means
  later capacity steps no longer reverse the result.
- Labor, software licensing, migration, compliance, and business-loss risk are
  not embedded as universal numbers.

