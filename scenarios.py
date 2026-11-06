"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ── The texts ────────────────────────────────────────────────────────────────
# Ten pieces I wrote myself. Wording is exactly as I wrote it. Pieces 1-2 are
# emails, 3-5 are longer pieces, 6-10 are short ones.
MY_TEXTS = [
    "We have a delivery scheduled for tomorrow November 5th .\n\n"
    "After informing our doorman and building superintendent about the upcoming delivery, "
    "we were just notified that they will require a Certificate of Insurance (COI). \n\n"
    "You have delivered to us multiple times previously without needing one, the latest "
    "delivery was just last month, so this is a new requirement on their end. \n\n"
    "Could you please provide the necessary COI, so we can clear this with our building "
    "staff for tomorrow?",

    "At the 1st Client Site meeting, we mentioned that we would be traveling in March.\n\n"
    "We have now confirmed that will be traveling for business from March 15 - April 5th.\n\n\n"
    "With the above in mind, we propose Friday, March 14th at 11am (same time as previous) "
    "as the date for the 2nd Client Site Meeting.  \n"
    "This would allow us to review the progress right before we leave.",

    "I am learning how to build web servers in Python coding language. It has been a "
    "challenging but rewarding process. Yesterday, I finally got my API to return a "
    "successful response.",

    "We are planning a trip to Hawaii next spring. I am really looking forward to "
    "snorkeling and hiking around the island. It will be nice to escape the cold city "
    "weather for a few weeks.",

    "Fixing this code bug took me three hours today. I kept missing a small syntax error "
    "on line forty. Once I finally spotted it, the whole program ran perfectly.",

    "The stone is very pretty. I like the light color. It looks good in the kitchen.",
    "I need to buy milk, eggs, and bread from the grocery store.",
    "The weather is really nice today, so I might go for a walk.",
    "I really enjoyed watching that movie last night.",
    "My cat is sleeping on the couch right now.",
]

# The five short pieces of mine used for criterion 2 (the same five as MY_TEXTS 6-10).
MY_SHORT_FIVE = MY_TEXTS[5:]

# Five clearly AI-written texts, written for this test. These are AI, not mine.
AI_TEXTS = [
    "Effective time management is essential for achieving both personal and professional "
    "goals. By prioritizing tasks, setting clear deadlines, and minimizing distractions, "
    "individuals can significantly improve their productivity. Furthermore, regular "
    "reflection allows for continuous improvement and long-term success.",

    "Climate change represents one of the most significant challenges facing humanity "
    "today. Rising global temperatures contribute to extreme weather events, sea level "
    "rise, and loss of biodiversity. Addressing this issue requires coordinated action "
    "from governments, businesses, and individuals alike.",

    "Artificial intelligence has the potential to transform numerous industries, from "
    "healthcare to finance. By automating routine tasks and analyzing vast amounts of "
    "data, AI systems can enhance efficiency and support better decision-making. "
    "However, it is important to consider the ethical implications of these technologies.",

    "A balanced diet plays a crucial role in maintaining overall health and well-being. "
    "Incorporating a variety of fruits, vegetables, whole grains, and lean proteins "
    "provides the essential nutrients the body needs. Additionally, staying hydrated and "
    "limiting processed foods can further support long-term health.",

    "Remote work has become increasingly popular in recent years, offering flexibility "
    "and improved work-life balance. Organizations that embrace remote work can access a "
    "broader talent pool while reducing overhead costs. Nevertheless, maintaining strong "
    "communication and team cohesion remains essential for success.",
]


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": MY_TEXTS,
    },
    {
        # Criterion 2 (score spread): 5 clearly-AI texts and 5 of my own.
        "name": "score spread",
        "criterion": 2,
        "texts": AI_TEXTS + MY_SHORT_FIVE,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        # My criterion 3 uses the same mixed set of 15: my 10 plus 5 AI texts.
        "texts": MY_TEXTS + AI_TEXTS,
    },
    {
        "name": "bad input",
        "criterion": 5,
        # My criterion 5: 8 inputs at the edges, plus one normal check afterwards.
        "bodies": [
            {"creator_id": "eval_bad_missing"},                                   # no text -> 400 text_required
            {"text": "", "creator_id": "eval_bad_empty"},                         # empty -> 400 text_required
            {"text": ("word " * 4)[:19], "creator_id": "eval_bad_19"},            # 19 chars -> 400 text_too_short
            {"text": ("word " * 320) + "x", "creator_id": "eval_bad_1601"},       # 1,601 chars -> 413 text_too_long
            {"text": "word " * 20000, "creator_id": "eval_bad_100k"},            # 100,000 chars -> 413 text_too_long
            {"text": "I need to buy milk, eggs, and bread from the store."},      # no creator_id -> 400 creator_id_required
            {"text": "word " * 4, "creator_id": "eval_ok_20"},                   # exactly 20 chars -> 200
            {"text": "word " * 320, "creator_id": "eval_ok_1600"},               # exactly 1,600 chars -> 200
            {"text": "I need to buy milk, eggs, and bread from the grocery store.",
             "creator_id": "eval_bad_normal"},                                    # normal check afterwards -> 200
        ],
    },
    # A bad-input criterion looks like this. Uncomment and adjust if that's one
    # of your five — these are raw request bodies, sent exactly as written.
    #
    # {
    #     "name": "bad input",
    #     "criterion": 3,
    #     "bodies": [
    #         {"text": "", "creator_id": "eval_bad_empty"},
    #         {"creator_id": "eval_bad_missing"},          # no text field at all
    #         {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
    #         {"text": None, "creator_id": "eval_bad_null"},
    #     ],
    # },

    # TODO: add what your remaining criteria need.
    #
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
