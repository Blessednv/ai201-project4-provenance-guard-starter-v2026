# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 20:56
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `a2415fb2-ba1a-4b01-96f7-a8334c2d0f35` | human | 0.282 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `a7dd0739-2b61-4ab6-84f9-0f6dd6318515` | unsure | 0.388 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `1627cf39-abc6-4777-9fa9-477585e853c2` | unsure | 0.491 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `66dba473-9298-48f5-a05c-5205533ea7f5` | unsure | 0.503 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `805295b5-3830-4cc4-8306-78207ba3f0b9` | human | 0.321 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `f2ec530b-1d77-426b-b11c-7b1d840bfcab` | unsure | 0.364 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `566d96b5-36df-4a6e-86fc-e55dfd8ece4a` | unsure | 0.581 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `5b48c2fe-8d7d-4ba9-b846-b472e63c26a3` | human | 0.242 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `3b03b36c-ebb9-4730-8189-2cc0bdf575ff` | unsure | 0.511 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ffa31589-4590-4d06-ae1b-350c3f6ffe6d` | ai | 0.704 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `85e1fd1c-2de0-4160-b893-a55cac2f31e3` | unsure | 0.471 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `b9e3ef55-8ee9-4ecc-b476-f85290fa5315` | unsure | 0.559 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `35360580-537d-4295-bfdd-f29f4c1fdf78` | unsure | 0.561 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `954c4125-1c2a-4d51-b138-e34959228bc0` | unsure | 0.570 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `59de1732-880d-46fd-9c2a-df6ddf434911` | unsure | 0.622 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `446aba2d-79db-49e8-bfef-9fa998950474` | unsure | 0.582 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `f66489bf-ff4b-423f-a11b-0c53b38867ea` | unsure | 0.614 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `07d8014e-154e-4ad6-8301-b747e588e365` | human | 0.256 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c69a763b-6a67-414d-9436-0b6d98d725dc` | human | 0.299 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `81c26ca8-1f34-4e11-9ce0-839814b68e32` | human | 0.217 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c53a5247-efca-4295-88fa-7d472781896f` | unsure | 0.442 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `9e05fb37-f895-46ee-abb4-1e48964c98a1` | unsure | 0.417 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `2a6140b8-e05a-481b-a468-a534af0eef2b` | unsure | 0.580 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `51e0eb6c-d9a0-4925-8fa4-6d7e23d4a15b` | unsure | 0.436 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `b81c7d77-ecdf-480a-bb56-82b63f74808b` | human | 0.083 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `fca5a3f1-9893-45cd-b5d6-20012e551b10` | human | 0.172 | HELD |
| MF05 | malformed | text is a very long single word | 413 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 200 | `2bff5773-0e71-49de-b5bb-8680bcb70273` | ai | 0.665 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `f27733d9-194a-4c0b-b3ff-917458af9378` | unsure | 0.620 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b16eb1c0-bca3-4144-8618-bb30c056faea` | human | 0.098 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2b0505bc-04f7-46b1-9c4e-2e21117f9384` | human | 0.098 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7dadae11-ba13-40b1-adda-212c5acf243f` | human | 0.098 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `80ce157f-4681-4719-a495-9874d6d93fe8` | human | 0.098 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6bfb0bcf-f1c7-4c05-8bd6-adbf4b19d6fb` | human | 0.098 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "a2415fb2-ba1a-4b01-96f7-a8334c2d0f35",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2824,
  "model_score": 0.1635,
  "style_score": 0.4013,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "a7dd0739-2b61-4ab6-84f9-0f6dd6318515",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3883,
  "model_score": 0.5943,
  "style_score": 0.1822,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "1627cf39-abc6-4777-9fa9-477585e853c2",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4911,
  "model_score": 0.6662,
  "style_score": 0.316,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "66dba473-9298-48f5-a05c-5205533ea7f5",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5035,
  "model_score": 0.6114,
  "style_score": 0.3955,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "805295b5-3830-4cc4-8306-78207ba3f0b9",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3211,
  "model_score": 0.3212,
  "style_score": 0.321,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "f2ec530b-1d77-426b-b11c-7b1d840bfcab",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3642,
  "model_score": 0.5727,
  "style_score": 0.1558,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "566d96b5-36df-4a6e-86fc-e55dfd8ece4a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5809,
  "model_score": 0.5862,
  "style_score": 0.5756,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "5b48c2fe-8d7d-4ba9-b846-b472e63c26a3",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.2422,
  "model_score": 0.2452,
  "style_score": 0.2391,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "3b03b36c-ebb9-4730-8189-2cc0bdf575ff",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5109,
  "model_score": 0.7042,
  "style_score": 0.3175,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "ffa31589-4590-4d06-ae1b-350c3f6ffe6d",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7038,
  "model_score": 0.9792,
  "style_score": 0.4285,
  "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "85e1fd1c-2de0-4160-b893-a55cac2f31e3",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4707,
  "model_score": 0.6175,
  "style_score": 0.3239,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "b9e3ef55-8ee9-4ecc-b476-f85290fa5315",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5589,
  "model_score": 0.7387,
  "style_score": 0.3791,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "35360580-537d-4295-bfdd-f29f4c1fdf78",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5607,
  "model_score": 0.8051,
  "style_score": 0.3163,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "954c4125-1c2a-4d51-b138-e34959228bc0",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5702,
  "model_score": 0.8329,
  "style_score": 0.3075,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "59de1732-880d-46fd-9c2a-df6ddf434911",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6216,
  "model_score": 0.8005,
  "style_score": 0.4427,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "446aba2d-79db-49e8-bfef-9fa998950474",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5824,
  "model_score": 0.8814,
  "style_score": 0.2835,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f66489bf-ff4b-423f-a11b-0c53b38867ea",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6137,
  "model_score": 0.8816,
  "style_score": 0.3458,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "07d8014e-154e-4ad6-8301-b747e588e365",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.3223,
  "style_score": 0.189,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c69a763b-6a67-414d-9436-0b6d98d725dc",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2986,
  "model_score": 0.4625,
  "style_score": 0.1347,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "81c26ca8-1f34-4e11-9ce0-839814b68e32",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.217,
  "model_score": 0.2044,
  "style_score": 0.2295,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c53a5247-efca-4295-88fa-7d472781896f",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.442,
  "model_score": 0.5943,
  "style_score": 0.2897,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "9e05fb37-f895-46ee-abb4-1e48964c98a1",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4169,
  "model_score": 0.4998,
  "style_score": 0.334,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "2a6140b8-e05a-481b-a468-a534af0eef2b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5803,
  "model_score": 0.6401,
  "style_score": 0.5206,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "51e0eb6c-d9a0-4925-8fa4-6d7e23d4a15b",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4363,
  "model_score": 0.5583,
  "style_score": 0.3142,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "b81c7d77-ecdf-480a-bb56-82b63f74808b",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.0833,
  "model_score": 0.0,
  "style_score": 0.1667,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "fca5a3f1-9893-45cd-b5d6-20012e551b10",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.1722,
  "model_score": 0.0112,
  "style_score": 0.3333,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "2bff5773-0e71-49de-b5bb-8680bcb70273",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6651,
  "model_score": 0.9969,
  "style_score": 0.3333,
  "label": "We think AI tools may have been used to help write this, but we could be wrong. If this doesn't match how you wrote it, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "f27733d9-194a-4c0b-b3ff-917458af9378",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6199,
  "model_score": 0.9064,
  "style_score": 0.3333,
  "label": "The result isn't clear. We can't tell for sure whether this was written by a person or with AI tools. If you'd like us to take another look, you can submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "b16eb1c0-bca3-4144-8618-bb30c056faea",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0977,
  "model_score": 0.0287,
  "style_score": 0.1667,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "2b0505bc-04f7-46b1-9c4e-2e21117f9384",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0977,
  "model_score": 0.0287,
  "style_score": 0.1667,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "7dadae11-ba13-40b1-adda-212c5acf243f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0977,
  "model_score": 0.0287,
  "style_score": 0.1667,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "80ce157f-4681-4719-a495-9874d6d93fe8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0977,
  "model_score": 0.0287,
  "style_score": 0.1667,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "6bfb0bcf-f1c7-4c05-8bd6-adbf4b19d6fb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0977,
  "model_score": 0.0287,
  "style_score": 0.1667,
  "label": "Thank you for sharing your writing. It looks like it was written by a real person, and that's great to see.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
