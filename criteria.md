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


---

# 🔒 CAPSTONE CRITERIA — Unit 9

**Extension:** better logging on `/submit` (Shape A, local run, Path B).
The five criteria above this line are from Unit 8 and stay as they were.
These five were written **before** I ran any capstone trials. All inputs are made up.

## Capstone criterion 1. Bad input gets the right reply and exactly one log record

**Do:** send these six requests one at a time to `/submit`. Count the lines in
`logs/audit.jsonl` before and after each one.

| Request body | Expected reply | Expected log `reason` |
|---|---|---|
| `["not an object"]` | 400, error `invalid_request` | `invalid_request` |
| `{"creator_id":"c1"}` (no text) | 400, error `text_required` | `missing_or_empty_text` |
| `{"creator_id":"c2","text":""}` | 400, error `text_required` | `missing_or_empty_text` |
| `{"text":"This text has no creator attached to it."}` | 400, error `creator_id_required` | `creator_id_required` |
| `{"creator_id":"c3","text":"Nineteen characters"}` (19 characters) | 400, error `text_too_short` | `text_too_short` |
| `{"creator_id":"c4","text":"a" repeated 1,601 times}` | 413, error `text_too_long` | `text_too_long` |

**Target:** **6 of 6** requests add exactly **one** log line, with the expected
`reason`, `outcome` "rejected", and an `http_status` equal to the status of the reply.

**Why this target:** 20 and 1,600 characters are this service's real limits, so
19 and 1,601 test the edges. Six of six, because each is a separate code path that
can be wrong on its own. A log that disagrees with the reply sends an investigator
the wrong way.

## Capstone criterion 2. A creator ID that is not text is stored as text

**Do:** send five requests with empty text and these `creator_id` values: an object
`{"id":"x"}`, a list `["a"]`, the number `123`, `null`, and an empty string `""`.
Read the `creator_id` field in each new log line.

**Target:** **5 of 5** log lines have `creator_id` as a text string.

**Why this target:** audit records should have predictable field types, so anyone
or any program reading them knows what to expect. **I already expect this to miss.**
In the empty-text path, the code logs `creator_id` as it was sent. I saw an object
stored there in my real log earlier. I'm keeping the criterion because it's a real
inconsistency that I want to diagnose and fix, not a surprise.

## Capstone criterion 3. The sixth request in a minute is blocked, and recorded

**Do:** send one valid request from `warmup_rl` to load the model. Then run **3
trials**. In each trial, use a **new** creator ID (`rl_trial_1`, `rl_trial_2`,
`rl_trial_3`) and send six valid requests within one minute, using this text:
`Today I tested the service with a short sample. It should return a score and a label.`

**Target:** in **3 of 3** trials, requests 1 to 5 return 200, and request 6 returns
**429** with error `rate_limited`. Its log line has `reason` "rate_limited",
`http_status` 429, `outcome` "rejected", a non-empty `request_id`, and a
whole-number `duration_ms`.

**Why this target:** the limit is 5 a minute per creator (`config.py`), so the sixth
request is the edge. A blocked request that leaves no record would look like a quiet
afternoon, so the record matters as much as the 429.

## Capstone criterion 4. A scoring crash gives a safe error and an error record

**Do:** run `python test_scoring_error.py` 3 times. The test makes the scoring
function crash with the message "secret internal detail", sends a made-up
submission, and checks a temporary log.

**Target:** **3 of 3** runs pass. That means the reply is 500 with error
`scoring_error` and does not contain "secret internal detail"; the log has exactly one
record with `outcome` "error", `http_status` 500 and an `error_type`; and the message
is not in the log.

**Why this target:** a leaked error message shows internal details to the caller,
and a crash with no record is invisible to whoever runs the service. This criterion
is deterministic, so I expect 3 of 3.

## Capstone criterion 5. The preview is cleaned and cut to 40 characters

**Do:** send these five made-up texts, each with its own `creator_id`, and read
`input_preview` in each new log line.

| Text (JSON) | Expected `input_preview` |
|---|---|
| `"First line of a test.\nSecond line, still made up text here."` | `First line of a test. Second line, still` |
| `"Column one\tcolumn two\tcolumn three and then some more words here."` | `Column one column two column three and t` |
| `"Alert\u0007 character inside this made up sample sentence for testing."` | `Alert  character inside this made up sam` |
| `"Before the separator after the separator and a few more words."` | `Before the separator after the separator` |
| `"abcdefghij"` repeated 10 times (100 letters) | `abcdefghijabcdefghijabcdefghijabcdefghij` |

**Target:** **5 of 5** previews equal the expected text **exactly**.

**Why this target:** an exact match, because a "no control characters and at most
40 characters" check would pass even if the preview were empty. The log is meant to
show what came in on one readable line. The preview is not anonymised, so only
made-up text is used.
