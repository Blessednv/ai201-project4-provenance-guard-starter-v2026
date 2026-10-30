# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |
f
Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives

<!-- Your criterion. It must name a number. -->

Human writing is rarely accused of being AI.

Of 10 pieces I wrote myself, at most 1 is labeled **high-confidence AI**. This must hold in all three test trials. If one trial has 2 or more, it counts as a miss. A piece labeled "unsure" or "high-confidence human" does not count against the target.

**Why this target:**

A false accusation is the most damaging mistake this system can make. A real writer wrongly called AI loses trust and may leave the site. Missing a few AI submissions costs the site much less. So I allow at most 1 false accusation in 10, and I don't count "unsure" because it doesn't accuse anyone.

---

## 2. Score spread

<!-- Your criterion. -->

Clearly-AI and clearly-human text score far apart.

I test with 5 pieces that are clearly AI-written and 5 pieces I wrote myself. The average score of the AI pieces must be at least **0.3 higher** than the average score of the human pieces. This must hold in all three test trials. If any trial has a gap under 0.3, it counts as a miss.

**Why this target:**

If AI and human text score close together, the labels don't mean anything, and many people would land in "unsure" or get the wrong label. A gap of 0.3 is big enough for the three labels to separate them, but not so big that it's impossible for a detector that only sees writing style.

---

## 3. Label coverage

<!-- Your criterion. -->

I will test with the same mixed set of 15 texts (10 I wrote myself, 5 AI-generated) in every trial. Every one of the three labels (high-confidence human, unsure, high-confidence AI) must appear at least once, and "unsure" must appear at least twice. This must hold in all three test trials. If any label is missing, or "unsure" appears fewer than 2 times, in any trial, it counts as a miss.

**Why this target:**

A label that can never appear is a broken label, and it means the score ranges have a gap. "Unsure" matters most. It is the safety net that protects a writer who may have written every word, because it admits doubt without accusing anyone. If the two thresholds are too close together, borderline text gets forced into a hard guess. Requiring "unsure" at least twice in every trial shows the middle band is wide enough to catch ambiguous writing, even when the model scores the same text differently from one run to the next.

---

## 4. Appeal path

<!-- Your criterion. -->

I will submit 11 appeals: 6 valid new appeals, 2 repeat appeals on an ID that is already under review, 2 appeals with a `content_id` that doesn't exist, and 1 appeal with empty `reasoning`. This must hold in all three test trials:

- Every valid new appeal returns 200 with status `under_review` and adds exactly one entry to `logs/audit.jsonl`.
- Every repeat appeal returns 200 and adds no new log entry.
- Every unknown ID returns 404 and adds nothing to the log.
- The empty-`reasoning` appeal returns 400 and adds nothing to the log.

That is 11 of 11, with no exceptions. A single miss in any trial counts as a miss.

**Why this target:**

An appeal is the only recourse a wrongly accused writer has. If one is silently lost, they have no defense, so this is one of the few places where anything below 100% is not acceptable. Repeat, fake and empty appeals must not touch the log, so it stays an honest record and can't be spammed or corrupted.

---

## 5. Bad input

<!-- Your criterion. -->

I will send 8 inputs to `/submit`, and the results must hold in all three test trials:

- Missing `text` returns 400 `text_required`.
- Empty `text` returns 400 `text_required`.
- `text` of exactly 19 characters returns 400 `text_too_short`.
- `text` of exactly 1,601 characters returns 413 `text_too_long`.
- A 100,000-character `text` returns 413 `text_too_long`.
- Missing `creator_id` returns 400 `creator_id_required`.
- `text` of exactly 20 characters is accepted (200).
- `text` of exactly 1,600 characters is accepted (200).

Every error uses the same shape (`error` plus `message`), and none of the six bad inputs adds an entry to `logs/audit.jsonl`. After the bad inputs, one normal submission still returns a correct 200 answer. That is 8 of 8, plus the normal check, with no exceptions. A single miss in any trial counts as a miss.

**Why this target:**

Bad input is where a service usually breaks, and the edges (19 vs 20, 1,600 vs 1,601) are where bugs hide. A rejected submission must not get a record, or an appeal could point at something that was never judged. Testing the exact boundaries and one enormous text shows the limits are enforced and that bad input can't crash the service.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
