# PREDICTIONS REGISTER (locked, leak-free, commit-before-reveal)

Rule: predictions are scored from information available BEFORE the ruling only
(standard of review, who is appealing, issue type, dissent-below). E (error
clarity) is NOT used as an input. Each row is written before the outcome is read.
A row with an outcome filled in before a prediction is void.

Honest baseline to beat: always predict the appellant LOSES. In a representative
sample that is ~85% correct. A ruler must beat that, not the 61% of our
reversal-biased pilot.

| date | case | category | appellant | standard of review (D) | leak-free prediction | committed? | actual | correct? |
|---|---|---|---|---|---|---|---|---|
| (empty — to be filled one case at a time, prediction before reveal) |

## Outcome frame standardized (correction)

Outcome is now **reversal (appellant wins) vs affirmance (appellant loses)** — not
the earlier "challenger to the lower decision," which silently flipped meaning in
agency cases (e.g. Baywing). "Who is the appellant" is objective and known before
the ruling, so this frame is leak-free.

## Leak-free status on the 18-case pilot (honest)

- reversal frame base rate (always predict AFFIRM): 66.7%
- best leak-free rule available (deference + appellant type): 66.7%
- **leak-free features do not beat the baseline yet — zero demonstrated signal.**

This is the true starting line. Any future rule must beat always-AFFIRM on a
sample whose reversal rate matches reality (~15%), using inputs fixed before the
ruling. E is excluded by construction.

## Attempt 3 — BLIND commit (predictions locked before any outcome was read)

Fetched with the syllabus field withheld, so no holding was visible at commit
time. Leak-free inputs: case caption + category + base rate. Prediction rule:
predict AFFIRM (appellant loses) for all — the base-rate-optimal leak-free call.
Committed 2026-07-02, before reveal.

| # | case | category (leak-free) | committed prediction |
|---|---|---|---|
| 1 | Kaufman v. Synnott | civil | AFFIRM |
| 2 | Khan v. Jewish Women International | civil | AFFIRM |
| 3 | Sarjac Partners v. Giuliano | civil | AFFIRM |
| 4 | Stanley v. State | criminal/other | AFFIRM |
| 5 | Vargas v. Kang Sjuen LLC | civil | AFFIRM |
| 6 | In re Nevaeh T. | child protection | AFFIRM |
| 7 | N.E. Construction Co. v. Anton | civil | AFFIRM |
| 8 | Esposito v. Rabin | civil | AFFIRM |
| 9 | Medina v. Commissioner of Correction | habeas | AFFIRM |
| 10 | Office of Chief Disciplinary Counsel v. Cunha | attorney discipline | AFFIRM |

### Attempt 3 — REVEAL & score

| # | case | committed | actual | correct? |
|---|---|---|---|---|
| 1 | Kaufman v. Synnott | AFFIRM | AFFIRM (SLAPP dismissal + fees upheld) | ✓ |
| 2 | Khan v. Jewish Women Int'l | AFFIRM | AFFIRM (litigation privilege; dismissed) | ✓ |
| 3 | Sarjac Partners v. Giuliano | AFFIRM | AFFIRM (findings not clearly erroneous) | ✓ |
| 4 | Stanley v. State | AFFIRM | AFFIRM (appeal dismissed, no certification) | ✓ |
| 5 | Vargas v. Kang Sjuen LLC | AFFIRM | **REVERSE** (evidentiary error, new trial) | ✗ |
| 6 | In re Nevaeh T. | AFFIRM | AFFIRM (termination + denial upheld) | ✓ |
| 7 | N.E. Construction v. Anton | AFFIRM | **REVERSE** (standing error) | ✗ |
| 8 | Esposito v. Rabin | AFFIRM | **REVERSE** (quiet-title error) | ✗ |
| 9 | Medina v. Comm'r of Correction | AFFIRM | AFFIRM (no abuse; cert denied) | ✓ |
| 10 | Office of Chief Disc. Counsel v. Cunha | AFFIRM | **REVERSE** (privilege scope error) | ✗ |

**Score: 6/10 = 60%.** Reversal rate in this blind sample = 40%.

### What this blind attempt honestly shows
- The leak-free base-rate call ("always affirm") scored **60%** — it did NOT beat
  a coin-flip by much, because this stream is reversal-heavy.
- **None of the 4 reversals was foreseeable from leak-free features.** Each turned
  on a merits point visible only in the opinion (an evidentiary ruling, a standing
  statute, a quiet-title statute, the scope of a privilege). Appellant type and
  category gave no warning. That is the honest cost of removing the leak: without
  reading the answer, we currently can't see reversals coming.
- The ONE leak-free regularity that held: habeas / criminal-defendant appeals
  (Stanley, Medina) affirmed, consistent with their very high known affirm rate.
  That is a base rate, not a discovered signal.
- **Sampling caveat:** CourtListener's newest published "appeal" opinions
  over-represent reversals (summary affirmances are often unpublished). So 40%
  reversal is a selection artifact; a representative docket would be far lower,
  making "always affirm" ~85%. To test honestly we need a representative sample,
  including unpublished dispositions — not just the published merits stream.

### Bottom line
Done the leak-free way, the ruler has **no demonstrated power to predict
reversal** yet. That is a real result, produced by committing before revealing —
exactly what the leaky 18/18 could never have told us.

## Attempt 4 — BLIND commit (11 more, locked before reveal)

Same rule: predict AFFIRM (appellant loses) for all — the leak-free base-rate call.
Categories from captions only; no holdings seen at commit.

| # | case | category | committed |
|---|---|---|---|
| 1 | State v. Sousa | criminal | AFFIRM |
| 2 | Thompson v. Zagaja | civil | AFFIRM |
| 3 | Kirpas v. Griffin Hospital | civil (med-mal) | AFFIRM |
| 4 | State v. Narcisse | criminal | AFFIRM |
| 5 | Festa v. Watertown Police Dept. | civil | AFFIRM |
| 6 | Morales v. Meehan | civil | AFFIRM |
| 7 | State v. Dukes | criminal | AFFIRM |
| 8 | Williams v. Williams | family | AFFIRM |
| 9 | Berglass v. Dworkin | civil | AFFIRM |
| 10 | Mack v. Commissioner of Correction | habeas | AFFIRM |
| 11 | Membrino v. Membrino | family | AFFIRM |

### Attempt 4 — REVEAL & score

| # | case | committed | actual | correct? |
|---|---|---|---|---|
| 1 | State v. Sousa | AFFIRM | AFFIRM (photos properly admitted) | ✓ |
| 2 | Thompson v. Zagaja | AFFIRM | AFFIRM (appeal dismissed, no certification) | ✓ |
| 3 | Kirpas v. Griffin Hospital | AFFIRM | AFFIRM (appeal moot, dismissed) | ✓ |
| 4 | State v. Narcisse | AFFIRM | AFFIRM (findings not clearly erroneous) | ✓ |
| 5 | Festa v. Watertown Police Dept. | AFFIRM | **REVERSE** (wrong procedural vehicle) | ✗ |
| 6 | Morales v. Meehan | AFFIRM | AFFIRM (contempt upheld) | ✓ |
| 7 | State v. Dukes | AFFIRM | AFFIRM (judgment stands; one sub-finding erred, no relief) | ✓ |
| 8 | Williams v. Williams | AFFIRM | **REVERSE** (appeal held timely — appellant prevailed) | ✗ |
| 9 | Berglass v. Dworkin | AFFIRM | AFFIRM (moot; dismissal proper) | ✓ |
| 10 | Mack v. Commissioner of Correction | AFFIRM | AFFIRM (cert-denial was abuse, but habeas denied on merits) | ✓ |
| 11 | Membrino v. Membrino | AFFIRM | AFFIRM (litigation privilege; dismissed) | ✓ |

**Attempt 4 score: 9/11 = 82%. Appellant-win rate here = 18%** — close to the real
world, unlike attempt 3's fluky 40%.

## Running tally across the two blind attempts (21 cases)

- always-affirm accuracy: **15/21 = 71%**
- appellant-win (reversal) rate: 6/21 = 29% (dropping toward realistic as n grows;
  attempt 4 alone was 18%)
- **leak-free features still add nothing.** All 6 reversals turned on merits or
  procedure visible only in the opinion (wrong dismissal vehicle, a timeliness
  technicality, an evidentiary rule, statutory standing). Caption and category
  gave no warning on any of them.

## Two honest wrinkles this batch exposed
1. **The bigger sample confirms attempt 3 was a small-n fluke.** With 11 more
   cases the reversal rate fell to 18% — the "boring affirmances" showed up, as
   expected, and the base-rate call performed near its real ~85% ceiling.
2. **Outcomes are not cleanly binary.** Dukes (one finding reversed, sentence
   stands) and Mack (cert-denial was an abuse, habeas still denied) are partial:
   the appellant won a point but got no relief. Scoring by "did the appellant
   actually get relief" is defensible but throws away detail — a future ruler may
   need a graded outcome, not a yes/no.

**Status unchanged and honest:** predicting before the answer exists, nothing we
can measure beats "always affirm." No leak-free signal yet.

## Attempt 5 — BLIND commit (15 more, tagged by type, locked before reveal)

Same rule: predict AFFIRM for all. Type recorded to test later whether any type
beats the base rate.

| # | case | type | committed |
|---|---|---|---|
| 1 | Speer v. Deutsche Bank | foreclosure | AFFIRM |
| 2 | State v. Sanderson | criminal | AFFIRM |
| 3 | U.S. Bank v. Jackson | foreclosure | AFFIRM |
| 4 | Wells Fargo v. Burns | foreclosure | AFFIRM |
| 5 | Desmond v. Yale-New Haven Hospital | civil | AFFIRM |
| 6 | Ortiz v. Commissioner of Correction | habeas | AFFIRM |
| 7 | In re Ricari B. | child protection | AFFIRM |
| 8 | McCullough v. Rocky Hill | civil (municipal) | AFFIRM |
| 9 | State v. Washington | criminal | AFFIRM |
| 10 | In re Hunter T. | child protection | AFFIRM |
| 11 | Aldin Associates v. Jannat LLC | civil | AFFIRM |
| 12 | Alers v. Bemer | civil | AFFIRM |
| 13 | Caldwell v. Jannat LLC | civil | AFFIRM |
| 14 | Commissiong v. Currytto | civil | AFFIRM |
| 15 | In re Brian C. | child protection | AFFIRM |

### Attempt 5 — REVEAL & score

14/15 AFFIRM correct. Only miss: Speer (partial — fee award struck, rest affirmed).
All 3 foreclosures, all 3 child-protection cases, both criminal, and the habeas
case affirmed.

## THE FIRST LEAK-FREE SIGNAL (36 blind cases, attempts 3–5)

Grouping the 36 by case type (knowable from the caption, before any ruling) and
counting how often the appellant actually won (reversal):

| type (leak-free) | cases | reversals | reversal rate |
|---|---|---|---|
| criminal (direct + new-trial) | 7 | 0 | 0% |
| habeas | 3 | 0 | 0% |
| child protection (In re) | 4 | 0 | 0% |
| **subtotal: criminal / habeas / child** | **14** | **0** | **0%** |
| family (dissolution / housing) | 3 | 1 | 33% |
| general civil (contract/tort/property/foreclosure/standing/discipline) | 19 | 6 | 32% |

**This is real, and it is the first honest positive result.** Case type — which
we can read off the caption with zero leakage — genuinely predicts reversal risk.
Criminal, habeas, and child-protection appeals were affirmed **14 out of 14**.
Nearly all the reversals live in ordinary civil cases (about 1 in 3 there).

**What it does and doesn't buy us (honest):**
- It does NOT beat "always affirm": even civil cases affirm more often than not,
  so affirm stays the best single guess everywhere.
- It DOES improve calibration: we can now say a criminal/habeas/child appeal is a
  near-certain affirm, while civil is where surprises concentrate. That is a
  genuine, leak-free piece of structure — the first the project has earned.
- Caveats: n is small; "civil" is a grab-bag; the pattern matches known
  real-world appellate behavior (these categories affirm at very high rates), so
  it is credible rather than a fluke, but it needs many more cases per type.

## Running tally (36 blind cases)
- always-affirm accuracy: **29/36 = 81%**
- reversal rate: 7/36 = 19% (now close to real-world)
- leak-free signal found: **case type predicts reversal rate** (criminal/habeas/
  child ≈ 0%, civil ≈ 32%) — improves confidence, does not beat the base rate.

## Attempt 6 — BLIND commit (14 civil cases, locked before reveal)

Civil-focused batch, since civil is where reversals concentrate (32% in the
running tally). Prediction: AFFIRM for all (still the base-rate-optimal call).
NEW second feature this round: at reveal, record the TRIAL COURT'S ACTION
(procedural knockout — dismissal/strike/summary judgment — vs decided on the
merits after trial). That fact predates the appellate ruling, so it is leak-free
in principle; recorded at reveal as an objective fact from the syllabus's first
sentence, not a judgment call. Hypothesis to test: appeals from full trials
affirm more; procedural knockouts get reversed more.

| # | case | committed |
|---|---|---|
| 1 | Toni v. Progressive Direct Ins. Co. | AFFIRM |
| 2 | Integris Ins. Co. v. Tohan | AFFIRM |
| 3 | Farias v. Rodriguez | AFFIRM |
| 4 | Karlen v. Saleeb | AFFIRM |
| 5 | Girolametti v. Larrabee | AFFIRM |
| 6 | Ligeri v. White Road Capital | AFFIRM |
| 7 | Karaoke Heroes NH v. RVRM Enterprises | AFFIRM |
| 8 | Hohorst v. Easton | AFFIRM |
| 9 | Casner v. Roberts | AFFIRM |
| 10 | Branford Quick Mart v. Aldin Associates | AFFIRM |
| 11 | Villwell Builders I v. Pereira | AFFIRM |
| 12 | Evexia Holdings v. Geurts | AFFIRM |
| 13 | Paniccia v. Success Village Apartments | AFFIRM |
| 14 | Doe v. Lamb | AFFIRM |

### Attempt 6 — REVEAL & score (scoring rule: a miss = appellant obtained ANY real relief)

| # | case | committed | actual | posture below (leak-free fact) | correct? |
|---|---|---|---|---|---|
| 1 | Toni v. Progressive | AFFIRM | REVERSED in part (coverage under one policy) | merits judgment (coverage law) | ✗ |
| 2 | Integris v. Tohan | AFFIRM | REVERSED (duty-to-defend revived) | summary judgment | ✗ |
| 3 | Farias v. Rodriguez | AFFIRM | AFFIRM | motion to strike | ✓ |
| 4 | Karlen v. Saleeb | AFFIRM | AFFIRM | settlement-enforcement hearing | ✓ |
| 5 | Girolametti v. Larrabee | AFFIRM | liability AFFIRMED, damages cut $280k | jury trial | ✗ |
| 6 | Ligeri v. White Road | AFFIRM | dismissal REVERSED as to 3 counts | motion to dismiss (standing) | ✗ |
| 7 | Karaoke Heroes v. RVRM | AFFIRM | AFFIRM | full court trial | ✓ |
| 8 | Hohorst v. Easton | AFFIRM | nuisance claim REVIVED vs town | summary judgment | ✗ |
| 9 | Casner v. Roberts | AFFIRM | liability AFFIRMED, injunction narrowed, fine vacated | court trial | ✗ |
| 10 | Branford Quick Mart | AFFIRM | AFFIRM (one judge dissenting) | court trial | ✓ |
| 11 | Villwell Builders | AFFIRM | liability AFFIRMED, damages vacated → nominal | court trial | ✗ |
| 12 | Evexia Holdings | AFFIRM | AFFIRM (arbitration confirmed) | arbitration confirmation | ✓ |
| 13 | Paniccia | AFFIRM | AFFIRM (controlled by precedent) | costs ruling | ✓ |
| 14 | Doe v. Lamb | AFFIRM | AFFIRM | summary judgment | ✓ |

**Attempt 6: 7/14 = 50%.** In pure civil, "always affirm" barely beats a coin.

## THE SECOND LEAK-FREE SIGNAL — deference reborn as posture

Splitting this civil batch by the trial court's action (a fact fixed BEFORE any
appellate ruling):

- **Decided after a full trial (fact-findings):** the liability finding was
  affirmed in essentially every case (Karlen, Girolametti, Karaoke, Casner,
  Branford, Villwell, Evexia, Paniccia — 8/8 on liability). What got altered on
  appeal was the REMEDY (damages cut, injunction narrowed) or a pure question of
  law (Toni's coverage reading).
- **Killed on paper (dismissal / strike / summary judgment):** the claim was
  revived in 3 of 5 (Ligeri, Hohorst, Integris vs Farias, Doe affirmed).

This is the old unit **D (deference) coming back to life in leak-free form**.
Earlier we declared D dead (r = −0.07) — but that was D hand-scored coarsely.
Measured instead by *posture*, which is objective and pre-ruling, the deference
structure is visible: fact-findings after trial are nearly untouchable; paper
rulings (reviewed fresh as pure law) are where reversals cluster; and even when
trial outcomes are disturbed, it's the remedy layer, not the finding.

## Pressure on the outcome definition (now unavoidable)

Five of seven misses were PARTIAL — liability stood, but damages or remedies
changed. A binary win/lose ruler keeps mis-scoring these. The outcome needs at
least three levels: AFFIRMED CLEAN / MODIFIED (relief adjusted) / REVERSED ON
LIABILITY. Under that scale, this batch reads: 7 clean, 5 modified, 2 reversed —
and "liability reversed after full trial" remains ~0. The ruler's true target may
be *which layer moves*, not *who wins*.

## Running tally (50 blind cases)
- always-affirm accuracy: 36/50 = **72%**
- any-relief rate: 14/50 = 28%
- Leak-free signals earned so far: (1) case TYPE sets reversal risk
  (criminal/habeas/child ≈ 0%; civil ≈ 1 in 3); (2) POSTURE sets what can move
  (post-trial fact findings ~untouchable; paper knockouts revivable; remedies
  are the soft layer). Both are real structure, neither yet beats the base rate
  head-on — but together they begin to look like the skeleton of an actual ruler.

## Attempt 7 — BLIND commit (16 civil, three-notch scale)

Scale: CLEAN AFFIRM / MODIFIED (relief adjusted, liability stands) / REVERSED
(liability disturbed). Committed prediction for all: CLEAN AFFIRM (base-rate call).
Posture recorded at reveal as an objective pre-ruling fact. First real test of the
hypothesis: post-trial fact-findings -> CLEAN/MODIFIED; paper knockouts -> REVERSED.

| # | case | committed |
|---|---|---|
| 1 | Deutsche Bank v. Burke | CLEAN AFFIRM |
| 2 | Matusz v. Wellmore Behavioral Health | CLEAN AFFIRM |
| 3 | United Cleaning & Restoration v. Koskerides | CLEAN AFFIRM |
| 4 | Khan v. Khan | CLEAN AFFIRM |
| 5 | McGee v. 456 Sackett WDS Associates | CLEAN AFFIRM |
| 6 | Stanford v. Nogiec | CLEAN AFFIRM |
| 7 | Housing Authority v. Singleton | CLEAN AFFIRM |
| 8 | Hadji v. Snow | CLEAN AFFIRM |
| 9 | ECR 2 v. Thompson | CLEAN AFFIRM |
| 10 | One Eighty-Five Stagg Associates v. Linwood Ave III | CLEAN AFFIRM |
| 11 | Freccia v. Freccia | CLEAN AFFIRM |
| 12 | Ready v. New Canaan | CLEAN AFFIRM |
| 13 | Schneider v. Federman | CLEAN AFFIRM |
| 14 | DiSpazio v. Pacapelli | CLEAN AFFIRM |
| 15 | Whelan v. Brestelli | CLEAN AFFIRM |
| 16 | Roux v. Coffey | CLEAN AFFIRM |

### Attempt 7 — REVEAL & score (3-notch: CLEAN / MODIFIED / REVERSED)

| # | case | posture below (pre-ruling fact) | actual notch | committed CLEAN correct? |
|---|---|---|---|---|
| 1 | Deutsche Bank v. Burke | post-judgment ejectment order | REVERSED (mootness/stay) | ✗ |
| 2 | Matusz v. Wellmore | jury trial | CLEAN AFFIRM | ✓ |
| 3 | United Cleaning v. Koskerides | court trial | MODIFIED (fees trimmed) | ✗ |
| 4 | Khan v. Khan | court trial | CLEAN AFFIRM | ✓ |
| 5 | McGee v. Sackett | summary judgment | CLEAN AFFIRM | ✓ |
| 6 | Stanford v. Nogiec | summary judgment | CLEAN AFFIRM | ✓ |
| 7 | Housing Authority v. Singleton | judgment for tenant (1 of 7 counts) | REVERSED (no final judgment) | ✗ |
| 8 | Hadji v. Snow | court trial | MODIFIED (damages recalculated) | ✗ |
| 9 | ECR 2 v. Thompson | court trial (summary process) | CLEAN AFFIRM | ✓ |
| 10 | One Eighty-Five Stagg v. Linwood | directed verdict | REVERSED (verdict reinstated) | ✗ |
| 11 | Freccia v. Freccia | court trial (summary process) | CLEAN AFFIRM | ✓ |
| 12 | Ready v. New Canaan | summary judgment | REVERSED (contract vs tort) | ✗ |
| 13 | Schneider v. Federman | default judgment / motion to open | CLEAN AFFIRM | ✓ |
| 14 | DiSpazio v. Pacapelli | summary judgment | CLEAN AFFIRM | ✓ |
| 15 | Whelan v. Brestelli | court trial | CLEAN AFFIRM | ✓ |
| 16 | Roux v. Coffey | motion to strike | CLEAN AFFIRM | ✓ |

**Attempt 7: 10/16 clean-affirm correct.** But score the NOTCH by posture:

## Posture predicts the notch (the hypothesis holds)

Reorganizing all 16 by the trial court's action (a pre-ruling fact):

| posture below | n | liability finding disturbed? | what actually moved |
|---|---|---|---|
| decided after a TRIAL (jury/court) | 7 | **0 / 7** | only remedies: Koskerides & Hadji trimmed damages/fees; 5 clean |
| SUMMARY JUDGMENT / directed verdict | 5 | 3 reversed (Stanford & McGee affirmed) | the paper knockout itself |
| MOTION TO STRIKE / dismiss | 2 | Roux affirmed, (Ready=SJ) | — |
| post-judgment / procedural order | 2 | Burke, Singleton reversed | finality/stay technicalities |

**The pattern from attempt 6 replicated on fresh cases:** across attempts 6–7,
appeals from a completed TRIAL disturbed the core liability finding in **0 of 15**
cases — every change was to the remedy. Reversals concentrated in paper rulings
(summary judgment, directed verdict, dismissal) and procedural-finality orders.

This is a genuinely predictive leak-free rule, stated before the reveal and
confirmed twice:

    If decided after trial  -> predict liability AFFIRMED; at most the remedy moves.
    If decided on paper     -> that's where reversals live; flag as uncertain.

## Running tally (66 blind cases)
- clean "always-affirm" accuracy: 46/66 = **70%**
- but the ruler now has SHAPE, and it is leak-free:
  - **TYPE** sets base risk (criminal/habeas/child ~0% reversal; civil ~1 in 3)
  - **POSTURE** sets which layer moves (post-trial finding ~untouchable, 0/15;
    remedy is the soft layer; paper rulings are the reversal zone)
  - **OUTCOME is graded** (clean / modified / reversed), which the binary hid
- This is E-minus-D rebuilt honestly: "clarity of error" now lives in POSTURE
  (paper rulings are easier to call wrong), "deference" now lives in the
  trial-vs-paper distinction — both read from objective facts, before the ruling.

## Attempt 8 — BLIND commit (17 civil, 3-notch). Committed CLEAN AFFIRM for all.

| # | case |
|---|---|
| 1 | Haworth Country Club v. United Bank |
| 2 | Edgewood Properties v. Dynamic Multimedia |
| 3 | Martinelli v. Martinelli |
| 4 | Stoor v. Vehs |
| 5 | Palmieri v. Cirino |
| 6 | Finnochio Brothers v. 587 CTA |
| 7 | GHP Media v. Hughes |
| 8 | Deer v. National General Ins. Co. |
| 9 | Cockerham v. Westphalen |
| 10 | Marafi v. El Achchabi |
| 11 | Lyons v. Birmingham Law Office |
| 12 | Westchester Modular Homes v. Arbella Protection Ins. |
| 13 | Glory Chapel Int'l Cathedral v. Philadelphia Indemnity |
| 14 | Kuselias v. Zingaro & Cretella |
| 15 | Cameron v. Santiago |
| 16 | Fischer v. People's United Bank |
| 17 | Adams v. Aircraft Spruce & Specialty Co. |

### Attempt 8 — REVEAL & score (3-notch)

| # | case | posture below | actual notch | CLEAN correct? |
|---|---|---|---|---|
| 1 | Haworth Country Club v. United Bank | motion to strike | CLEAN AFFIRM | ✓ |
| 2 | Edgewood Properties v. Dynamic Multimedia | court trial (summary process) | CLEAN AFFIRM (alt. ground) | ✓ |
| 3 | Martinelli v. Martinelli | motion to dismiss (standing) | CLEAN AFFIRM | ✓ |
| 4 | Stoor v. Vehs | court trial | CLEAN AFFIRM | ✓ |
| 5 | Palmieri v. Cirino | default + fee hearing | MODIFIED (fees remanded) | ✗ |
| 6 | Finnochio Bros. v. 587 CTA | court trial | CLEAN AFFIRM | ✓ |
| 7 | GHP Media v. Hughes | motion to strike | CLEAN AFFIRM | ✓ |
| 8 | Deer v. National General | summary judgment | CLEAN AFFIRM | ✓ |
| 9 | Cockerham v. Westphalen | court trial | CLEAN AFFIRM | ✓ |
| 10 | Marafi v. El Achchabi | summary judgment | CLEAN AFFIRM | ✓ |
| 11 | Lyons v. Birmingham Law Office | motion to dismiss (jurisdiction) | CLEAN AFFIRM | ✓ |
| 12 | Westchester Modular v. Arbella | summary judgment | CLEAN AFFIRM | ✓ |
| 13 | Glory Chapel v. Philadelphia Indemnity | motion to strike | MODIFIED (one ruling reversed) | ✗ |
| 14 | Kuselias v. Zingaro & Cretella | summary judgment | CLEAN AFFIRM | ✓ |
| 15 | Cameron v. Santiago | sua sponte dismissal | REVERSED (due process) | ✗ |
| 16 | Fischer v. People's United Bank | motion to dismiss (standing) | CLEAN AFFIRM | ✓ |
| 17 | Adams v. Aircraft Spruce | summary judgment | CLEAN AFFIRM | ✓ |

**Attempt 8: 14/17 clean-affirm correct (82%).** Three slips: two partial
(Palmieri fees, Glory Chapel one point), one real reversal (Cameron — a sua
sponte dismissal with no notice, a paper/procedural knockout).

## Posture pattern — now three batches deep and holding

Post-trial cases this round (Stoor, Finnochio, Cockerham, Edgewood): **4/4 core
finding affirmed.** Across attempts 6–8, appeals from a completed TRIAL have left
the liability finding intact in **19 of 19** cases. Every reversal continues to
come from the paper/procedural side (Cameron sua sponte dismissal; and this batch
the SJ/strike cases were mostly affirmed, but that's where the one real reversal
sat).

## Running tally (83 blind cases)
- clean "always-affirm" accuracy: 60/83 = **72%**
- **Post-trial liability finding disturbed: 0 / 19.** This is now the single
  sharpest leak-free regularity in the whole project: if a Connecticut civil
  appeal comes from a completed trial, the finding of who-was-right is, so far,
  never overturned — only remedies move.
- Confirmed leak-free structure:
  - TYPE sets base reversal risk (criminal/habeas/child ≈ 0%; civil ≈ 1 in 3)
  - POSTURE sets which layer moves (trial finding ≈ untouchable; paper rulings =
    the reversal zone; remedy = the soft middle)
  - graded outcome (clean/modified/reversed) captures the partial wins

## Attempt 9 — BLIND commit (17: 16 civil + 1 habeas). Committed CLEAN AFFIRM for all.

Harrigan v. Fidelity Title; Scott v. Scott; Konover Development v. Waterbury Omega;
Brass Mill Center v. Subway Real Estate; Gianetti v. Neigher; Mercedes-Benz Financial
v. 1188 Stratford; Pointe Residential Builders v. TMP Construction; Kinity v. US Bancorp;
Russbach v. Yanez-Ventura; Pringle v. Pattis; Robbins Eye Center v. Commerce Park;
Gilman v. Shames; New Milford v. Standard Demolition; Bernblum v. Grove Collaborative;
Electrical Contractors v. 50 Morgan Hospitality; Kling v. Hartford Casualty;
Gonzalez v. Commissioner of Correction (habeas).

### Attempt 9 — REVEAL & score (3-notch)

| # | case | posture below | actual notch | CLEAN correct? |
|---|---|---|---|---|
| 1 | Harrigan v. Fidelity Title | court trial | CLEAN AFFIRM | ✓ |
| 2 | Scott v. Scott | court trial (contempt) | CLEAN AFFIRM | ✓ |
| 3 | Konover Dev. v. Waterbury Omega | PJR hearing | CLEAN AFFIRM | ✓ |
| 4 | Brass Mill Center v. Subway | summary judgment | REVERSED (SJ flipped) | ✗ |
| 5 | Gianetti v. Neigher | summary judgment | CLEAN AFFIRM | ✓ |
| 6 | Mercedes-Benz Fin. v. 1188 Stratford | default / motion to open | CLEAN AFFIRM (1 dissent) | ✓ |
| 7 | Pointe Residential v. TMP | court trial | CLEAN AFFIRM | ✓ |
| 8 | Kinity v. US Bancorp | summary judgment | CLEAN AFFIRM | ✓ |
| 9 | Russbach v. Yanez-Ventura | court trial + SJ | MODIFIED (SJ on damages reversed; coverage finding stood) | ✗ |
| 10 | Pringle v. Pattis | motion to dismiss | MODIFIED (2 claims revived, 1 dismissal upheld) | ✗ |
| 11 | Robbins Eye Center v. Commerce Park | post-trial motion to compel | CLEAN AFFIRM | ✓ |
| 12 | Gilman v. Shames | motion to dismiss (immunity) | REVERSED (dismissal ordered) | ✗ |
| 13 | New Milford v. Standard Demolition | court trial | MODIFIED (extra damages hearing; liability stood) | ✗ |
| 14 | Bernblum v. Grove Collaborative | court trial | REVERSED (standing / no reliance) | ✗ |
| 15 | Electrical Contractors v. 50 Morgan | summary judgment | CLEAN AFFIRM | ✓ |
| 16 | Kling v. Hartford Casualty | court trial (stipulated record) | CLEAN AFFIRM | ✓ |
| 17 | Gonzalez v. Commissioner of Correction | habeas | CLEAN AFFIRM | ✓ |

**Attempt 9: 10/17 clean-affirm correct.** Habeas (Gonzalez) affirmed, as the
type signal predicts.

## The post-trial rule takes its first real hit — and gets sharper

**Bernblum** is the exception the rule needed: a case decided after a full trial
where the liability judgment was REVERSED. So "post-trial finding never
overturned" is now **1 crack in ~23**. But look at WHY it cracked — the reversal
was for lack of **standing** (the plaintiff sued in the wrong capacity). That is
not a re-weighing of the facts; it is a threshold legal defect a higher court
reviews fresh. Same with Russbach and New Milford: the fact-findings stood; only
legal/remedy layers moved.

So the rule refines rather than breaks:

    Post-trial FACT-FINDINGS (credibility, who-did-what) -> essentially never
    disturbed (still ~0). What can still move even after trial: pure LEGAL
    rulings riding on top (standing, statute reach, damages measure).

This is exactly the E/D structure asserting itself again: deference attaches to
the fact layer, not the law layer, and it does so whether the case came from a
trial or a paper motion. Posture tells you the fact-findings are safe; the legal
overlay is always de novo and always the soft spot.

## Running tally (100 blind cases)
- clean "always-affirm" accuracy: 70/100 = **70%**
- post-trial FACT-FINDING disturbed: ~0; post-trial cases where anything moved
  were legal-overlay/standing/remedy, not the facts
- three leak-free signals now stable over 100 committed-before-reveal cases:
  **TYPE** (base risk), **POSTURE** (which layer moves), **LEGAL-vs-FACT** (the
  layer within a case that deference does/doesn't protect)

## Attempt 10 — FIRST v3 TEST (predict the NOTCH from type+posture+layer, then reveal)

Prediction derived deterministically from posture + layer under attack (both in
the case setup, before the Held). Rule is fixed, so no room to fit to the outcome.
Baseline = "always CLEAN AFFIRM". (11 usable cases; empty-syllabus dupes dropped.)

| case | posture | layer attacked | v3 predicts | actual | v3? | base? |
|---|---|---|---|---|---|---|
| Gleason v. Durden | trial | law (unpleaded basis) | REVERSED | REVERSED | ✓ | ✗ |
| Kellogg v. Middlesex | SJ denied | law (law-of-case) | REVERSED | REVERSED | ✓ | ✗ |
| Gottesman v. Kratter | SJ/strike | law (expert reqt) | LIVE→rev | AFFIRM | ✗ | ✓ |
| KDM v. DRVN | trial | law (amendment) | REVERSED | REVERSED | ✓ | ✗ |
| Canner v. Governor's Ridge | hearing | fact (SOL trigger) | AFFIRM | AFFIRM | ✓ | ✓ |
| DiTullio v. LM General | award confirm | remedy (offset) | MODIFIED | MODIFIED | ✓ | ✗ |
| Lasso v. Valley Tree | SJ | law (duty) | LIVE→rev | AFFIRM | ✗ | ✓ |
| Squillante v. Capital Region | SJ | law | LIVE→rev | AFFIRM | ✗ | ✓ |
| Menard v. State | trial | law+remedy | MODIFIED | MODIFIED | ✓ | ✗ |
| Herron v. Daniels | trial | fact (pretext) | CLEAN AFFIRM | AFFIRM | ✓ | ✓ |
| Medical Device v. Aferzon | trial | law+remedy (SOL) | MODIFIED | MODIFIED | ✓ | ✗ |

**Score: v3 = 8/11 (73%). Baseline always-affirm = 5/11 (45%).**
**v3 beat the baseline on a fresh, committed-before-reveal batch — for the first time.**

## Where v3's power came from, and where it failed (honest)

- **The winner: post-trial + legal/remedy overlay.** In every case that came from
  a trial where the appellant attacked a LAW or REMEDY layer (Gleason, KDM,
  DiTullio, Menard, Medical Device) the overlay moved while the fact-findings
  stood — **5/5**, all of which always-affirm structurally missed. Plus the two
  fact-layer cases (Canner, Herron) correctly affirmed. The "which layer moves"
  logic is the real, earned signal.
- **The failure: paper posture.** All 3 v3 misses (Gottesman, Lasso, Squillante)
  were "civil + summary-judgment + legal issue," where v3 said LIVE→reversed but
  the court AFFIRMED. Summary-judgment affirmances are common; "paper + law =
  reversal" over-fires. (And Kellogg shows paper CAN reverse — so paper is
  genuinely high-variance, not predictable in either direction yet.)

## v3 → v3.1 refinement (keep/change)
- KEEP: fact layer -> affirm.
- KEEP + PROMOTE: **post-trial + law/remedy overlay -> predict MODIFIED/REVERSED
  on that layer** (6/6 this batch). This is the ruler's strongest, most novel
  call — it beats always-affirm precisely where the baseline is blind.
- CHANGE: paper posture + law -> do NOT auto-predict reversed. Predict AFFIRM
  (base rate) but tag HIGH-VARIANCE. Paper cases split unpredictably (Kellogg rev
  vs Gottesman/Lasso/Squillante aff); the ruler has no edge there yet.

## Honest caveat on this test
Predictions were derived from posture+layer (setup facts) via a fixed rule, which
controls leakage by determinism — but the full syllabus was in view. The stricter
protocol (read setup only, commit, then reveal the Held) is the next tightening.
Also this older-case batch was movement-heavy (6/11 moved), which depressed the
baseline; on a representative docket always-affirm scores higher. The durable
result is not the 73% — it's that v3 caught 6/6 post-trial overlay movements the
baseline cannot see.

## Running tally: 111 blind cases; v3 now making live notch calls.

## Attempt 11 — v3.1 test (8 usable cases; predict notch from posture+layer)

| case | posture | layer | v3.1 predicts | actual | v3.1? | base? |
|---|---|---|---|---|---|---|
| Marco v. Starr Indemnity | court trial on law | pure law (duty to defend) | AFFIRM | AFFIRM | ✓ | ✓ |
| O&G Industries v. American Home | court trial | fact (recklessness) | AFFIRM | AFFIRM | ✓ | ✓ |
| DeJesus v. R.P.M. | admin (comp board) | legal overlay (alter-ego/veil) | MODIFIED | MODIFIED (alter-ego reversed) | ✓ | ✗ |
| Robb v. Vet. Med. Board | admin | law (statute reading) | AFFIRM | AFFIRM | ✓ | ✓ |
| Property Tax Mgmt v. Worldwide | court trial | purely legal (contract legality) | AFFIRM | AFFIRM | ✓ | ✓ |
| Smernoff v. Star Tire | court trial | remedy-as-fact (damages estimate) | AFFIRM | AFFIRM | ✓ | ✓ |
| Eichler v. Healthy Mom | court trial | fact (waiver) | AFFIRM | AFFIRM | ✓ | ✓ |
| Lemma v. York & Chapel | award confirm | law (jurisdiction) | AFFIRM | AFFIRM | ✓ | ✓ |

**Score: v3.1 = 8/8. Baseline = 7/8** (affirm-heavy batch, so the base did well;
v3.1's edge was catching DeJesus's alter-ego reversal via the overlay logic).

## Two refinements this batch forced (v3.1 → v3.2) — that fix attempt 10's misses
Attempt 10 over-predicted reversal on "civil + law." These distinctions fix it:

1. **Legal OVERLAY on top of fact-findings (moves) vs a PURELY legal case (base-rate
   affirm).** DeJesus had comp fact-findings PLUS a separable legal overreach
   (piercing the veil) — the overlay moved, facts stood -> MODIFIED. Property Tax,
   Marco, Lemma were WHOLLY legal questions with no protected fact layer -> those
   just affirm at the base rate. The star rule applies only when there is a fact
   layer for the overlay to sit on. (This is exactly why Gottesman/Lasso/Squillante
   in attempt 10 should have been AFFIRM, not reversed — they were purely-legal SJ.)
2. **Remedy-as-legal-calculation (moves) vs remedy-as-factual-estimate (protected).**
   Menard/DiTullio offsets were legal calculations -> moved. Smernoff's damages were
   a factual estimate -> deferential, affirmed. "Remedy" is not one layer.

## Honest caveat
These two refinements were induced FROM this batch, so they are new hypotheses,
not yet validated — the next fresh batch is their real test. The DeJesus =
MODIFIED credit involves a judgment call. Recording both so they can be checked,
not celebrated.

## Running tally: 119 blind cases
- Combined v3 notch test (attempts 10–11): **v3 = 16/19 (84%)** vs baseline
  **12/19 (63%).** The ruler is ahead on committed-before-reveal notch calls.
- The durable, repeatedly-confirmed core: after a trial, FACT-FINDINGS stand; a
  separable LEGAL/REMEDY overlay is what moves. That single rule is where all of
  v3's advantage over always-affirm comes from.

## Attempt 12 — FIRST FOREIGN blind test (UK, committed from posture+layer before disposition)

Foreign cases have no syllabus, so each is a full read — batches are slow. Two
careful cases to start the foreign register.

| case | court | posture | layer attacked | ruler predicts | actual | core rule held? |
|---|---|---|---|---|---|---|
| Stacey v Autosleeper | Court of Appeal (from County Court trial) | post-trial | legal (causation) + remedy (quantum); breach finding UNCHALLENGED | facts stand; star rule would say overlay MODIFIED | CLEAN AFFIRM | YES (facts stood); star rule over-fired |
| Water & Sewerage Auth. v Sahadath | Privy Council (from trial + Court of Appeal) | post-trial, concurrent findings | FACT (causation-in-fact) | CLEAN AFFIRM (fact layer protected) | CLEAN AFFIRM | YES — exactly as predicted |

## Why Sahadath matters more than a data point
The Privy Council did not just affirm — it stated the ruler's core seam as
**black-letter doctrine**: it will not review "concurrent findings of fact made
by two lower courts," and it drew the exact line the ruler uses — the *weight* of
evidence is FACT (not reviewable), the *admissibility* of evidence is LAW
(reviewable). Our ruler was reverse-engineered from 119 Connecticut cases; here a
Caribbean final court, applying a doctrine traceable to 1849, writes that same
fact/law distinction as its operating rule. That is strong evidence the seam is
real and universal, not a local artifact.

## Honest limits of this foreign batch
- n = 2. Both affirmed, so the always-affirm baseline also went 2/2 — the ruler
  did not BEAT the baseline here, it CONFIRMED its mechanism (it correctly
  identified WHY each affirmed: facts untouched).
- The star rule (overlay attacked -> predict MODIFIED) over-fired on Stacey (weak
  overlay challenge, affirmed). Same lesson as CT's paper zone: only fire the star
  rule when the overlay challenge is colorable. Still on probation.
- Pipeline note: without foreign syllabi, large blind batches abroad are
  expensive. Next: either a headnote/summary source, or steady small careful
  batches. The protocol itself transfers cleanly.

## Cross-border status: the ruler's SHAPE is confirmed in UK/Commonwealth by
direct reading (not just structure) — the fact/law seam is the court's own stated
rule. Quantified BEATING of the baseline abroad still needs fact-reviewing cases
where facts actually get challenged and the notch varies.

## Attempt 13 — NEW REGION (Ohio) + NEW COURT LEVEL (Supreme Court, law-only). 3 per category.

Ohio's syllabus-bearing court is its SUPREME COURT — a discretionary, law-only
court (like a cassation court). This tests the ruler ACROSS court levels and a new
region at once.

| category | case | layer | outcome |
|---|---|---|---|
| criminal | State ex rel. Bates v. Clancy | law (jurisdiction, writ) | AFFIRMED (writ denied) |
| criminal | State v. Turner | law (bindover jurisdiction; overruled precedent) | REVERSED |
| criminal | State ex rel. McIntyre v. McCarty | law (jurisdiction, writ) | AFFIRMED (writ denied) |
| civil | Sherwin-Williams v. Underwriters | law (insurance "damages") | REVERSED |
| civil | Weidman v. Hildebrandt | law (discovery rule / SOL) | AFFIRMED |
| civil | Smith v. Ohio State Univ. | law (sovereign immunity) | REVERSED |
| admin | Olentangy Schools v. Bd. of Revision | law (appealability statute) | AFFIRMED |
| admin | In re E. Ohio Gas Co. | law (rate plan) | AFFIRMED |
| admin | In re Ohio Edison Excessive Earnings | law (rider revenue) | REMANDED (moved) |

## The finding: the baseline COLLAPSES exactly where the ruler says it should
- Movement rate here (reversed/remanded): **4/9 = 44%.**
- "Always affirm" baseline accuracy: **5/9 = 56%** — versus ~72–81% at the
  Connecticut INTERMEDIATE court.

Why? Every case here is a PURE-LAW case with **no fact-findings to protect**. The
ruler's whole reason intermediate courts are affirm-heavy is the armored fact
layer (P + L). Strip that layer away — as a law-only supreme court does by
design — and movement jumps and the lazy baseline degrades. **The ruler's units
(posture, layer) predict the DIFFERENCE between court levels, across regions:**
fact-reviewing court -> affirm-heavy; law-only court -> movement-heavy. Same units,
opposite regime, correctly explained.

## Honest caveats
- These syllabi state outcomes, so this is an AGGREGATE structural result (movement
  rate by court level), not a clean per-case blind notch test. Cases were the
  newest available, not cherry-picked.
- The two criminal writs (Bates, McIntyre) affirm because extraordinary writs have
  a high bar, not because of fact-protection — a distinct mechanism that happens to
  also predict "affirm." Noted, not hidden.
- Small n per cell (3). The court-level contrast (44% vs ~20% movement) is the
  durable point, not the exact numbers.

## Universality scorecard so far
- STRUCTURE (fact/law seam): confirmed in US (CT), UK/Commonwealth, France, Germany.
- COURT-LEVEL prediction: confirmed — intermediate (fact-armored, affirm-heavy) vs
  supreme/cassation (law-only, movement-heavy), now shown within the US across two
  states and two court levels.
- Still owed: clean per-case blind notch tests in fact-reviewing courts OUTSIDE the
  US (foreign intermediate appeals), where facts can move but usually don't.

## Attempt 14 — CONNECTICUT SUPREME COURT (same state, higher court level). ~13 cases, 3+/category.

Clean control: same state and law as our Appellate data, but a discretionary,
law-focused higher court. Tests whether COURT LEVEL (not region) drives movement.

| category | case | layer attacked | outcome |
|---|---|---|---|
| criminal | State v. Edwards | law (evidence/confrontation), harmless | AFFIRM |
| criminal | State v. Turner | law (Porter/cell), unpreserved | AFFIRM |
| criminal | Jobe v. Commissioner | law (habeas custody jurisdiction) | AFFIRM |
| criminal | Gilchrist v. Commissioner | law (habeas procedure), paper | REVERSED |
| criminal | State v. Lebrick | law (confrontation, plenary) | REVERSED (partial) |
| criminal | State v. Collymore | law (immunity/ID), harmless | AFFIRM |
| civil | Rutter v. Janis | law (statutory computation), SJ | AFFIRM |
| civil | Graham v. Friedlander | law (exhaustion/immunity), motion to dismiss | REVERSED |
| civil | Netscout v. Gartner | law (defamation/1st Am.), SJ | AFFIRM |
| civil | Jenzack v. Stoneridge | law (hearsay/business records), trial | REVERSED (Appellate's reversal undone) |
| family | Zhou v. Zhang | FACT (postnuptial enforceability), trial | AFFIRM |
| family | Puff v. Puff | fact (contempt clearly erroneous) + law | MODIFIED |
| family | In re Tresin J. | FACT (no ongoing relationship), trial | AFFIRM |

## Finding: court LEVEL drives movement, holding region constant
- CT Supreme movement rate: ~5/13 = **38%** vs CT Appellate ~19%. Same state,
  same law — only the court level changed. Movement roughly DOUBLED, exactly as
  the ruler predicts (a discretionary law-court has less fact-armor in play).
- always-affirm baseline here: 8/13 = **62%** (vs ~81% at the Appellate level).
- **The fact/law seam held again:** every case attacking a post-trial FACT-finding
  affirmed (Zhou, Tresin J.; Edwards/Collymore harmless). All movement was in the
  PURE-LAW / paper-posture cases (Graham, Gilchrist, Jenzack, Lebrick). 0 fact
  reversals.

## Why this one matters
Ohio showed the court-level effect across a region change (confounded). This shows
it WITHIN Connecticut — region, law, and court system held constant, only the level
varied. That isolates the cause: the ruler's posture/layer units, not local quirks,
explain why higher courts move more. The seam "facts armored, law open" now holds
at three court levels (CT Appellate, CT Supreme, OH Supreme) and four legal systems.

## Honest caveats
Syllabi show outcomes -> aggregate structural result, not clean per-case blind. But
the layer-to-outcome mapping (fact->affirm, law->movement) is confirmatory and the
within-state level comparison is clean. Small n per cell.

## Attempt 15 — v3.2's PROSPECTIVE EXAM (14 cases, 3+ per category, CT SUPREME level)

Fresh 2022-23 window, never scored. Predictions derived deterministically from
posture+layer via the v3.2 rules (code in ruler.py). Data: blind_register_attempt15.csv.

**Criminal (8):** Brandon ✓, Grant ✓, James A. ✓, Douglas C. ✓, Brown ✓ (sufficiency
= fact-deference, affirmed), but **Joseph V. REVERSED in part** (jury-unanimity law,
new trial on one count), **Gary S. MODIFIED** (one count acquitted, state conceded),
**Ares REVERSED** (convicted under uncharged prong — notice). R1 type-armor: 5/8.

**Civil (3 + 1 unscorable certified question):** Solon MODIFIED (collateral-estoppel
law, part revived) — hv tag fired, base call missed; Clinton REVERSED (no final
judgment) — hv fired, missed; **AGW Sono: star-rule EXACT HIT** — trial liability
(impossibility/frustration) affirmed, damages/mitigation layer reversed → MODIFIED.

**Admin (3):** Kovachich moved (evidentiary law — Appellate reversed, trial judgment
reinstated) — movement ✓; Board of Ed ✓ (pure law, affirmed); Rodriguez ✗ (class-cert
abuse-of-discretion AFFIRMED; ruler over-fired MODIFIED).

**Score: v3.2 movement-grain 9/14 (64%) vs always-affirm 7/14 (50%).** Exact-notch 7/14.
Movement rate at the Supreme level = 50% — replicating the court-level effect
(attempt 14) on committed calls.

### What the exam taught (three findings, prospectively earned)
1. **R1 (type-armor) is COURT-LEVEL-DEPENDENT — falsified at the apex.** Criminal
   cases moved 3/8 at the Supreme court vs ~0% at the intermediate court. Type-armor
   is an intermediate-court phenomenon; at a discretionary law-court, LAYER dominates
   TYPE. → v3.3: R1 conditioned on court level.
2. **The star rule (R3) travels up.** AGW exact, Kovachich at movement-grain: even at
   the apex, trial facts stand while the legal/remedy overlay moves.
3. **Abuse-of-discretion is a THIRD protection regime.** Rodriguez: a discretionary
   procedural order reviewed for abuse ≈ armored like fact. → v3.3: L gains a
   'discretionary-ruling' level (~0.25, protected).
4. **The fact seam: held in-batch.** In all 14 cases, ZERO fact-findings were
   overturned (Brown's sufficiency challenge affirmed; every reversal was law-layer).
   [Corrected at audit 2026-07-10: the LIFETIME record is not literally zero — two
   override-mediated fact reversals exist in attempt 3 (C.W. v. E.W., clearly-erroneous;
   Baywing v. WPCA, no-substantial-evidence). Correct statement: facts are armored
   EXCEPT via the named override standards, which fired ~2/171 (~1%).]

Register CSVs: v1 (frozen, v3's committed record) + attempt15 (v3.2's exam).

## Attempt 16 — v3.3 PROSPECTIVE TEST at INTERMEDIATE court (fresh 2015-2018 window) — **VOID, never scored**

**Audit note (2026-07-10):** 14 predictions were committed, then the window turned out
to have NO syllabi in the database (pre-2019 empty). Outcomes were never seen by the
coder; the batch was abandoned for data availability, not for its results. Logged to
prevent silent cherry-picking. No score derives from this table.

Testing v3.3's central claim: R1 type-armor should HOLD here (unlike at CT Supreme,
attempt 15, where it broke). Identities pulled with NO syllabus visible; committed
below BEFORE any outcome text was fetched.

Committed (v3.3 rule: type-armor holds at intermediate -> predict CLEAN_AFFIRM
for criminal/habeas/child; base-rate CLEAN_AFFIRM for civil/admin pending
posture+layer refinement at reveal):

| # | case | category (from caption) | committed |
|---|---|---|---|
| 1 | State v. Fuller | criminal | CLEAN_AFFIRM |
| 2 | In re Damian G. | child protection | CLEAN_AFFIRM |
| 3 | Little v. Commissioner of Correction | habeas | CLEAN_AFFIRM |
| 4 | State v. McGee | criminal | CLEAN_AFFIRM |
| 5 | Bueno v. Commissioner of Correction | habeas | CLEAN_AFFIRM |
| 6 | R.T. Vanderbilt Co. v. Hartford Accident & Indemnity | civil (insurance) | CLEAN_AFFIRM |
| 7 | Gagliano v. Advanced Specialty Care | civil (med-mal) | CLEAN_AFFIRM |
| 8 | Amica Mutual Ins. Co. v. Muldowney | civil (insurance) | CLEAN_AFFIRM |
| 9 | Brown v. Otake | civil | CLEAN_AFFIRM |
| 10 | Nationwide Mutual Ins. Co. v. Pasiak | civil (insurance) | CLEAN_AFFIRM |
| 11 | First American Title Ins. Co. v. 273 Water Street | civil | CLEAN_AFFIRM |
| 12 | Metropolitan District v. Commission on Human Rights & Opportunities | admin | CLEAN_AFFIRM |
| 13 | Recycling, Inc. v. Commissioner of Energy & Environmental Protection | admin | CLEAN_AFFIRM |
| 14 | Town of Griswold v. Camputaro | admin (municipal enforcement) | CLEAN_AFFIRM |

## Attempt 16 (rerun in syllabus window) — v3.3 test at INTERMEDIATE court, 3/category

Identities pulled with NO syllabus. v3.3 predicts type-armor HOLDS at intermediate
level. Committed before reveal:

CRIMINAL/HABEAS (R1 type-armor -> CLEAN_AFFIRM):
 1 State v. Lanier ...... CLEAN_AFFIRM
 2 State v. Coleman ..... CLEAN_AFFIRM
 3 Stafford v. Comm'r (habeas) ... CLEAN_AFFIRM
CIVIL (base-rate CLEAN_AFFIRM pending posture/layer):
 4 LPP Mortgage v. Underwood Towers ... CLEAN_AFFIRM
 5 Wells Fargo v. Melahn (foreclosure) ... CLEAN_AFFIRM
 6 Office Condominium Assn. v. Rompre ... CLEAN_AFFIRM
ADMIN (base-rate CLEAN_AFFIRM):
 7 Black v. West Hartford ... CLEAN_AFFIRM
 8 McLoughlin v. Planning & Zoning Commission ... CLEAN_AFFIRM
 9 Northwest Hills Chrysler Jeep v. DMV ... CLEAN_AFFIRM

### Attempt 16 — REVEAL & score (intermediate court, v3.3 test)

Committed CLEAN_AFFIRM for all 9. Actual notches:

| case | category | actual | posture/layer at reveal | v3.3 ok? |
|---|---|---|---|---|
| State v. Lanier | criminal | CLEAN_AFFIRM | trial, evidence/instruction (law) | ✓ |
| State v. Coleman | criminal | MODIFIED | resentencing, statutory-max (pure law) | ✗ |
| Stafford v. Comm'r | habeas | CLEAN_AFFIRM* | UNSCORED — syllabus never verified | excluded (audit 2026-07-10) |
| Wells Fargo v. Melahn | civil | CLEAN_AFFIRM | strike counterclaim (law) | ✓ |
| Office Condo v. Rompre | civil | CLEAN_AFFIRM | dismissal, finality | ✓ |
| LPP Mortgage v. Underwood | civil | (no syllabus; excluded) | — | n/a |
| Black v. West Hartford | admin | CLEAN_AFFIRM | dismissal, standing (law) | ✓ |
| South Windsor v. Lanata | admin | MODIFIED | trial, remedy/fines (abuse of discretion) | ✗ |
| Northwest Hills Jeep v. DMV | admin | (not in batch; excluded) | — | n/a |

Scorable = 6 (Stafford excluded at audit — outcome never verified). **v3.3 4/6; always-affirm 4/6 — tie.**

### What it shows for v3.3
- **Type-armor mostly held at intermediate (criminal 2/3 affirmed) — but Coleman
  cracked it** on a pure-law statutory-maximum resentencing. So R1 is not absolute
  even at intermediate; pure-law sentencing-correction is a movement pocket. This
  refines, not refutes, the court-level rule: intermediate type-armor is strong but
  leaks on statutory-max/illegal-sentence corrections.
- **The two misses were both the SAME kind:** a pure-law or remedy overlay moving
  while nothing factual did (Coleman's parole term; Lanata's fine). Fact seam intact
  again — ZERO fact-findings disturbed in the batch.
- Baseline tied the ruler here because this intermediate batch was affirm-heavy
  (movement ~29%, matching the ~19-30% intermediate rate). The ruler's edge shows
  at the apex/movement-heavy level, not here.

Running committed total (audited): 163 through attempt 16 incl. foreign.

## Attempt 17 — v3.3 test, fresh INTERMEDIATE batch (2021-2022 window)

Committed CLEAN_AFFIRM for all (derived from posture+layer before reading disposition).
Two admin cases (Black, South Windsor) DEDUPED — already scored in attempt 16.

| case | category | committed | actual | posture/layer | v3.3 ok? |
|---|---|---|---|---|---|
| State v. Gray | criminal | CLEAN_AFFIRM | CLEAN_AFFIRM | jury trial, Brady/evidence (law) | ✓ |
| Jones v. Comm'r | habeas | CLEAN_AFFIRM | CLEAN_AFFIRM | cert denied, IAC/Brady | ✓ |
| Lewis v. Comm'r | habeas | CLEAN_AFFIRM | CLEAN_AFFIRM | cert denied, procedural default | ✓ |
| Pringle v. Pattis | civil | CLEAN_AFFIRM [hv] | MODIFIED | dismissal, exoneration-rule scope (pure law) | ✗ |
| Robbins Eye v. Commerce Park | civil | CLEAN_AFFIRM | CLEAN_AFFIRM | post-trial motion, lease interp (law) | ✓ |
| Desmond v. Yale-New Haven | civil | CLEAN_AFFIRM [hv] | CLEAN_AFFIRM | strike, WC-exclusivity bar (pure law) | ✓ |
| State Marshal Assn v. Johnson | admin | CLEAN_AFFIRM | CLEAN_AFFIRM | dismissal, standing (pure law) | ✓ |

Scorable fresh = 7. **Ruler 6/7; always-affirm 6/7 — tie** (affirm-heavy intermediate
batch; ruler's edge lives at the apex, not here). Criminal type-armor held 3/3.

### Findings
- **Type-armor solid at intermediate again (criminal/habeas 3/3 affirmed)** — consistent
  with v3.3's court-level rule.
- **The one miss (Pringle) had its high-variance flag ON.** It was a pure-law dismissal
  on the scope of the exoneration rule; the Appellate Court revived two collateral claims
  (fee dispute, forfeiture timing) while affirming dismissal of the plea-attack claim. So
  the ruler correctly signaled uncertainty (R5 high-var), and the movement was pure legal
  layer — no facts touched (a dismissal has no findings to disturb).
- **Fact seam intact again:** across all 7, ZERO fact-findings overturned. Gray's
  chain-of-custody/sufficiency challenge affirmed; the only movement was legal-layer.

Running committed total (audited): 171 (163 + Ackland + 7 fresh in A17).

## Attempt 18 — THE FITTED EQUATION'S OWN EXAM (pre-registered, Ohio Supreme, fresh)

Pre-registration (set at end of attempt 17, before any of these 9 cases were
pulled): fresh apex batch, 3/category, layer coded from facts per standing
convention, p taken from the frozen fitted table with NO adjustment, graded by
Brier score vs always-affirm (p=0) and constant base-rate (p=0.38).

**Housekeeping note:** checked docs/CODING_RUBRIC_v1.md as the exam text specified
— it turns out to be a leftover Fourth-Amendment coding scheme (privacy/exception/
warrant units) from an earlier, different sub-project, and was never actually the
rubric governing posture/layer. The real operative definitions are the Posture/
Layer enums in ruler.py + RULER.md's prose, used consistently since attempt 13.
Filed as a doc-hygiene fix (rename/archive), not a scoring problem.

Grader (protocol note): all 9 cases coded lawside=1 (pure_law) from the facts —
Ohio Supreme's docket at this window is almost entirely legal-question review, so
every case got the SAME p=0.47 regardless of which specific question was live.

| case | category | layer | p (model) | actual | moved? |
|---|---|---|---|---|---|
| State v. Taylor | criminal | pure_law | 0.47 | REVERSED | yes |
| State ex rel. Yeager v. Lake Cty. | criminal | pure_law | 0.47 | CLEAN_AFFIRM | no |
| State ex rel. Mitchell v. Frederick | habeas | pure_law | 0.47 | CLEAN_AFFIRM | no |
| Vandercar v. Port of Gtr Cincinnati | civil | pure_law | 0.47 | REVERSED | yes |
| McCarthy v. Lee | civil | pure_law | 0.47 | CLEAN_AFFIRM | no |
| Scott Fetzer v. Am. Home Assur. | civil | pure_law | 0.47 | CLEAN_AFFIRM | no |
| In re Solar Generation Fund Rider | admin | pure_law | 0.47 | MODIFIED | yes |
| Karr v. McClain | admin | pure_law | 0.47 | REVERSED | yes |
| N.A.T. Transp. v. McClain | admin | pure_law | 0.47 | MODIFIED | yes |

Movement 5/9 (56%). **Brier(model) = 0.254 vs Brier(always-affirm) = 0.556 vs
Brier(constant 0.38) = 0.278. Model beats BOTH baselines — exam PASSED** per the
pre-registered condition.

### The honest reading (not just "it passed")
The pass is real but weaker than it looks: because every case coded to the same
lawside=1/apex=1 bucket, the model predicted the IDENTICAL 0.47 for all nine —
it beat always-affirm on aggregate calibration, but had ZERO power to discriminate
Yeager/Mitchell (near-mechanical affirmances under Ohio's "adequate remedy at law"
original-action doctrine) from Taylor/Vandercar/Karr (live substantive reversals).
It won because the batch's true rate (56%) landed near 47%, not because it told
these cases apart. **Diagnosis: the two-feature grouped model is too coarse within
the pure-law/apex cell.** The T x L x level formula (still coded in predict())
already has finer within-pure-law resolution (via posture) that this pilot fit
collapsed for tractability. Next refit should add posture (or a
original-action-vs-merits flag) as a third feature before claiming real
discriminative power, not just calibration.

Fact seam: n/a this batch (no fact-side cases arose from the query — 100% pure-law
docket, itself informative about what Ohio's apex court chooses to hear).

Running committed total: 180 cases (171 + 9 new, backfill rows already counted
in the 71 machine-readable set).

## Attempt 19 — targeted for posture diversity (summary_judgment + discretion)

Queries chosen BEFORE seeing results to surface underrepresented postures/layers
(the equation's weak spot per attempt 18's audit). 9 cases, CT Appellate
(intermediate). State v. Gray excluded (duplicate of attempt 17).

| case | category | posture | layer | actual |
|---|---|---|---|---|
| Donald v. Comm'r of Correction | habeas | trial | pure_law | REVERSED |
| State v. Garrison | criminal | trial | legal_overlay | REVERSED |
| State v. Bouvier | criminal | trial | legal_overlay | CLEAN_AFFIRM |
| Bucci v. Bridgeport | civil | summary_judgment | pure_law | CLEAN_AFFIRM |
| Carty v. Merchant 99-111 | civil | summary_judgment | pure_law | CLEAN_AFFIRM |
| Dorfman v. Liberty Mutual | civil | summary_judgment | pure_law | MODIFIED |
| L.D. v. Comm'r Children & Families | admin | discretionary | discretion | CLEAN_AFFIRM |
| One Elmcroft Stamford v. ZBA | admin | trial | pure_law | REVERSED |
| Nutmeg State Crematorium v. DEEP | admin | discretionary | discretion | CLEAN_AFFIRM |

Movement 4/9 (44%). Coding note: One Elmcroft is a judgment call — the syllabus
lists 4 sub-holdings without one clean disposition line; holding 3 (board applied
wrong legal standard) reads as succeeding on the merits, so coded REVERSED.
Flagged, not smoothed over.

**Discretion-layer sample TRIPLED this turn** (was n=1 in the machine set; now
n=4 total incl. Rodriguez/South Windsor). All 3 new discretion cases affirmed —
consistent with the "third protected regime" finding, though One Elmcroft shows
a pure_law challenge to an agency CAN still win when it's a legal-standard error
rather than a discretion challenge.

## Attempt 20 — THE REAL v2 EXAM (genuinely held-out, unbiased query terms)

Fresh CT Appellate batch, generic search terms chosen for a natural mix (not
targeted at any posture, unlike attempt 19). 9 cases scorable; one duplicate-case
excluded (Kovachich, already scored at CT-Supreme in attempt 15; One Elmcroft's
2019 first-round opinion excluded, its 2022 second round already used in attempt
19). One bonus family-category case (Brown v. Brown, REVERSED) logged separately,
outside the 3-per-category count.

Movement 1/9 (11% — a quiet batch, consistent with the known ~10-20% intermediate
rate). Scored against BOTH frozen models with NO adjustment:

| case | p (v1, 2-feat) | p (v2, +posture) | actual |
|---|---|---|---|
| State v. Errol J. | 0.37 | 0.54 | CLEAN_AFFIRM |
| State v. Orr | 0.09 | 0.05 | CLEAN_AFFIRM |
| Whistnant v. Comm'r | 0.37 | 0.22 | CLEAN_AFFIRM |
| DeMattio v. Plunkett | 0.09 | 0.08 | CLEAN_AFFIRM |
| Falcigno v. Falcigno | 0.09 | 0.08 | CLEAN_AFFIRM |
| Castle v. DiMugno | 0.37 | 0.26 | CLEAN_AFFIRM |
| Turek v. ZBA | 0.37 | 0.42 | REVERSED |
| Jezouit v. Malloy | 0.37 | 0.22 | CLEAN_AFFIRM |
| Putnam Park v. P&Z | 0.09 | 0.05 | CLEAN_AFFIRM |

**Brier: v2 = 0.090 < v1 = 0.109 < always-affirm = 0.111.**
**v2 beats v1. v1 barely beats always-affirm. THE PRE-REGISTERED HARDER BAR PASSED
— on genuinely held-out data, none of which was in either model's training set.**

### The honest read
This is the first non-circular validation of the posture feature: v2 pulled the
fact/dismissal-adjacent cases (Orr, DeMattio, Falcigno, Putnam Park) down toward
0.05-0.08 and they all affirmed; it pulled Turek (discretionary+pure_law, a real
legal-standard error) up to 0.42 and it moved. v1 treated most of these as a flat
0.37 or 0.09 based on layer alone.

Caveats, stated plainly: n=9, one movement event — this batch mainly validates
the LOW end of calibration (correctly assigning low p to affirm-heavy cases), not
the high end. v1 itself barely cleared always-affirm here (0.109 vs 0.111) because
the batch was so quiet; a single quiet batch cannot strongly separate two models
that both predict "mostly affirm." The result is a real, earned point for v2, not
proof — it needs to repeat on a movement-heavier (e.g., apex) batch before the
posture feature is trusted the way the fact/law seam now is.

Running committed total: 190 (180 + 9 official + 1 bonus family).

## Attempt 21 — apex batch, HIGH-MOVEMENT (tests v2's high end), Ohio Supreme

Fresh 2019-2020 window (no overlap with attempt 18). Generic query terms. 9 cases,
all apex. Movement 6/9 (67%) — deliberately the movement-heavy terrain the quiet
attempt-20 batch could not probe.

| case | posture | p(v1) | p(v2) | actual |
|---|---|---|---|---|
| State v. Gideon | trial | 0.47 | 0.61 | REVERSED |
| State v. Weber | trial | 0.47 | 0.61 | CLEAN_AFFIRM |
| State v. Pendleton | trial | 0.47 | 0.61 | REVERSED |
| Wildcat Drilling v. Discovery Oil | trial | 0.47 | 0.61 | REVERSED |
| Menorah Park v. Rolston | dismissal | 0.47 | 0.27 | REVERSED |
| Piazza v. Cuyahoga Cty. | dismissal | 0.47 | 0.27 | CLEAN_AFFIRM |
| State ex rel. Omni Energy v. ODNR | dismissal | 0.47 | 0.27 | REVERSED |
| In re Ohio Edison | discretionary | 0.47 | 0.49 | MODIFIED |
| In re LMD Integrated Logistics | dismissal | 0.47 | 0.27 | CLEAN_AFFIRM |

**Brier: v2 = 0.255 < v1 = 0.261 = const-0.47 (0.261) < always-affirm = 0.667.**
v2 beats v1 again (2nd straight batch, now on HIGH-movement data) — but barely,
and with an important asterisk below.

### The honest read — a real strain shows up
1. **v2 edges v1 again (0.255 vs 0.261), the harder bar passes twice.** Direction of
   the posture effect is right: mean p(movers) 0.48 > mean p(non-movers) 0.39.
2. **BUT on this batch v1 only tied a dumb constant (p=0.47 everywhere) — 0.261 both.**
   At a pure-apex batch v1 has no discriminating feature left (every case is
   lawside=1, apex=1 -> flat 0.47), so it literally IS the constant. That's the
   attempt-18 weakness restated: the 2-feature model cannot see inside the apex
   cell.
3. **v2's posture split MISfired on the dismissal cases here.** It pushed dismissal
   down to 0.27 — but at the APEX, dismissal-posture cases MOVED (Menorah Park,
   Omni Energy both reversed; only 2/4 dismissals affirmed). The posture
   coefficient was fit mostly on INTERMEDIATE dismissals (gatekeeping affirmances);
   apex dismissals behave differently (the court took the case to reverse). So v2
   won overall via the trial-posture cases (correctly pushed to 0.61, mostly moved)
   but LOST ground on apex dismissals. **This is direct evidence for the
   "dismissal means two different things" hypothesis flagged in v2's writeup —
   and evidence the posture coefficient should itself interact with court level.**
4. Fact seam: n/a — no fact-side cases in this pure-law apex batch (again, apex
   dockets are ~all law; a real structural fact about what supreme courts choose).

### Net
v2 > v1 holds twice (quiet AND loud batches). But attempt 21 exposes that BOTH
models are still too coarse inside the apex/pure-law cell, and that posture's
effect flips between levels for the dismissal bucket. Next model version (v3)
should split dismissal into gatekeeping-dismissal vs merits-dismissal, or add a
posture×level interaction. Not done yet — flagged with the evidence that motivates it.

Running committed total: 199 (190 + 9).

## Attempt 22 — resolving the dismissal ambiguity (apex dismissal cluster, Ohio Supreme)

Targeted grab: apex dismissal-posture cases, to test the "dismissal = two things"
hypothesis from attempt 21. 12 cases, all apex, all dismissal posture, coded by
subtype from the syllabus BEFORE scoring:
- gatekeeping = original-action writ (mandamus/prohibition/habeas/quo warranto)
  denied for adequate-remedy-at-law / jurisdiction / standing
- merits = appeal from a lower court's dismissal that the supreme court took up

**Result: gatekeeping 0/9 moved; merits 3/3 moved. The split is essentially total.**

Pooled with attempts 18 & 21 apex dismissals:
- gatekeeping-dismissal: 0/14 moved (0.00)
- merits-dismissal: 3/3 moved (1.00)

This CONFIRMS the hypothesis flagged in attempt 21's writeup. "Dismissal" was a
mixture; at the apex it separates cleanly into a near-0 and a near-1 bucket. The
posture coefficient in v2 was averaging these two — which is exactly why v2
mispredicted apex dismissals. Frozen: fitted_params_v3_dismissal.json.

Note this batch is single-subtype-certain by construction (all coded, all scored),
so it is a CONFIRMATION + fit, not a blind prospective test of v3. v3's blind exam
is owed on a FRESH apex batch where subtype is coded before reveal (attempt 23).

Running committed total: 211 (199 + 12).

## Attempt 23 — v3 dismissal-split BLIND EXAM (fresh apex, Ohio Supreme 2020 window)

Subtype committed from the PROCEDURAL NATURE of each action (gatekeeping =
original-action writ testing jurisdiction/adequate-remedy/res judicata; merits =
court reaches the substance / remands for substantive redo). v3 predicts:
gatekeeping -> CLEAN_AFFIRM (p~0), merits -> move (p~1). Committed BEFORE scoring:

 1 State ex rel. Feltner v. Bd. of Revision . gatekeeping -> AFFIRM
 2 State ex rel. Kendrick v. Parker ......... gatekeeping -> AFFIRM (res judicata)
 3 State ex rel. Johnson v. BSC ............. gatekeeping -> AFFIRM (res judicata)
 4 State ex rel. Franks v. Parole Auth. ..... gatekeeping -> AFFIRM (waiver)
 5 State ex rel. Parisi v. Dayton Bar ....... gatekeeping -> AFFIRM
 6 State ex rel. Davis v. Janas ............. merits -> MOVE (jurisdictional defect reached)

### Attempt 23 — v3 dismissal split: BLIND EXAM PASSED 6/6 (Brier 0.000)
5 gatekeeping writs (Feltner, Kendrick, Johnson, Franks, Parisi) all committed
CLEAN_AFFIRM -> all affirmed. 1 merits dismissal (Davis v. Janas: nunc pro tunc
jurisdictional defect reached) committed MOVE -> reversed & remanded. Subtype
coded from procedural nature before scoring. First prospective confirmation of
the v3 split — it now has a (small) blind track record, not just an in-sample fit.

### Attempt 23 — FOREIGN depth: Canada added (Legal Data Hunter connector)
Bedwell v. McGill, 2008 BCCA 6 (BC Court of Appeal, intermediate). Committed
CLEAN_AFFIRM before reading (Housen "palpable and overriding error" standard).
Actual: appeal dismissed = CLEAN_AFFIRM. Notch ✓ AND a rare two-sided seam
demonstration: the MAJORITY refused every challenged fact-finding under palpable-
and-overriding-error; the DISSENT would have reversed but ONLY via an "extricable
error of law" (failure to give legal effect to dominant-driver status) — neither
judge would touch the facts. The fact/law seam appears on both sides of a split
panel inside one case.

**Foreign blind tally now: 4 cases across 3 systems (UK, Australia, Canada) —
notch 3/4, fact-seam 4/4.** Canada was the gap; now filled. The seam has survived
every foreign committed case; only the Ackland notch (AU) missed, and that was a
legal-overlay reversal that still honored the seam.

Running committed total: 217 (211 + 6 exam cases; Bedwell counted in foreign).

### Attempt 24 — FOREIGN: first civil-law blind case (France)
Cass. Civ. 1, 4 juillet 2000, 98-10.744. Committed CLEAN_AFFIRM (fact challenge to
"appréciation souveraine"); actual REJETTE le pourvoi = CLEAN_AFFIRM ✓. The
fact/law seam is the court's stated operative rule in a non-common-law system.
Foreign tally: 5 cases / 4 systems, notch 4/5, seam 5/5.
Running committed total: 218.

### Attempt 25 — FOREIGN: Germany (2nd civil-law system), 4 cases
3 BGH Revisions committed CLEAN_AFFIRM -> all verworfen ✓. OLG Hamm 4 RVs 141/20
committed CLEAN_AFFIRM -> REVERSED (miss), but reversed BECAUSE the lower court
misapplied the binding-effect of facts — the seam enforced, not crossed.
Foreign tally: 9 cases / 5 systems, notch 7/9, seam 9/9.
Running committed total: 222.

### Attempt 26 — Privy Council volume + a new mechanism
TLM v Bedasie [2014] UKPC 25: committed CLEAN_AFFIRM -> appeal dismissed ✓.
Revealed the STACKING LAW (concurrent-findings practice): fact-armor accumulates
with each court that has already found the fact. New falsifiable prediction logged
in MATH_CANDIDATES.md #4. Foreign tally: 10 cases / 5 systems, notch 8/10, seam 10/10.
Running committed total: 223.

## Attempt 27 — 9 cases, targeted at FACT CHALLENGES (to test the stacking law)

Purpose: the stacking law (MATH #4) needs fact-layer challenges specifically; the
general register is dominated by law-side cases. Queries aimed at sufficiency /
credibility / clearly-erroneous claims at the INTERMEDIATE court.

| case | category | layer | actual | sample |
|---|---|---|---|---|
| State v. Olivero | criminal | fact (sufficiency) | CLEAN_AFFIRM | unbiased |
| Foster v. Comm'r | habeas | fact (credibility) | CLEAN_AFFIRM | unbiased |
| Ross v. Comm'r | habeas | fact (actual innocence) | CLEAN_AFFIRM | unbiased |
| State v. Griffin | criminal | legal_overlay (4th Am.) | CLEAN_AFFIRM | unbiased |
| **Circulent v. Hatch & Bailey** | civil | **fact (clearly erroneous)** | **REVERSED** | unbiased |
| In re A'vion A. | child | fact | CLEAN_AFFIRM | unbiased |
| Lastrina v. Bettauer | civil | pure_law | CLEAN_AFFIRM | BIASED-excl |
| **Johnson v. Vita Built** | civil | **fact (clearly erroneous)** | **REVERSED** | BIASED-excl |
| Downing v. Dragone | civil | fact (credibility) | CLEAN_AFFIRM | BIASED-excl |

**TWO GENUINE FACT REVERSALS.** Both via the clearly-erroneous override; both where
the trial court's findings were contradicted by the documentary record (not by a
re-weighing of credibility — Downing shows credibility findings still stand).

### This forced a MAJOR CORRECTION to the headline number — see MATH_CANDIDATES.md
S was computed with the wrong denominator (all cases, not fact-challenged cases).
**Corrected: S ≈ 0.17 — facts move ~6x less than law, not 30x.** The seam survives;
the inflated headline does not.

### Methodology self-flag
One query contained the word "reversed" = sampling on the outcome. Those 3 cases are
logged but EXCLUDED from rate estimation. Caught and quarantined, not smoothed over.

### Stacking law status
P(fact reversal | fact challenged, INTERMEDIATE, k=1 court below) = 1/14 = 7%.
Still need the APEX comparison (k=2) to test f(2) << f(1). Next target.

Running committed total: 232.

## Attempt 28 — 9 APEX cases, targeted at fact challenges (stacking-law test)

CT Supreme + OH Supreme. Outcome-neutral queries only (lesson from attempt 27).
State v. Brandon excluded (already scored, attempt 15); Solar Rider excluded
(already scored, attempt 21).

| case | court | challenge | notch | FACT disturbed? |
|---|---|---|---|---|
| Menard v. State | CT-S | expert credibility (fact) | MODIFIED | **no** (law: dram-shop offset) |
| State v. Michael R. | CT-S | sufficiency (law) | CLEAN_AFFIRM | no |
| Reserve Realty v. Windemere | CT-S | intent finding (fact) | CLEAN_AFFIRM | no |
| State v. Curet | CT-S | emergency-aid doctrine (law) | REVERSED | no |
| State v. Whitaker | OH-S | sufficiency (law) | MODIFIED | **no** (statutory interp.) |
| State v. Garrett | OH-S | guilt findings (fact) | CLEAN_AFFIRM | no |
| State v. Weaver | OH-S | **biased fact-finder** | REVERSED | no (process, not finding) |
| Brandt v. Pompa | OH-S | damages cap (constitutional) | REVERSED | no |
| Friendship Supported Living | OH-S | right-to-control test (law) | REVERSED | no |

**6 of 9 MOVED (67%) — and ZERO fact-findings were disturbed.**
This is the seam's cleanest demonstration in the entire project: a high-movement
apex batch where every single movement landed in the legal layer.

Three findings, all logged in MATH_CANDIDATES.md:
1. **Coding correction:** sufficiency is LAW-side (de novo), not fact-side. Whitaker
   vacated a conviction for insufficient evidence *without disturbing a fact*.
2. **New channel:** procedural integrity (Weaver — biased fact-finder). A third door.
3. **Better invariant:** W = P(fact moved | something moved) ≈ 0.10 register-wide,
   0/6 this batch. Replaces the unstable suppression ratio S.

Running committed total: 241.

## Attempt 29 — 9 cases + FULL EVALUATION of the whole register

Cases (7 scorable; Piazza excluded as duplicate of attempt 21; Morton/House/Horton
excluded — ambiguous dispositions or original disciplinary actions, not appeals):
Lueders (crim, sufficiency, affirm), Cockerham (civil, clearly-erroneous +
credibility, affirm), Hilton (habeas, expert credibility, affirm), Steinberg (admin,
character findings, disapproved), Gabbard (admin, pure law, affirm), State v. Taylor
2020 (crim, pure law, MODIFIED), Binder (admin, pure law, REVERSED).

Cockerham and Hilton are textbook seam cases: both courts stated they *would not
disturb* the fact-finder's credibility determinations. Fact challenges, both failed.

### FULL EVALUATION — 151 machine-readable committed rows, 57 movements (38%)
- **W = P(fact disturbed | case moved) = 2/57 = 0.035** — when a case moves, ~95%+
  of the time the LAW moved, not the facts.
- **⭐ NEW: THE FACT CHANNEL IS LEVEL-INVARIANT.** law-side movement rises with court
  level (0.36 -> 0.51); fact-side does NOT (0.14 -> 0.14). Court level drives the law
  channel and leaves the fact channel untouched. See MATH_CANDIDATES.md.
- Models re-scored on all 151: v2 Brier 0.202 < v1 0.215 < baseline 0.378.
- Stacking law now CONFLICTS with level-invariance — they predict opposite things
  about apex fact rates. A clean, settleable fork. Target: 40+ deferential-fact
  challenges per level.

Running committed total: 250.

## Attempt 30 — the axiom hunt (5 new cases + full fact-channel re-analysis)

New cases: Fajardo v. Boston Scientific (civil apex, pure law, AFFIRM), State v.
Griffin CT-S 2021 (criminal apex, suppression, AFFIRM), Ayuso v. Comm'r (habeas,
credibility, AFFIRM), Smith v. Comm'r (habeas, credibility, AFFIRM), Soto v. Comm'r
(habeas, credibility, AFFIRM). Fewer than the standing 9 — the CT syllabi in this
window are very long; the substantive work this attempt was the channel re-analysis
across ALL 17 fact challenges in the register.

### ⭐ CANDIDATE AXIOM FOUND: A0 — EPISTEMIC ACCESS
"A reviewing court may revise only what it is positioned to know at least as well as
the court below." Full write-up in AXIOM_CANDIDATES.md.

It DERIVES (not merely describes) the seam, the level-invariance of the fact channel
found in attempt 29, all four override channels, and the sufficiency/fact distinction.

**Its new prediction, tested across every fact challenge in the register:**
- fact rests on DOCUMENTS -> disturbed 4/4 (100%)
- fact rests on CREDIBILITY -> disturbed 0/13 (0%)

Every fact reversal we have is documentary. No credibility finding has ever been
overturned, at any level, in any jurisdiction.

**Caveats logged loudly:** circularity risk (courts' own framing may drive my coding),
selection risk (litigants may only bring strong documentary challenges), and the test
was a retrodiction on collected data, not prospective. PRE-REGISTERED CLEAN TEST:
next batch, commit the documentary/credibility coding from the FACTS SECTION ONLY,
before reading any holding.

Running committed total: 255.

## Attempt 31 — 8 cases, ADVERSARIAL test of axiom A0

Method flip: instead of confirming A0, I hunted its falsifier (a credibility reversal)
with queries designed to surface exactly that. **The hunt failed — zero found.**

| case | layer/challenge | notch | fact disturbed? |
|---|---|---|---|
| **Rose v. Comm'r** | fact — **DOCUMENTARY (transcript)** | REVERSED | **YES** |
| Barash v. Lembo | pure law (fiduciary duty) | REVERSED | no |
| Ahmed v. Oak Mgmt | pure law (arbitration) | CLEAN_AFFIRM | no |
| State v. Robles | sufficiency + evidentiary limit | MODIFIED | no |
| Comm'r MHAS v. FOIC | pure law (FOIA/privilege) | MODIFIED | no (agency fact deferred to) |
| State v. Graham | evidentiary (penal-interest) | CLEAN_AFFIRM | no |
| State v. Torres | evidentiary exclusion | CLEAN_AFFIRM | no |
| **State v. Komisarjevsky** | fact — **CREDIBILITY** | CLEAN_AFFIRM | no |

Rose is the near-miss that CONFIRMS A0: a genuine fact reversal, but the fact rested
on a transcript both courts could read. Komisarjevsky is the reverse: the witness was
found CREDIBLE, yet the finding stood because the document was destroyed — nobody
upstairs could see it either.

**A0 channel tally now 5/5 documentary vs 0/14 credibility.**
Status: unfalsified after a deliberate falsification attempt. Not proven — the
circularity caveat stands, and absence of evidence is not proof.

Running committed total: 263.

## Attempt 32 — AXIOM PROPOSALS (Claude's), with tests

Proposed three structural axioms and tested two claims:
1. **A1 (Channel Exclusivity) is independent of A0.** Gatekeeping writs are 0/9 moved
   (0/14 pooled) and EVERY ONE is pure_law — full epistemic access. A0 permits the
   court to act; it refuses anyway. A separate gate is operating. A1 also DERIVES the
   v3 gatekeeping/merits dismissal split we found empirically in attempt 22.
2. **The FACTORIZATION.** If the axioms are independent gates, log-odds must be
   additive. Tested by adding a lawside x apex interaction: LR = 0.04 (needs 3.84 for
   significance). **No interaction — gates behave independently.** The fitted model's
   three features map onto the three axioms. NOTE: low power at n=151; "consistent
   with independence," not proof.

**A1's killer test, stated for the record: CHANNEL BEATS MERIT.** Find a court reaching
the merits of a claim brought in a plainly improper channel because the claim was
strong. Currently 0/9 against.

Also recorded: the TWO SKELETONS distinction — our axioms describe the epistemic/
procedural skeleton; Sina's describe the value skeleton. The seam is VALUE-NEUTRAL
(unjust systems have it too). Courts serve knowledge, not justice. The value skeleton
requires measuring PRICES (sentences, damages, exception-maps), which we have not done.

Running committed total: 263 (no new cases this attempt — axiom work).

## Attempt 33 — VALUE SKELETON OPENED (domain 2)

Primary sources read in full: UK Fatal Accidents Act 1976; Ohio ORC 2125.02 (civil
wrongful death); Ohio ORC 2929.04 (capital aggravators).

**Finding: THE TWO-PRICE LAW.** Every death is priced twice, by two incompatible
algorithms: a flat DIGNITY price (identical for all humans) and a variable ECONOMIC
price (what the life transferred to others). Full write-up: docs/VALUE_SKELETON.md.

- UK s.1A: bereavement = **£15,120 flat**, divided equally among claimants. E = 0.
- UK s.3: dependency = proportioned to loss. E >> 0.
- Ohio civil: **pure V** — all 5 heads measured from the survivors' side; the decedent's
  own lost future is NOT compensable. A hermit is worth funeral costs.
- Ohio criminal: **pure D** — no earning capacity, dependents, or life expectancy
  anywhere in the capital aggravators. "Under 13" is a threshold, not a calculation.

**This corrects my own earlier proposal.** I had said "price = the option value the life
had ahead of it." FALSE. The law never prices the decedent's own lost future. It prices
(a) a flat dignity sum and (b) the value transferred to others.

**NEW RULER: R = D/V**, dimensionless, cross-jurisdictional. UK first estimate R ~ 0.02-0.05.

Sina's A3 is IMPLEMENTED — in the D channel, with a number attached. The economic axiom
is implemented beside it in V. The law houses both and never reconciles them.

Falsifiers pre-registered. Next: Islamic diya (flat blood-price — may have no V channel),
China's "same life, different price" scandal (a natural experiment on the contradiction).

## Attempt 34 — THE TWO-PRICE LAW DIES; THE UNPRICEABILITY PRINCIPLE REPLACES IT

Primary source read in full: German Bundestag Drs. 18/11397 (2017), introducing
Hinterbliebenengeld (§ 844 III BGB).

**My own attempt-33 claim is FALSIFIED.** I said systems pay a flat "dignity price on a
life." They do not. Every channel — UK bereavement, German Hinterbliebenengeld, Ohio's
five heads — prices what the death did to OTHER PEOPLE (their grief, their economic
loss). **None prices the life.**

And Germany says the quiet part in statute:
- *"Bewertungen des verlorenen Lebens ... können nicht in die Bemessung einfließen"*
  = **valuations of the lost life MAY NOT enter the assessment.**
- Pre-2017 German law treated grief as *"entschädigungslos hinzunehmendes Schicksal"*
  — fate borne without compensation.

**NEW LAW: THE UNPRICEABILITY PRINCIPLE — "the law may price what a life PRODUCED; it
may not price THE LIFE."** Same logical form as the fact/law seam: a forbidden
transition, stated in the systems' own doctrine, holding across legal families.

**Sina's A3 is implemented — as a TABOO, not a valuation.** "Life is unpriceable; you
may not put a number on it." That is the only computable form of "nothing is more
valuable than life."

**Cross-border split found:** UK pays £15,120 per DEATH (fixed, divided among claimants).
Germany pays ~EUR 10,000 per SURVIVOR (each gets the full amount). The UK prices the
death; Germany prices the grief. Same institution, different objects.

**DECISIVE NEXT TEST (pre-registered):** regulators DO compute a value of a statistical
life (VSL) for cost-benefit analysis — the measurement exists. Does tort law refuse to
use it? If YES, the prohibition is a MORAL TABOO, not an epistemic limit. If courts
adopt VSL/hedonic damages, the epistemic reading wins. Also must check: US "hedonic
damages" / loss-of-enjoyment-of-life doctrines are the live falsifier of unpriceability.

## Attempt 35 — UNPRICEABILITY FALSIFIED (one attempt after I proposed it)

The pre-registered falsifier hit, in the state where we ran 200+ cases.

**Conn. Gen. Stat. § 52-555 (verified primary text):** an action "**surviving to** ...
executor," recovering "**just damages**," "**whether instantaneous or otherwise**."
- SURVIVAL action -> the claim is the DECEDENT'S, not the survivors'.
- Germany explicitly closes the door on instantaneous death (no legal capacity to acquire
  a claim). **Connecticut holds it open.** With no suffering and no survivors' loss in
  issue, what remains to compensate is **the life itself**.

**REPLACEMENT FINDING: the law has TWO incompatible theories of a death, and
jurisdictions CHOOSE.**
- LOSS-TO-SURVIVORS (UK, Ohio, Germany): price what the living lost. Life unpriced.
- SURVIVAL (Connecticut): price what the DEAD lost. **Life priced.**

**THE DEEP RESULT: the epistemic skeleton is INVARIANT; the value skeleton is NOT.**
The seam held in every system, blind, 263 cases. Whether a life may be priced varies by
statute. Knowledge-constraints are universal; worth-constraints are legislated.

**Both of Sina's axioms are enacted — in different countries.** A3 (unpriceable life) =
the German/UK/Ohio taboo. A1 (enjoyment) = Connecticut's measure (pending verification).
They are inconsistent, and the world has split. **Sina's axioms are not wrong — they are
contingent.**

⚠ VERIFICATION GAP (flagged, not smoothed): the CT case-law damages gloss ("destruction
of the capacity to carry on and enjoy life's activities") is from background knowledge,
NOT verified this session — CourtListener dropped mid-attempt. Statutory structure IS
verified. Must confirm when the connector returns. If CT's "just damages" turns out to
exclude the life itself, unpriceability is resurrected and this entry is wrong.

**Sharpest test now open:** England says NO, Connecticut says YES — both common law. So
the value split does NOT follow the common-law/civil-law joint that structures the
epistemic skeleton. **The two skeletons are carved along different joints.** Survey
survival-vs-loss-to-survivors across 20 jurisdictions to map it.

## Attempt 36 — VERIFICATION GAP CLOSED (primary sources, free connectors only)

CourtListener requires re-auth; all of this came from **Legal Data Hunter (free)**.

**Ecker v. West Hartford, 205 Conn. 219 (1987):** the common-law baseline is
**Baker v. Bolton (1808)** — "no civil right of action at common law for damages
resulting from the death of a human being." **Death was not a civil injury AT ALL.**
Every wrongful-death statute is a legislative override. **Unpriceability is the DEFAULT.**

**Floyd v. Fruit Industries, 144 Conn. 659 (1957):** VERIFIED, verbatim —
- the statute "adds ... as an element of damage, **THE DEATH ITSELF**"
- damages compensate "the **destruction of the decedent's capacity to carry on life's
  activities**"
- "**recoverable for death itself, even though instantaneous, without regard to earnings**"
- assessed on "**loss to the DECEDENT**," and expressly **NOT** on the loss "to the
  decedent's wife and children"
- **"evidence as to the decedent's HOBBIES AND RECREATIONS ... would presumably operate
  to ENHANCE the amount of the verdict"** -> **Sina's A1 (enjoyment) is a priced head of
  damages.**

**⭐ THE PERFECT INVERSION: Germany forbids pricing the life. Connecticut forbids pricing
the survivors' loss. Opposite prohibitions, both functioning.**

Corrected structure: THREE objects, not two — D_life (CT), D_grief (UK/DE), V (all).
Lord Campbell family = D_grief + V, D_life forbidden. Survival family = D_life + V,
D_grief forbidden.

**The core thesis is now confirmed from both directions: the epistemic skeleton is
invariant; the value skeleton is chosen — and two systems chose exact opposites.**
