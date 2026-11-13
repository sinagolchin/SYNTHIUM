# Campaign A progress (A0 clean test: evidence basis coded from FACTS ONLY, committed before reveal)

Store: this folder holds blindlog.jsonl (hash-chained) and sealed/ (full texts). To continue in a new session,
download both into a local BLIND_HOME, run `python3 -m synthium.blind.protocol verify`, then append.

| case id | source | grade | committed | actual | notch hit |
|---|---|---|---|---|---|
| ca-wagonhound | CL op 11448351 (Wyo.) | blind | MODIFIED | MODIFIED | yes |
| ca-pa-ins-fedex | CL op 11433545 (8th Cir.) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |
| ca-brock-tompkins-r2 | CL op 11436984 (Mont.) | uncertain_exposure | REVERSED | MODIFIED | no |
| ca-canter-canter-r2 | CL op 11524635 (Utah App.) | uncertain_exposure | MODIFIED | MODIFIED | yes |
| ca-koch-sargent | CL op 11524241 (Neb.) | uncertain_exposure | REVERSED | REVERSED | yes |
| ca-cheung-pena | CL op 11523520 (Idaho) | blind | REVERSED | CLEAN_AFFIRM | no |
| ca-berkshire | CL op 11491792 (Neb.) | blind | MODIFIED | CLEAN_AFFIRM | no |
| ca-colton-overlook | CL op 11525565 (Idaho) | blind | CLEAN_AFFIRM | REVERSED | no |
| ca-armitage-degroot | CL op 11515307 (Idaho) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |
| ca-estate-todd | CL op 11518004 (Neb.) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |
| ca-bear-bear | CL op 11515144 (Idaho) | blind | REVERSED | CLEAN_AFFIRM | no |
| ca-ellman-charron | CL op 11507686 (Idaho) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |
| ca-miracle-hills-ali | CL op 11518005 (Neb.) | blind | REVERSED | REVERSED | yes |
| ca-reilly-sullivan | CL op 11510763 (Wyo.) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |
| ca-hinckley-uwyo | CL op 11520336 (Wyo.) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |
| ca-yc-properties-connolly | CL op 11522243 (Mont.) | blind | REVERSED | REVERSED | yes |
| ca-christofferson | CL op 11522250 (Mont.) | uncertain_exposure | MODIFIED | MODIFIED | yes |
| ca-estate-bradford | CL op 11514123 (Mont.) | blind | REVERSED | REVERSED | yes |
| ca-copper-city-allen | CL op 11454075 (Mont.) | blind | REVERSED | REVERSED | yes |
| ca-kearns | CL op 11514121 (Mont.) | blind | MODIFIED | MODIFIED | yes |

Logged: 14 of ~20 (notch 9/14; layer 10/10 where coded). Fact points by evidence basis so far (Campaign A only):
- CREDIBILITY-based findings challenged: 9, disturbed 0 (Reilly sequestration-violation credibility; Wagonhound Parsons Creek and dust; FedEx breach and Sonia credibility; Canter expenses and 2LMD; Berkshire capital account and unreported transfers).
- DOCUMENTARY-based: 7, disturbed 1 (Brock deeds/severance). Held: FedEx invoice, FedEx subrogation, Wagonhound appraisal, Canter tax-return argument, Berkshire rent (lease/ledger), Berkshire ATM ledger.
- RECORD-ABSENCE (no evidence at all): 3, disturbed 3 (Wagonhound conditions 4 and 6; Colton road location, where the court used absence of evidence to shift the movant's burden).
No credibility finding overturned yet. A0 falsifier not found.

Open / not usable:
- ca-krasko-konkos-r2 (CL op 11525525, Conn. App.): VOIDED 2026-11-11 13:41 run before any commit. Its "Part I" is the analysis of the first appellate claim, not background, so facts scope would expose reasoning. Not usable blind.
- ca-curella-behny (CL op 11517056, Ind. App.): sealed, no_cut (no facts heading); fails closed. Do not code blind.
- ca-krasko-konkos, ca-canter-canter, ca-brock-tompkins: first requests failed intake because the courier transcript held rate-limit error results (non-JSON) and ingest fails closed. Re-requested as -r2. Run couriers one at a time to avoid this.

Selection: CourtListener keyword search with fields limited to caseName/court/date/ids (no snippets), so prior exposure = case name only.

Note 2026-11-11 13:41 run: all three new cases were Nebraska/Idaho apex courts; two of three were clean affirmances I predicted would move (both were direct appeals to the apex court; a lean toward predicting movement is a coder bias to watch). Koch grade is uncertain_exposure only because the tool redacted a front-loaded outcome sentence.

Note 2026-11-11 16:41 run: four more Idaho/Nebraska apex cases, all blind. After the 13:41 note I leaned the other way and missed Colton (a reversal). Bear was a split: the court rejected the trial court's legal theory (subject-matter jurisdiction) but affirmed on full faith and credit, so the law was corrected without the disposition moving; the notch scheme codes that as CLEAN_AFFIRM. Flag for P1. Colton uses party_power_proxy value individual_v_organization (new value, needed for an individual against an HOA/developer).

Note 2026-11-11 19:41 run: three more apex cases, all blind, all notch hits. Ellman (Idaho) affirmed on subject matter jurisdiction while the court declared its own precedent (Roe, permissive intervention) superseded by later CPA amendments: law moved, disposition did not (second case like Bear; flag for P1). Miracle Hills (Neb.) was a hit for the wrong reason: I predicted reversal on homestead protection; the court rejected that and vacated on plain error in the decree's scope (whole residence vs debtor's half) and on leaving the seller to the creditor. New standard_of_review value plain_error used in T1_POINTS (mention to Sina). Reilly (Wyo.) custody, credibility and weighing all affirmed.


## Campaign A complete (2026-11-12 10:41 run): 20 of 20 logged

- Notch score: 15/20 (75%). Always-affirm baseline on the same 20 cases: 9/20 (45%). Blind grade only (16 cases): notch 12/16, always-affirm 9/16. Uncertain_exposure (4): notch 3/4.
- Layer: 16/16 where coded.
- Fact points by evidence basis, Campaign A (adds today's 6): credibility-based findings challenged 10, disturbed 0 (adds Kearns account-change credibility). Documentary-based 8, disturbed 1 (adds Christofferson "delay" finding: contradicted by the record but held harmless, so not disturbed in effect; flag for P1 how to code a wrong-but-harmless finding). Record-absence 3, disturbed 3. A0 falsifier still not found.
- Caveat for reading the 75%: in today's six, the facts sections were written by the deciding court and several carried directional wording ("nevertheless", "overlooked", emphasis added to the lower court's rule). Facts scope still leaks the court's framing. Worth discussing before public claims.
- Not usable: ca-bauer-scott-myers (CL op 11510679): REQUEST logged 2026-11-12, courier returned FAILED (CourtListener has no text for this opinion). Nothing sealed; id retired.
- Today's six were all apex courts (5 Montana, 1 Wyoming); Montana's 2026 MT opinions have clean FACTUAL AND PROCEDURAL BACKGROUND / STANDARD OF REVIEW headings and work well blind.
- Next: keep coding blind (as Campaign A's open phase), Greene rival paragraph draft once (ROADMAP step after Campaign A).

## Open phase after Campaign A (2026-11-12 13:41 run)

Same protocol, same log (entries 135 onward). Chain verified intact before logging (135 entries, last = ca-kearns RECORD from the 10:41 run; no foreign entries).

| case | source | grade | predicted | actual | notch hit |
|---|---|---|---|---|---|
| ca-victory-ins-auditor | CL op 11526918 (Mont. 2026 MT 269) | blind | MODIFIED | MODIFIED | yes (layer miss) |
| ca-gca-state | CL op 11500396 (Mont. 2026 MT 243) | blind | REVERSED | CLEAN_AFFIRM | no |
| ca-yellowstone-mtdeq | CL op 11500389 (Mont. 2026 MT 242) | blind | CLEAN_AFFIRM | CLEAN_AFFIRM | yes |

Open-phase running score: notch 2/3. Always-affirm on the same 3: 2/3.
- ca-ellingson-state and ca-ellingson-state-r2 (CL op 11480718): REQUEST logged twice, courier returned DONE both times but the result was not JSON, so ingest refused to seal (fail closed). Nothing sealed; both ids retired. Don't retry this opinion via courier.
- Yellowstone County affirmed "on narrower grounds": third case (after Bear, Ellman) where the law was corrected but the disposition held. P1 flag.
- New party_power_proxy values: organization_v_government, government_v_government (P2 flag).
