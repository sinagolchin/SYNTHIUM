# PROPOSALS (waiting for Sina; nothing here is applied until Sina says yes)

- P1 (raised 2026-11-10): one coding vocabulary across registers. Still waiting for Sina. Its full text was not found in this Drive folder on 2026-11-12; ask the 10:41 run's memory or the old mirror for it.

## P2 (2026-11-12): make party_power_proxy directional in T1_POINTS.csv
**Why:** the Greene rival (G1, DRAFT in docs/AXIOM_CANDIDATES.md) can only be tested if we know who appealed. The current values (individual_v_individual, individual_v_organization, corporate_v_corporate, and state-related values) do not say which side is the appellant or whether either side was pro se.
**Proposal:** add three columns, appellant_type, appellee_type (individual / organization / state) and pro_se (none / appellant / appellee / both), and back-fill the existing 83 rows from the case notes. Keep party_power_proxy as is for compatibility.
**Cost:** one pass over existing rows; no change to any other rule.
