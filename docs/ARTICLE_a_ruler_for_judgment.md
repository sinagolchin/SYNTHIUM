# A Ruler for Judgment

*An open research note from the Synthium project. Nothing in this article is a confirmed finding. It describes a question, a method, and some early guesses — and it is an invitation to help test them, or break them.*

---

## The question

We measure length with rulers and heat with thermometers. Can anything like that be built for an abstract concept — for something like *judgment*?

Not as a metaphor. A real instrument: named quantities, a formula that combines them, and predictions that can fail in public. If the predictions keep holding across many independent tries, the concept has measurable structure. If they collapse, that is worth knowing too.

Synthium is a project built around that question, and behind it sits one deeper conjecture: that an abstract concept may carry two kinds of structure at once. One kind would be the same everywhere, whether anyone likes it or not — call it the concept's **physics**. The other kind would be chosen, differently, by each community — call it its **ethics**. If judgment really splits this way, then a question like "which parts of justice are universal, and which are local choices?" stops being philosophy-only and becomes something you can check.

Everything below should be read as hypothesis. The project's verified foundation is deliberately small right now (more on that near the end), and no statistical claims are made in this article.

## Why courts

To measure judgment you need a domain where judgment is written down, where outcomes are recorded, and which exists everywhere. Appellate courts are exactly that.

A lower court decides something. A higher court reviews it. The result is recorded in a small set of outcomes — affirmed, reversed, modified — and the higher court explains its reasoning in writing. This structure repeats across criminal, civil, and administrative law, in essentially every country, going back centuries. Millions of documents, all following the same basic shape: *a decision, a challenge, a review, an outcome, and the reasons.*

That is a natural laboratory for judgment. It is not the only possible one — the same approach could try medical second opinions, grant reviews, or referee decisions — but courts publish more of their reasoning than almost anyone else.

## The first thing you notice — in the courts' own words

Read full appellate opinions from different countries and one structural feature keeps appearing. It is not hidden; the courts state it themselves, each in its own doctrine.

Higher courts treat **facts** and **law** under different rules. Findings of fact made below are armored: in the United States a fact finding "will not be disturbed unless clearly erroneous." In France, the lower judges' assessment of the evidence is *l'appréciation souveraine* — sovereign, not for the high court to redo. In Japan, Article 405 of the Code of Criminal Procedure simply does not list "the facts were wrong" among the grounds for final appeal. In Germany, the *Revision* examines legal error only. Meanwhile questions of **law** are wide open: reviewed "de novo," under "plenary review," fresh, with no deference at all.

Sometimes both rules appear a page apart in a single opinion — the same panel saying, in effect, *we may not touch what the trial judge found happened, but we owe his legal conclusions nothing.*

Call the line between these two zones the **seam**. To be clear about what is and is not being claimed: that these doctrines exist is just black-letter law, quotable from the opinions. The research questions sit on top of it, and they are open. Is the seam genuinely present in every legal system, including ones built on very different traditions? Does it have the same shape everywhere? And *why* does it exist at all?

## A first-draft ruler

Here is the project's current prototype instrument, in plain words. An appeal is a tug-of-war between two quantities.

**E — error clarity** (0 to 1): how obviously the decision below got the dispositive point wrong. A ruling that looks basically correct scores low; a glaring, can't-miss mistake scores high.

**D — deference** (0 to 1): how much armor the decision below wears. A pure legal question has thin armor, because the higher court decides it fresh. A fact found by the judge who watched the witnesses, or a call entrusted to an agency's discretion, wears heavy armor.

The formula subtracts one from the other:

> **Ω = E − D.** Predict that the challenger wins if Ω is positive.
> **Override:** if E is high enough (≥ 0.7 on the current scale), predict a win regardless of D — a clear enough error punches through any armor.

The override was not designed in advance. In an early trial batch, one administrative case broke the plain formula: the challenger won despite maximum deference, because the agency's finding had no evidence behind it at all. The formula was edited to fit reality, and the edit was logged. That loop — reality edits the ruler, never the reverse — is the whole method in miniature.

An honest status note: in its first trial run, the scoring of E and D was done by one coder who already knew the outcomes. A perfect fit under those conditions proves nothing; it may only show a coder agreeing with himself. The prototype earns nothing until it survives blind scoring, at volume, by people who are not its authors. That is precisely the work being invited here.

## Three structural guesses

Behind the ruler sit three candidate axioms — guesses about *why* appellate judgment behaves as it does. Each sticks its neck out; each names what would falsify it.

**A0 — epistemic access.** *A court may revise only what it can see at least as well as the court below.* The trial judge watched the witnesses breathe; the appeals panel reads a transcript. If A0 is right, it explains the seam without any appeal to tradition — and it makes a sharp prediction: the fact-challenges that *can* succeed are the ones resting on evidence the higher court sees exactly as well as the lower one did (documents, contracts, video, forensic reports), not on live-witness credibility. One clean counterexample — a higher court overturning a pure credibility finding with no new documentary evidence — would wound it badly. A known weakness to keep in view: courts might merely be reciting the deference doctrine rather than being constrained by what they can see, so confirmations risk circularity. The clean test (classify the evidence type from the facts section alone, *before* reading the holding, then check) is designed but has not yet been run at scale.

**A1 — channels.** *The right forum at the right moment beats merit.* A meritorious claim brought in the wrong channel, or at the wrong time, loses anyway — and the door usually closes without the merits ever being examined.

**A2 — inertia.** *The judgment below stands unless error is shown.* Ties go to what already exists; the challenger always carries the burden.

None of these is established. They are stated here so that others can attack them.

## The value side: who may price a life?

If the seam is the candidate for judgment's physics, the values a system enforces are the candidate for its ethics — the part each community chooses. The sharpest probe found so far is wrongful death, because every legal system must answer the same terrible question: what follows, in law, when a life is wrongly ended?

Reading statutes and cases in full text, the *mechanisms* differ enormously from system to system. Some let the estate recover for the lost life itself; others refuse to price the life at all and compensate the survivors' grief instead; some fix a single flat statutory sum for bereavement; some publish an explicit state formula; in classical Islamic law the amount (*diya*) is fixed by scripture rather than by any court's discretion. Each of these descriptions deserves independent re-verification — treat them as pointers, not established facts. What matters for the research program is the shape of the variety.

And inside that variety hides one pattern worth stating as a conjecture, because it would be easy to break if false: in every system examined so far, the price of a life is set by a *sovereign* of some kind — a jury, a legislature, a regulator's published formula, scripture — and never discovered by a market inside the courtroom. Candidate axiom: **you may not price what you have no standing to price.** A single system that lets adjudication import a market valuation of a life as such would refute it.

There is a refined question here, better than the crude "is ethics universal?": different systems may be giving *different answers to the same underlying question* — how to honor a life — so that the mechanisms diverge while the commitment beneath them may not. Separating purpose from mechanism, across many jurisdictions, is unclaimed territory.

## The method — and the scars that shaped it

The working loop is simple. Propose a unit or formula. Pull fresh cases. Score the inputs. Predict. Compare with the real outcome. Keep what held; change what broke; log every change with its reason. Two value-side conjectures have already been proposed and killed within one attempt each — that is the system functioning, not failing.

The project also learned some rules the hard way, by violating them first and paying for it:

1. **Full primary text only.** Court-published summaries are convenient and misleading. An early phase of this project ran mostly on such summaries; everything built on them was later demoted to provisional. A case counts only when the complete opinion has been read, with the source recorded.
2. **Counts must be machine-made.** A running tally kept by mental arithmetic across sessions drifted upward and had to be retired entirely. Now a case exists only as a row in a verified ledger, and any number cited must come from counting that file.
3. **Blinding must be mechanical, not honor-system.** Score the inputs before the outcome is visible to you; seal the committed prediction (timestamp and hash) before revealing the result.
4. **Pre-register.** Say what would prove you wrong before you look.

These four rules are, in a sense, the project's first genuine findings — findings about how *not* to fool yourself.

## Where the project honestly stands

At the time of writing, the verified ledger holds a **single-digit number of cases** — each read in full, each with its source cited, spanning a first spread of jurisdictions and all three categories (criminal, civil, administrative). Earlier exploratory passes covered far more cases and suggested patterns, but they do not meet the current standard, so no numbers from them are claimed here.

That is not an embarrassment to hide; it is the price of doing it properly, paid in public. It also means anyone joining now joins at the ground floor of the verified rebuild — not decorating a finished result, but laying foundation stones.

## How to work on it

Pick whichever entry point fits you.

**Code a batch.** Choose a jurisdiction whose language you read. Pull three criminal, three civil, and three administrative appellate decisions — complete opinions, from any full-text source (official court portals, national databases, open repositories). For each case, *before* looking at the outcome, record: the procedural posture, whether the challenge attacks facts or law, and your E and D scores. Then reveal the outcome, compare, and log — for each case — whether the formula held or broke, and why.

**Attack an axiom.** Hunt for one clean counterexample. A higher court reversing a live-witness credibility finding without new documentary evidence would damage A0 more than a hundred confirmations could help it. A case where a clearly meritless claim won because it used the right channel, or a meritorious one that was heard despite the wrong channel, tests A1.

**Run the value probe.** In your own legal system: who prices a wrongfully ended life, under what mechanism — and is that price ever taken from a market? Write down the statute and the leading case, from full text.

**Replicate the blinding.** Build or use any procedure that makes it *mechanically impossible* to see the outcome before committing the prediction, and share it.

The only non-negotiable standard across all of these: complete primary text, sources cited, predictions committed before outcomes are seen, and every kept-or-broken result logged — including the broken ones. Especially the broken ones.

## One sentence

Courts everywhere may be running the same epistemic machine with different value settings. If that is true, it can be measured. If it is false, it can be broken. Either result is worth having — and either is within reach of anyone willing to read whole opinions and write down, in advance, what would prove them wrong.
