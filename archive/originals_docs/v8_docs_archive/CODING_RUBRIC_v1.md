# Synthium Judicial Coding Rubric v1 (FROZEN)

This rubric exists because the v0 court-derived cases were coded *outcome-aware*
(the coder saw the holding first). That can unconsciously fit features to the
known result. v1 fixes the protocol and the one operator ambiguity the data
exposed.

## Blind protocol (mandatory)

1. Read ONLY the facts / background section of the opinion. Do **not** read the
   holding, disposition, or reasoning yet.
2. Code all 12 units and the operator flags from the facts alone. Commit them.
3. ONLY THEN read the disposition and record the outcome (GRANTED / DENIED).
4. Never revise a unit value after seeing the holding. If the facts were
   genuinely insufficient to code a unit, record it as missing, not guessed.

A unit you would code differently once you know the outcome is a unit you were
coding from the outcome. The protocol is the guard against that.

## Operator flags mean PRESENT-ON-THE-FACTS, not UPHELD

The v0 dominance test failed because `op_exigency` was set for a case where
exigency was *claimed and rejected*. Resolution: an operator flag records that
the doctrine was **raised / factually in play**, NOT that the court upheld it.
"Upheld" is a function of the outcome and is therefore unblindable — coding it
would leak the target. Consequence: `dominance[op_exigency]` is ill-posed (mere
invocation should not dominate) and is retired. Dominance, if tested, uses a
fact-codeable trigger such as `op_home_core` (was this a search of the home's
interior?), which can be coded blind.

## The 12 units — anchored 0..1 (code from facts only)

**Obs — Observability.** Lawful perceptual grounding behind the state action.
0.2 = action on a hunch / non-criminal conduct; 0.5 = tip or indirect basis;
0.8 = officer directly perceived contraband/violation (plain view, plain smell).

**Priv — Privacy legitimacy.** Baseline privacy interest in the place/thing,
*before* exceptions. THIS IS THE BASE DIMENSION absorption tests.
0.05–0.15 = abandoned property, open fields, exposed garbage, knowingly exposed
to the public/third parties (no reasonable expectation); 0.35 = automobile
interior; 0.6 = commercial space, bag/container; 0.85–0.98 = interior of the home.

**Excp — Exception strength.** Force of the doctrine offered to override privacy,
as raised on the facts. 0.2 = no real exception, bare assertion; 0.5 = colorable
exception; 0.8 = strong, squarely-applicable exception (clear automobile + PC,
valid consent, search incident to lawful arrest).

**Rem — Remedial proximity.** Closeness between the alleged violation and the
evidence sought to be excluded. 0.2 = violation collateral / attenuated /
independent source (e.g. knock-and-announce under Hudson, later jailhouse calls);
0.8 = evidence is the direct product of the challenged search.

**Close — Doctrinal closure.** How settled/compressed the controlling doctrine is.
0.3 = open or splitting question; 0.6 = mostly settled with wrinkles; 0.85 =
black-letter, squarely controlled by precedent.

**Amb — Factual ambiguity.** Contestability of the threshold facts. 0.15 = facts
on video / undisputed; 0.5 = some dispute; 0.85 = credibility contest, no record.

**Temp — Temporal admissibility distance.** Procedural-time distance between the
original act and the evidentiary use. Default 0.5 unless the facts show a long
gap or intervening events.

**Gate — State-action gateway weight.** Degree to which Fourth Amendment scrutiny
narrows because the actor was private. 0 = ordinary police action; >0 only when a
private party performed the search.

**Bound — Boundary reclassification weight.** Degree to which the place/thing is
classified OUT of the protected zone (curtilage→open field, container→abandoned).
0 = no reclassification; high = the core privacy holding is a reclassification.

**Spec — Warrant specificity.** Particularity of any warrant. 0.2 = warrantless
(no warrant to be specific about); 0.85 = detailed, particular warrant.

**Scope — Authorization-scope fidelity.** Match between authorization and the
action actually taken. 0.15 = action grossly exceeded any authorization; 0.85 =
action stayed within authorization.

**JRem — Jurisdictional remedial regime.** Availability of remedy dampers (good
faith, etc.). Default 0.5–0.7; lower where conduct is egregious enough that good
faith is implausible on the facts.

## Operator flags (0/1, present-on-the-facts)

abandonment, consent, exigency, good_faith, attenuation, private_search,
scope_breach, curtilage, emergency_aid, public_exposure, automobile_exception,
protective_sweep, probation_waiver, search_incident, boundary_reclassification,
digital_privacy, home_core, warrant_particularity.

Set 1 if the doctrine is raised or squarely in play on the facts; 0 otherwise.
Do not condition on whether the court accepted it.
