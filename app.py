#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import time  # CAPSTONE: a stopwatch for timing /submit handler runs
import uuid

from flask import Flask, jsonify, request

import audit
import config

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

def make_preview(text, limit=40):
    """
    CAPSTONE: make a short, safe-to-read preview of the submitted text, for
    the audit log. It is NOT anonymised: a name inside the first 40
    characters would still show up, so only made-up test text is used.

    Step 1: text[:limit] keeps only the first 40 characters, so we never
    store a whole essay in the log.

    Step 2: we go through those characters one at a time. If a character can
    be displayed normally (a letter, number, space or punctuation mark) we
    keep it. If it can't (a line break, a tab, an invisible character) we
    swap it for a plain space. That keeps the preview on one readable line.

    Step 3: "".join(...) glues the characters back into one short piece of text.
    """
    return "".join(ch if ch.isprintable() else " " for ch in text[:limit])


@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """
    # CAPSTONE: press "start" on the stopwatch when our /submit code begins.
    # We read it again just before the log line is written, to see how long
    # our code spent working on this submission.
    start = time.perf_counter()

    # CAPSTONE: give this visit its own unique ticket number. Every log line
    # for this request carries it, so we can find it later. It is separate
    # from content_id, which labels a submission that can be appealed.
    request_id = str(uuid.uuid4())

    payload = request.get_json(silent=True) or {}

    # ══ UNIT 8, MILESTONE 5: CHECK THE REQUEST BEFORE USING IT ═══════════════
    # In plain words: this function is the "front door" of the service. Before
    # this change, the door let almost anything in, and some requests made the
    # service crash. Now the door checks every request first, and politely
    # turns away anything that isn't usable, with a short message saying why.
    # Every turned-away request is also written in the audit log, so a refusal
    # never disappears without a trace.
    #
    # CHECK 1 — is the request the right shape?
    # A request should be a labelled form with `text` and `creator_id` on it
    # (programmers call this a "JSON object"). If someone sends something else,
    # like a bare list, the lines below would crash trying to read it. That is
    # exactly what happened with attack RQ07. So we stop it here.
    if not isinstance(payload, dict):
        audit.log_rejection(
            creator_id="unknown",
            reason="invalid_request",
            request_id=request_id,  # CAPSTONE: the ticket number for this visit
            # CAPSTONE: there is no usable text in this kind of request, so the
            # preview stays empty (null). The field is still written, so every
            # record has the same fields.
            input_preview=None,
            # CAPSTONE: how long our /submit code ran before turning this away
            duration_ms=round((time.perf_counter() - start) * 1000),
        )
        return jsonify({
            "error": "invalid_request",
            "message": "Please send a JSON object with text and creator_id.",
        }), 400

    # TODO: delete this and build the route.

    # Milestone 3, step 3: wire in the first signal.
    import detector
    import scoring
    import stylometry

    text = payload.get("text", "")
    creator_id = payload.get("creator_id")

    # Refuse missing, empty or non-string text before it reaches the model.
    if not isinstance(text, str) or not text.strip():
        audit.log_rejection(
            creator_id=creator_id or "unknown",
            reason="missing_or_empty_text",
            request_id=request_id,  # CAPSTONE: the ticket number for this visit
            # CAPSTONE: here `text` might be missing, a number, a list or an
            # empty string. We only make a preview when it really is text.
            # Otherwise we write null, so the field is still there.
            input_preview=make_preview(text) if isinstance(text, str) else None,
            # CAPSTONE: how long our /submit code ran before turning this away
            duration_ms=round((time.perf_counter() - start) * 1000),
        )
        return jsonify({
            "error": "text_required",
            "message": "Please send some writing to check.",
        }), 400

    # CHECK 2 — do we know who sent it?
    # Every submission must say who it is from (`creator_id`), because the
    # rate limit, the audit log and the appeal process all depend on knowing
    # that. If it is missing, blank or not a piece of text, we turn it away.
    # `log_creator` is just the name we write in the log: the real name if
    # there is a usable one, otherwise the word "unknown", so that something
    # odd (like a whole object sent as a name) never gets copied into the log.
    log_creator = creator_id if isinstance(creator_id, str) and creator_id.strip() else "unknown"

    if not isinstance(creator_id, str) or not creator_id.strip():
        audit.log_rejection(
            creator_id=log_creator,
            reason="creator_id_required",
            request_id=request_id,  # CAPSTONE: the ticket number for this visit
            # CAPSTONE: the first 40 characters of what came in, cleaned up so
            # it stays on one line. Safe here because the text check above has
            # already confirmed that `text` is real, non-empty text.
            input_preview=make_preview(text),
            # CAPSTONE: how long our /submit code ran before turning this away
            duration_ms=round((time.perf_counter() - start) * 1000),
        )
        return jsonify({
            "error": "creator_id_required",
            "message": "Please tell us who is submitting this writing.",
        }), 400

    # CHECK 3 — is the writing long enough to judge?
    # The detector needs a few words to work with. A single letter crashed it
    # (attack MF02), and very little text can't be judged fairly anyway, so
    # anything under 20 characters is turned away. We count the text exactly
    # as sent, spaces included, so text of exactly 20 characters is accepted.
    if len(text) < 20:
        audit.log_rejection(
            creator_id=log_creator,
            reason="text_too_short",
            request_id=request_id,  # CAPSTONE: the ticket number for this visit
            # CAPSTONE: the first 40 characters of what came in, cleaned up so
            # it stays on one line. Safe here because the checks above have
            # already confirmed that `text` is real text.
            input_preview=make_preview(text),
            # CAPSTONE: how long our /submit code ran before turning this away
            duration_ms=round((time.perf_counter() - start) * 1000),
        )
        return jsonify({
            "error": "text_too_short",
            "message": "Please send at least 20 characters of writing.",
        }), 400

    # CHECK 4 — is the writing short enough?
    # The detector only reads roughly the first 400 word-pieces of any text
    # and ignores the rest, so accepting a huge text would mean pretending to
    # judge something we mostly never looked at (attacks MF05 and MF08). So
    # anything over 1,600 characters is turned away. The reply code is 413,
    # the standard code for "too large".
    if len(text) > 1600:
        audit.log_rejection(
            creator_id=log_creator,
            reason="text_too_long",
            request_id=request_id,  # CAPSTONE: the ticket number for this visit
            # CAPSTONE: the first 40 characters of what came in, cleaned up so
            # it stays on one line. Only 40 are kept, so a huge text does not
            # fill the log. Safe because `text` is confirmed to be real text.
            input_preview=make_preview(text),
            # CAPSTONE: how long our /submit code ran before turning this away
            duration_ms=round((time.perf_counter() - start) * 1000),
        )
        return jsonify({
            "error": "text_too_long",
            "message": "Please send no more than 1,600 characters at a time.",
        }), 413
    # ══ END OF THE NEW CHECKS — the code below is unchanged ═══════════════════

    model_score = detector.model_signal(text)
    # Milestone 4: second signal, then combine the two into one score.
    style_score = stylometry.style_signal(text)
    combined_score = scoring.combine_signals(model_score, style_score)
    # Milestone 5: turn the combined score into a guess and a label.
    guess, label = scoring.score_to_label(combined_score)
    content_id = str(uuid.uuid4())

    # Milestone 3, step 4: write this submission to the audit log.
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        label=label,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        status="decided",
        request_id=request_id,  # CAPSTONE: the ticket number for this visit
        # CAPSTONE: the first 40 characters of what came in, cleaned up so it
        # stays on one line. We call it only here, after the checks above have
        # confirmed that `text` is real text.
        input_preview=make_preview(text),
        # CAPSTONE: "stop" the stopwatch and save the time our /submit code
        # spent on this submission, up to the moment just before this log line
        # is written. This is not the full round trip: it leaves out the time
        # Flask takes to receive the request and to send the reply.
        # We take the time now minus the start time (in seconds), multiply by
        # 1000 to get milliseconds, and round it to a whole number.
        duration_ms=round((time.perf_counter() - start) * 1000),
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined_score,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
    }), 200


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    payload = request.get_json(silent=True) or {}

    # TODO: delete this and build the route.

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({
            "error": "reasoning_required",
            "message": "Please tell us why you think this label is wrong.",
        }), 400

    entries = audit.entries_for(content_id) if content_id else []
    if not entries:
        return jsonify({
            "error": "content_id_not_found",
            "message": "We couldn't find that submission. Please check the ID.",
        }), 404

    already_under_review = any(e.get("status") == "under_review" for e in entries)
    if already_under_review:
        return jsonify({
            "content_id": content_id,
            "status": "under_review",
            "message": "Your appeal is already being reviewed. Thank you for your patience.",
        }), 200

    original = entries[0]
    audit.log_appeal(
        content_id=content_id,
        creator_id=original.get("creator_id"),
        reasoning=reasoning.strip(),
    )

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Thank you. Your appeal has been recorded and your writing is now under review.",
    }), 200


# ── Stretch: one item's current status ────────────────────────────────────────

@app.get("/content/<content_id>")
def get_content(content_id):
    """The current status of one submission: 'decided' or 'under_review'."""
    entries = audit.entries_for(content_id)
    if not entries:
        return jsonify({
            "error": "content_id_not_found",
            "message": "We couldn't find that submission. Please check the ID.",
        }), 404

    return jsonify({
        "content_id": content_id,
        "status": entries[-1].get("status"),
    }), 200


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
