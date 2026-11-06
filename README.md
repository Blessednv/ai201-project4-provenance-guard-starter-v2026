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

1. A writer sends their text and a `creator_id` to the `/submit` route.
2. The **Math Robot** (the model signal, `detector.py`) reads the text and scores how predictable the words are.
3. The **Counting Machine** (the style signal, `stylometry.py`) ignores the meaning and measures the shape of the text: sentence length spread, word variety in the first 100 words, and punctuation density.
4. The **combining rule** (`scoring.py::combine_signals`) takes a plain 50/50 average of the two scores to make one final number from 0 to 1.
5. `score_to_label` turns that number into one of three labels: high-confidence human (below 0.35), unsure (0.35 to 0.65) or high-confidence AI (above 0.65), written in plain English.
6. The decision is recorded in `logs/audit.jsonl`: the `content_id`, the writer, both signal scores, the combined score, the guess, the label and the status.
7. The writer gets the label back with the `content_id`. If they disagree, they can use `/appeal` to ask for a review. That records their reason and sets the status to `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the words are. A language model (`gpt2`, running on my own computer) reads the text and I measure how surprised it is by each word. The result is a score from 0 to 1, and higher means more likely AI.

**Why that might differ between human and AI writing:** An AI writes by picking likely next words, so its text is easy for another model to predict. Human writing wanders more, with odd word choices, sudden turns and specific details, so it surprises the model more.

**What it can't see:** It can't see who wrote the text. It only sees how guessable the words are. Plain, simple writing is easy to guess, so it scores as machine-like even when a person wrote it. My plain human stone text ("The stone is very pretty. I like the light color...") scored 0.73. That could also affect people writing in a second language, or anyone who writes plainly on purpose. It also fails the other way: a lightly-edited AI text scored 0.35, in the human range, because the edits made the words less predictable.

### Signal two — the style signal

**What it measures:** The shape of the text, without understanding a word. It combines three measures into one score from 0 to 1, where higher means more likely AI: how much sentence lengths vary, how many different words are used in the first 100 words, and how many commas, semicolons, colons and dashes there are per word. The three count equally in the average. In practice the word-variety measure barely changed on my short test texts (0.83 to 1.00), so it did little to separate them.

**Why that might differ between human and AI writing:** AI writing tends toward even, mid-length sentences and a narrower range of words, because that's what "most likely next word" produces on average. Human writing is lumpier, with a three-word sentence next to a forty-word one.

**What it can't see:** It can't read, so it has no idea what the text says. Anything that changes the shape without changing the meaning moves it, such as adding typos, breaking up sentences or pasting in a quotation. That's cheap to do on purpose. It is also unreliable on short texts: with only one sentence it can't measure spread at all and returns "can't tell" (0.5), and my short, plain human stone text scored 0.83 on sentence-length spread, as if it were machine-neat. Its overall scores also stayed in a narrow band (0.28 to 0.51 on my five test texts), so on its own it's a mild hint, not a strong judge.

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

**Moment 1: the label for human writing**

- *What I asked for:* My project shows a short message to a writer after it checks their text. I asked the AI to help me write the message for text that looks like it was written by a person.
- *What came back:* The AI gave me "We think this was probably written by a person." It was accurate, but it sounded cold, like a machine reading out a measurement. I realized I wouldn't want to receive that message about my own writing.
- *What I changed:* I told the AI I wanted something more positive, encouraging and kind. I chose this version: "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see."

**Moment 2: a suggestion I didn't use**

- *What I asked for:* I asked a second AI window to improve my message for the case where the system can't tell who wrote the text. I wanted a second opinion on the wording.
- *What came back:* It suggested saying "we give the writer the benefit of the doubt." It sounded kind at first, and the rest of its feedback was useful.
- *What I changed:* I decided not to use that sentence. "Benefit of the doubt" quietly says "we suspected you and let it go," so someone who wrote every word themselves might feel accused. I kept a version that says honestly that the result isn't clear.

**Moment 3: reading my messages like a stranger**

- *What I asked for:* I asked an AI to read my three messages as if it were a writer who had received them on its own work. I asked it to say what it would think and what it would do next, and I told it not to rewrite them.
- *What came back:* It said the "AI" message sounded like an accusation, and that it left out people who only used a tool a little, like a grammar checker. It also said my "can't tell" message gave the writer nothing to do next, and that the line "nothing is wrong with your writing" could make someone wonder if something was wrong.
- *What I changed:* The "can't tell" message now says "The result isn't clear" and offers an appeal, so the writer isn't left stuck. The "AI" message now says "If this doesn't match how you wrote it, please submit an appeal," which covers people who used a tool only a little.

**Moment 4: choosing test texts I could trust**

- *What I asked for:* I wanted four test texts to check my system: one clearly AI, one clearly human, one formal human, and one AI text with small human-looking edits. I knew the test would only mean something if I was sure who wrote each one.
- *What came back:* The AI wrote me example texts, and another window gave me a different pair. Before using them, I was asked who wrote the "formal human" one, because it only counts as human if a person wrote it.
- *What I changed:* I used the formal text that I wrote myself, so it was truly human. When the edited AI text scored like human writing, I decided not to change my rule just to fix four examples, and wrote it down as a known weakness instead.

---

## Stretch Features

**Declared before building: a `GET /content/<id>` endpoint (+1 pt).**

I am adding one stretch feature: a `GET /content/<id>` route in `app.py`. A writer who has a `content_id` can ask what is happening with their writing. The route looks up the `content_id` with `audit.entries_for`, and returns the item's current status, which is `decided` at first and `under_review` after an appeal. It only reads the log and never writes to it. If the `content_id` doesn't exist, it returns a 404 with the same `error` and `message` shape as my other routes.

**What it changed:** Before this, a writer could send text and get a label (`/submit`), or appeal a label (`/appeal`), but could not ask what was happening with their writing. Now a writer with a `content_id` can check its current status at any time. It only reads the log, so asking never changes anything, and a fake ID gets a clear 404 instead of a crash. I added one route in `app.py`, `get_content`, placed just above `/log`, and no other file changed.

**A request and the response it returns:**

An item I appealed earlier, so its newest log entry says `under_review`:

```bash
$ curl http://127.0.0.1:5000/content/54aa2188-ec2e-4f96-b4b9-d47397ce7617
```

```json
{
  "content_id": "54aa2188-ec2e-4f96-b4b9-d47397ce7617",
  "status": "under_review"
}
```

An item nobody appealed, so it is still `decided`:

```bash
$ curl http://127.0.0.1:5000/content/9b6ef075-2771-41b5-abab-26dfb5d3f1f1
```

```json
{
  "content_id": "9b6ef075-2771-41b5-abab-26dfb5d3f1f1",
  "status": "decided"
}
```

An ID that does not exist:

```bash
$ curl -i http://127.0.0.1:5000/content/not-a-real-id
```

```json
{
  "error": "content_id_not_found",
  "message": "We couldn't find that submission. Please check the ID."
}
```

This last one returns HTTP status `404 NOT FOUND`.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
A real writer submits a piece, reads the result, and maybe resubmits once or
twice, so 5 a minute doesn't bother them. 50 a day is far more than anyone
checking their own work needs. A script mapping my thresholds needs hundreds of
variations, so 50 a day slows it down a lot. Each submission also runs a local
model for 1–2 seconds, so a low per-minute cap protects the machine too.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->
Per `creator_id`, falling back to the IP address when there is none. The
weakness: a script can rotate creator IDs to get around the limit.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

Fifteen entries: twelve decisions and three rejections (two 400s, one 429).

```json
// EV01
{"timestamp": "2026-11-05T00:39:49+00:00", "content_id": "f9eed3e3-c8ef-469f-b9d7-3cd10b1443f2", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4013, "combined_score": 0.2824, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "status": "decided"}
// EV08
{"timestamp": "2026-11-05T00:39:50+00:00", "content_id": "baf320c1-fce5-45d6-aa8e-ffb1d9112694", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.2391, "combined_score": 0.2422, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "status": "decided"}
// EV07
{"timestamp": "2026-11-05T00:39:50+00:00", "content_id": "4804441a-b2b4-4d1b-830b-2385d612efb7", "creator_id": "attacker_EV07", "guess": "unsure", "model_score": 0.5862, "style_score": 0.5756, "combined_score": 0.5809, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "status": "decided"}
// EV10
{"timestamp": "2026-11-05T00:39:51+00:00", "content_id": "297f8e4b-9eb0-40f4-beff-908089b98468", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.4285, "combined_score": 0.7038, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "status": "decided"}
// PI01
{"timestamp": "2026-11-05T00:39:53+00:00", "content_id": "01116fe1-564c-48d1-a768-344a803ad609", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.1347, "combined_score": 0.2986, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "status": "decided"}
// PI02
{"timestamp": "2026-11-05T00:39:53+00:00", "content_id": "2cc70205-c60f-43c6-9330-8cbea0371013", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.2295, "combined_score": 0.217, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "status": "decided"}
// PI03
{"timestamp": "2026-11-05T00:39:53+00:00", "content_id": "4b347db4-5110-4885-875b-61387dbe3be7", "creator_id": "attacker_PI03", "guess": "unsure", "model_score": 0.5943, "style_score": 0.2897, "combined_score": 0.442, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "status": "decided"}
// MF06
{"timestamp": "2026-11-05T00:39:55+00:00", "content_id": "66880e94-bccb-46f2-b254-fa6bf60d11c5", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.3333, "combined_score": 0.6651, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "status": "decided"}
// MF08
{"timestamp": "2026-11-05T00:39:56+00:00", "content_id": "ec9ab212-c315-496d-9cd0-50648d037bcc", "creator_id": "attacker_MF08", "guess": "ai", "model_score": 0.9876, "style_score": 0.3337, "combined_score": 0.6606, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "status": "decided"}
// FP03
{"timestamp": "2026-11-05T00:39:52+00:00", "content_id": "da17da45-6b71-4afc-80a1-b0b58b9ab1d2", "creator_id": "attacker_FP03", "guess": "unsure", "model_score": 0.8051, "style_score": 0.3163, "combined_score": 0.5607, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "status": "decided"}
// FP05
{"timestamp": "2026-11-05T00:39:52+00:00", "content_id": "3a5ba326-76f4-4dfd-8c0d-4ab6194ca965", "creator_id": "attacker_FP05", "guess": "unsure", "model_score": 0.8005, "style_score": 0.4427, "combined_score": 0.6216, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "status": "decided"}
// RQ02
{"timestamp": "2026-11-05T00:39:57+00:00", "content_id": "84ce7bca-0745-48d0-a38c-d818e36fc798", "creator_id": null, "guess": "human", "model_score": 0.2395, "style_score": 0.1667, "combined_score": 0.2031, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "status": "decided"}
// MF01 (400)
{"timestamp": "2026-11-05T00:39:53+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "missing_or_empty_text"}
// RQ01 (400)
{"timestamp": "2026-11-05T00:39:56+00:00", "creator_id": "attacker_RQ01", "event": "rejected", "status": "rejected", "reason": "missing_or_empty_text"}
// 429 from the flood rows (FL01)
{"timestamp": "2026-11-05T00:39:57+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**1. MF08, a real writer called "ai".** The input was a person's camping-trip
writing, repeated up to about 60,000 characters. My service returned 200 with
guess `ai` (model score 0.99, style score 0.33, combined 0.661, just above my
0.65 line). A writer would be told their own work looks machine-made.

**2. FP03, an honest writer left under doubt.** The input was careful writing by
a non-native English speaker. My service returned `unsure` (model score 0.81,
style score 0.32, combined 0.56), so the writer is told we can't tell whether a
person or AI wrote it, and their only way out is an appeal. This is the person
least able to argue back.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | **MET** |
| 2. Score spread (AI avg minus human avg) | ≥ 0.3 | gap 0.134 | gap 0.134 | gap 0.134 | **MISSED** |
| 3. Label coverage | all 3 labels appear, "unsure" at least twice | no "human" (0 human, 11 unsure, 4 ai) | same | same | **MISSED** |
| 4. Appeal path | 11 of 11 | 11/11 | 11/11 | 11/11 | **MET** |
| 5. Bad input | 8 of 8 + normal check | 4/8 (+ normal OK) | 4/8 (+ normal OK) | 4/8 (+ normal OK) | **MISSED** |

Notes:
- All three trials were identical for every criterion, as expected, because neither signal is random.
- Criterion 1, trial 1: the first piece timed out once at 90 seconds (a slow first request). The same text scored fine in the other runs.
- Criterion 4 was not run through `run_eval.py`, because it only sends `POST /submit` and can't send appeals. I tested it with a separate script (not in this repo) that submitted 7 texts per trial, sent the 11 appeals, and counted the lines in `logs/audit.jsonl` before and after each appeal.
- Source: `results/run_2026-11-05_2008_before.md`, produced by `run_eval.py::main`.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

**Criterion 1: my own writing** · produced by `run_eval.py::main` (which POSTs to `app.py::submit`), saved in `results/run_2026-11-05_2008_before.md`, trial 2

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.4949, "model_score": 0.6012, "style_score": 0.3886, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "We have a delivery scheduled for tomorrow November 5th .\n\nAfter inform"},
  {"status": 200, "guess": "unsure", "confidence": 0.5458, "model_score": 0.6672, "style_score": 0.4244, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "At the 1st Client Site meeting, we mentioned that we would be travelin"},
  {"status": 200, "guess": "unsure", "confidence": 0.467, "model_score": 0.5639, "style_score": 0.3702, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I am learning how to build web servers in Python coding language. It h"},
  {"status": 200, "guess": "unsure", "confidence": 0.572, "model_score": 0.8445, "style_score": 0.2995, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "We are planning a trip to Hawaii next spring. I am really looking forw"},
  {"status": 200, "guess": "unsure", "confidence": 0.3738, "model_score": 0.3459, "style_score": 0.4016, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "Fixing this code bug took me three hours today. I kept missing a small"},
  {"status": 200, "guess": "unsure", "confidence": 0.5166, "model_score": 0.6942, "style_score": 0.3389, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "The stone is very pretty. I like the light color. It looks good in the"},
  {"status": 200, "guess": "unsure", "confidence": 0.6317, "model_score": 0.7634, "style_score": 0.5, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I need to buy milk, eggs, and bread from the grocery store."},
  {"status": 200, "guess": "unsure", "confidence": 0.5422, "model_score": 0.7468, "style_score": 0.3376, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "The weather is really nice today, so I might go for a walk."},
  {"status": 200, "guess": "unsure", "confidence": 0.4156, "model_score": 0.6645, "style_score": 0.1667, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I really enjoyed watching that movie last night."},
  {"status": 200, "guess": "unsure", "confidence": 0.48, "model_score": 0.7934, "style_score": 0.1667, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "My cat is sleeping on the couch right now."}
]
```

**Criterion 2: score spread** · produced by `run_eval.py::main` (which POSTs to `app.py::submit`), saved in `results/run_2026-11-05_2008_before.md`, trial 2

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.6581, "model_score": 0.7773, "style_score": 0.5389, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "Effective time management is essential for achieving both personal and"},
  {"status": 200, "guess": "ai", "confidence": 0.7266, "model_score": 0.9191, "style_score": 0.534, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "Climate change represents one of the most significant challenges facin"},
  {"status": 200, "guess": "ai", "confidence": 0.6533, "model_score": 0.885, "style_score": 0.4217, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "Artificial intelligence has the potential to transform numerous indust"},
  {"status": 200, "guess": "ai", "confidence": 0.7077, "model_score": 0.899, "style_score": 0.5165, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "A balanced diet plays a crucial role in maintaining overall health and"},
  {"status": 200, "guess": "unsure", "confidence": 0.5085, "model_score": 0.6093, "style_score": 0.4078, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "Remote work has become increasingly popular in recent years, offering "},
  {"status": 200, "guess": "unsure", "confidence": 0.5166, "model_score": 0.6942, "style_score": 0.3389, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "The stone is very pretty. I like the light color. It looks good in the"},
  {"status": 200, "guess": "unsure", "confidence": 0.6317, "model_score": 0.7634, "style_score": 0.5, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I need to buy milk, eggs, and bread from the grocery store."},
  {"status": 200, "guess": "unsure", "confidence": 0.5422, "model_score": 0.7468, "style_score": 0.3376, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "The weather is really nice today, so I might go for a walk."},
  {"status": 200, "guess": "unsure", "confidence": 0.4156, "model_score": 0.6645, "style_score": 0.1667, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I really enjoyed watching that movie last night."},
  {"status": 200, "guess": "unsure", "confidence": 0.48, "model_score": 0.7934, "style_score": 0.1667, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "My cat is sleeping on the couch right now."}
]
```

**Criterion 3: label coverage** · produced by `run_eval.py::main` (which POSTs to `app.py::submit`), saved in `results/run_2026-11-05_2008_before.md`, trial 2

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.4949, "model_score": 0.6012, "style_score": 0.3886, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "We have a delivery scheduled for tomorrow November 5th .\n\nAfter inform"},
  {"status": 200, "guess": "unsure", "confidence": 0.5458, "model_score": 0.6672, "style_score": 0.4244, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "At the 1st Client Site meeting, we mentioned that we would be travelin"},
  {"status": 200, "guess": "unsure", "confidence": 0.467, "model_score": 0.5639, "style_score": 0.3702, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I am learning how to build web servers in Python coding language. It h"},
  {"status": 200, "guess": "unsure", "confidence": 0.572, "model_score": 0.8445, "style_score": 0.2995, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "We are planning a trip to Hawaii next spring. I am really looking forw"},
  {"status": 200, "guess": "unsure", "confidence": 0.3738, "model_score": 0.3459, "style_score": 0.4016, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "Fixing this code bug took me three hours today. I kept missing a small"},
  {"status": 200, "guess": "unsure", "confidence": 0.5166, "model_score": 0.6942, "style_score": 0.3389, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "The stone is very pretty. I like the light color. It looks good in the"},
  {"status": 200, "guess": "unsure", "confidence": 0.6317, "model_score": 0.7634, "style_score": 0.5, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I need to buy milk, eggs, and bread from the grocery store."},
  {"status": 200, "guess": "unsure", "confidence": 0.5422, "model_score": 0.7468, "style_score": 0.3376, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "The weather is really nice today, so I might go for a walk."},
  {"status": 200, "guess": "unsure", "confidence": 0.4156, "model_score": 0.6645, "style_score": 0.1667, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I really enjoyed watching that movie last night."},
  {"status": 200, "guess": "unsure", "confidence": 0.48, "model_score": 0.7934, "style_score": 0.1667, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "My cat is sleeping on the couch right now."},
  {"status": 200, "guess": "ai", "confidence": 0.6581, "model_score": 0.7773, "style_score": 0.5389, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "Effective time management is essential for achieving both personal and"},
  {"status": 200, "guess": "ai", "confidence": 0.7266, "model_score": 0.9191, "style_score": 0.534, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "Climate change represents one of the most significant challenges facin"},
  {"status": 200, "guess": "ai", "confidence": 0.6533, "model_score": 0.885, "style_score": 0.4217, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "Artificial intelligence has the potential to transform numerous indust"},
  {"status": 200, "guess": "ai", "confidence": 0.7077, "model_score": 0.899, "style_score": 0.5165, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "A balanced diet plays a crucial role in maintaining overall health and"},
  {"status": 200, "guess": "unsure", "confidence": 0.5085, "model_score": 0.6093, "style_score": 0.4078, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "Remote work has become increasingly popular in recent years, offering "}
]
```

**Criterion 5: bad input** · produced by `run_eval.py::main` (which POSTs to `app.py::submit`), saved in `results/run_2026-11-05_2008_before.md`, trial 2

```json
[
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"creator_id\": \"eval_bad_missing\"}"},
  {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "(empty text)"},
  {"status": 200, "guess": "human", "confidence": 0.2099, "model_score": 0.003, "style_score": 0.4167, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "sent": "word word word word"},
  {"status": 200, "guess": "ai", "confidence": 0.747, "model_score": 0.9972, "style_score": 0.4967, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "word word word word word word word word word word word word word word "},
  {"status": 200, "guess": "ai", "confidence": 0.7471, "model_score": 0.9975, "style_score": 0.4967, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "word word word word word word word word word word word word word word "},
  {"status": 200, "guess": "unsure", "confidence": 0.5932, "model_score": 0.6863, "style_score": 0.5, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "{\"text\": \"I need to buy milk, eggs, and bread from the store.\"}"},
  {"status": 200, "guess": "human", "confidence": 0.2103, "model_score": 0.0038, "style_score": 0.4167, "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.", "sent": "word word word word "},
  {"status": 200, "guess": "ai", "confidence": 0.747, "model_score": 0.9972, "style_score": 0.4967, "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.", "sent": "word word word word word word word word word word word word word word "},
  {"status": 200, "guess": "unsure", "confidence": 0.6317, "model_score": 0.7634, "style_score": 0.5, "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.", "sent": "I need to buy milk, eggs, and bread from the grocery store."}
]
```

**Criterion 4: appeal path** · produced by a separate test script calling `app.py::appeal` (not `run_eval.py`), trial 1. `log_added` is how many lines `logs/audit.jsonl` grew by.

```json
[
  {"case": "valid new appeal 1", "status": 200, "log_added": 1, "body": {"content_id": "c9c2dfd6-ab23-4457-8686-1733f6752bbb", "message": "Thank you. Your appeal has been recorded and your writing is now under review.", "status": "under_review"}},
  {"case": "repeat appeal 1", "status": 200, "log_added": 0, "body": {"content_id": "c9c2dfd6-ab23-4457-8686-1733f6752bbb", "message": "Your appeal is already being reviewed. Thank you for your patience.", "status": "under_review"}},
  {"case": "unknown id 1", "status": 404, "log_added": 0, "body": {"error": "content_id_not_found", "message": "We couldn't find that submission. Please check the ID."}},
  {"case": "empty reasoning", "status": 400, "log_added": 0, "body": {"error": "reasoning_required", "message": "Please tell us why you think this label is wrong."}}
]
```
Of the 11 cases in each trial, these are one of each kind. All 11 matched the expected status and log change in all three trials.

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

**Audit log limitation:** the log records all nine required fields, but not the
signal weights or label thresholds in force at the time. Changing config.py
later makes older entries harder to interpret.



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
