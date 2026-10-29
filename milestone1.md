# Milestone 1 — Trace a submission before building one

Planning notes only. No code. Scores in the false-positive trace are illustrations, not measured results — real numbers come from the Milestone 4 calibration inputs.

---

## 1. The path a piece of text takes

**Step 1. Text arrives.** The writer sends `text` and `creator_id` to the `/submit` door.
- What it is: `submit()` in `app.py`.
- What it adds: the raw `text` and `creator_id`.
- Source: the `/submit` docstring in `app.py` ("Expects JSON").

**Step 2. The input is checked.** The system makes sure the text isn't missing, too short, or too long, so bad input doesn't crash it.
- What it is: the check at the top of `submit()` in `app.py`.
- What it adds: safety. A bad input gets a clear error instead of a crash.
- Source: the last paragraph of the `/submit` docstring ("what should this do when `text` is missing, empty, or enormous").

**Step 3. Both clues are measured.** The system runs two signals on the text.
- Clue 1: `model_signal()` in `detector.py` measures how predictable the words are. Adds `model_score`.
- Clue 2: `style_signal()` in `stylometry.py` measures the shape of the text (sentence length, word variety, punctuation). Adds `style_score`.
- Source: the Milestone 3 and 4 comments in `app.py`, the docstring of `detector.py`, and the "Where everything lives" table in `RUNNING.md`.

**Step 4. The clues are mixed.** The system blends the two scores into one.
- What it is: `combine_signals()` in `scoring.py`.
- What it adds: one combined score from 0 to 1. This is the `confidence` in the response.
- Source: the Milestone 4 comments in `app.py` and the docstring of `combine_signals`.

**Step 5. The score becomes words.** The system turns the number into a `guess` and a sentence a person can read.
- What it is: `score_to_label()` in `scoring.py`.
- What it adds: the `guess` ("ai", "human" or "unsure") and the `label` text.
- Source: the Milestone 5 comments in `app.py` and the docstring of `score_to_label`.

**Step 6. The decision is recorded.** The system makes the `content_id`, then writes it to the audit log with both scores, the combined score, the guess and the label.
- What it is: `log_decision()` in `audit.py`.
- What it adds: the `content_id`, plus a permanent record in `logs/audit.jsonl` so an appeal can find it later.
- Source: the Milestone 3 comments in `app.py`, the docstring of `log_decision`, and the "Where everything lives" table in `RUNNING.md`.

**Step 7. The reader sees the label.** The system sends the decision back.
- What it is: the `return` in `submit()` in `app.py`.
- What it adds: the JSON response with `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score`.
- Source: the `/submit` docstring ("Should return JSON with, at minimum").

---

## 2. The two signals

### Signal 1 — the model signal (`detector.py`, given)

- **Measures:** how predictable the text is. A language model on the laptop asks of each word, "could I have guessed that?" Score 0 to 1, higher means more likely AI.
- **Why it might differ between human and AI:** an AI writes by picking likely next words, so its text is easy for another model to predict. Human writing wanders more: odd word choices, abrupt turns, specific details.
- **Blind spot:** predictability is not authorship. It rewards common words in short, ordinary sentences, and plenty of real people write that way (second-language writers, younger writers, anyone writing plainly on purpose). That writing scores as machine-like as machine writing. It also fails the other way: dense, ornate prose full of rare words can score as human even if an AI wrote it.
- Source: docstring at the top of `detector.py`.

### Signal 2 — the style signal (`stylometry.py`, I build it)

- **Measures:** the shape of the text without understanding it: how much sentence lengths vary, how much vocabulary repeats, how much punctuation there is and how varied. Combined into one 0 to 1 score, higher means more likely AI.
- **Why it might differ between human and AI:** AI prose tends toward even, mid-length sentences and a narrower range of words. Human writing is lumpier, with a three-word sentence next to a forty-word one.
- **Blind spot:** it cannot read. It has no idea what the text means. Anything that changes the shape without changing the meaning fools it: typos, broken-up sentences, a pasted quotation. These are cheap to do on purpose, and unit 8's attack set will do them.
- Source: docstring at the top of `stylometry.py` and the "two blind spots" section of `RUNNING.md`.

### How the two blind spots relate

Signal 1 is fooled by plain, honest writing, which causes false accusations. Signal 2 is fooled by cheap tricks, which let AI text slip through. Each covers some of the other's weakness.

---

## 3. The false-positive trace

**The person:** Maria, a student who learned English as a second language. She writes her own essay in short, plain sentences with common words, because those are the words she's sure of.

1. She submits her essay to `/submit`. The input check passes.
2. Signal 1 finds it easy to predict, so `model_score` is high (illustration: 0.80). This is Signal 1's blind spot.
3. Signal 2 sees fairly even sentences and repeated simple words, so `style_score` is high too (illustration: 0.70).
4. Combined with the placeholder 50/50 weights in `config.py`: 0.5 × 0.80 + 0.5 × 0.70 = 0.75.
5. 0.75 is above `AI_THRESHOLD` (0.65), so the guess is "ai" and she gets the high-confidence AI label.
6. It's logged and she sees the label.

**What score did she get?** About 0.75 combined, with both signals wrong in the same direction. Nothing in the combining rule catches this.

**What did the label say?** The AI label. The text isn't written yet (`score_to_label` returns placeholders until Milestone 5). It must not sound like an accusation, because the reader may have written every word.

**What can she do?** Send `/appeal` with her `content_id` and her reasoning. This records the appeal and moves her item to `under_review`. Nothing is re-checked automatically.

**Why this decides the thresholds:** a higher `AI_THRESHOLD` accuses fewer people wrongly but lets more AI text through. A lower one catches more AI text but accuses more people like Maria. Because Maria has the least room to argue back, lean toward not accusing, and write down whichever way I lean.

---

## 4. Endpoint contracts

### `POST /submit`

**In (JSON):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | 20 to 1,600 characters |
| `creator_id` | string | yes | any non-empty string, not validated |

**Out, 200:**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | unique ID for this submission, needed for appeals |
| `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| `confidence` | number, 0 to 1 | the combined score; higher means more likely AI (so a low value with guess "human" means confidently human) |
| `label` | string | the plain sentence the writer reads |
| `model_score` | number, 0 to 1 | Signal 1's score |
| `style_score` | number, 0 to 1 | Signal 2's score |

**Out, errors** (all shaped `{"error": "...", "message": "..."}`):

| Case | Status | `error` |
|---|---|---|
| `text` missing or empty | 400 | `text_required` |
| `text` under 20 characters | 400 | `text_too_short` |
| `creator_id` missing | 400 | `creator_id_required` |
| `text` over 1,600 characters | 413 | `text_too_long` |
| model not downloaded | 503 | `detector_unavailable` |

### `POST /appeal`

**In (JSON):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `content_id` | string | yes | must exist in the audit log |
| `reasoning` | string | yes | why the writer says the label is wrong |

**Out, 200:**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | the same ID, echoed back |
| `status` | string | `"under_review"` |
| `message` | string | a confirmation the writer can read |

If the item is already `under_review`, the response has the same shape with a message saying it's already being reviewed. No second log entry is written.

**Out, errors** (same `error` + `message` shape):

| Case | Status | `error` |
|---|---|---|
| `content_id` not in the log | 404 | `content_id_not_found` |
| `reasoning` missing or empty | 400 | `reasoning_required` |

---

## 5. Decisions locked

- **Maximum length: 1,600 characters.** About 400 tokens, which matches `DETECTOR_MAX_TOKENS` in `config.py`, so nothing a writer sends is silently cut off.
- **Minimum length: 20 characters.** `detector.py` fails on fewer than 3 tokens.
- **Repeat appeals:** accepted with a calm "already under review" message, no duplicate log entry. Chosen because the person appealing may be wrongly accused and shouldn't see a scary error.
- **`creator_id`:** any non-empty string.
- **Errors:** one shape everywhere, `error` plus `message`.
- **Open:** exact threshold values and the final label wording, both settled in Milestones 4 and 5.

---

## 6. Read-back test

Could someone build against this without asking me a question? Questions the draft raised and how they were settled: maximum length (1,600), minimum length (20), repeat appeals (accept, no duplicate), what `creator_id` accepts (any non-empty string), what `confidence` means (combined score, higher is more AI), error shape (same everywhere).
