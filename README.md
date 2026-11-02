# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### Signal two — the style signal

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** I take the average of the two signals. Each one counts the same. When the two signals disagree, the average lands in the middle, and the system calls the text "unsure" instead of guessing. I chose this because two methods disagreeing really is uncertainty, and I'd rather say "unsure" than accuse a writer on the word of one signal.

**The numbers:** combined score = 0.5 × model score + 0.5 × style score. The weights are `WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5`, both in `config.py`. Both signals run from 0 to 1, and higher means more likely AI.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

**Split case: the stone text.** *"The stone is very pretty. I like the light color. It looks good in the kitchen. We will use it for the counter."* I wrote this myself, so it is human. The model signal scored it **0.73**, which leans AI, because the words are plain and easy to guess. The style signal scored it **0.34**, which leans human, because the text has some punctuation and varied sentence lengths. The two signals point in opposite directions.

*What my rule does with it:* The stone text gets a model score of 0.73 and a style score of 0.34, so the combined score is 0.53. That falls in the middle, so the system calls it "unsure" and doesn't accuse the writer. The plain average turns a disagreement between the signals into uncertainty.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | below 0.35 | "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see." |
| unsure | 0.35 to 0.65 | "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal." |
| high-confidence AI | above 0.65 | "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person reading this may have written every word themselves, so it must not sound like an accusation. It starts by saying plainly that the result isn't clear, and it doesn't guess. It gives the writer a next step, the appeal, so they never feel stuck. It talks about the text, not the person, and it avoids technical words like "score" or "threshold."



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence is transforming the way we live and work. It offers numerous benefits, including increased efficiency, improved decision-making, and enhanced productivity. However, it is important to consider the ethical implications and ensure that these technologies are developed responsibly.", "creator_id": "maria"}'
```

```json
{
  "confidence": 0.6926,
  "content_id": "54aa2188-ec2e-4f96-b4b9-d47397ce7617",
  "guess": "ai",
  "label": "We think AI tools may have been used to help write this, but we could be wrong. If you wrote this yourself, please submit an appeal.",
  "model_score": 0.8759,
  "style_score": 0.5094
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "54aa2188-ec2e-4f96-b4b9-d47397ce7617", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{
  "content_id": "54aa2188-ec2e-4f96-b4b9-d47397ce7617",
  "message": "Thank you. Your appeal has been recorded and your writing is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=5"
```

```json
{
  "count": 5,
  "entries": [
    {
      "combined_score": 0.6926,
      "content_id": "a03da2f2-5003-488e-a048-8bdef6d6ce3b",
      "creator_id": "maria",
      "guess": "unsure",
      "label": null,
      "model_score": 0.8759,
      "status": "decided",
      "style_score": 0.5094,
      "timestamp": "2026-10-31T17:57:52+00:00"
    },
    {
      "combined_score": 0.6926,
      "content_id": "54aa2188-ec2e-4f96-b4b9-d47397ce7617",
      "creator_id": "maria",
      "guess": "ai",
      "label": "We think AI tools may have been used to help write this, but we could be wrong. If you wrote this yourself, please submit an appeal.",
      "model_score": 0.8759,
      "status": "decided",
      "style_score": 0.5094,
      "timestamp": "2026-10-31T19:08:55+00:00"
    },
    {
      "combined_score": 0.5339,
      "content_id": "9b6ef075-2771-41b5-abab-26dfb5d3f1f1",
      "creator_id": "maria",
      "guess": "unsure",
      "label": "We can't tell for sure whether this was written by a person or with AI tools. That doesn't mean anything is wrong with your writing.",
      "model_score": 0.7321,
      "status": "decided",
      "style_score": 0.3358,
      "timestamp": "2026-10-31T19:09:15+00:00"
    },
    {
      "combined_score": 0.3224,
      "content_id": "a2ce1d36-6b73-423d-a3ad-bc4d7370bf77",
      "creator_id": "maria",
      "guess": "human",
      "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
      "model_score": 0.2927,
      "status": "decided",
      "style_score": 0.3521,
      "timestamp": "2026-10-31T19:09:39+00:00"
    },
    {
      "content_id": "54aa2188-ec2e-4f96-b4b9-d47397ce7617",
      "creator_id": "maria",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment.",
      "status": "under_review",
      "timestamp": "2026-11-02T16:31:44+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
