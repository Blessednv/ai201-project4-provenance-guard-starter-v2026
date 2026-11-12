#!/usr/bin/env python3
"""
CAPSTONE: runs my five capstone criteria once. One run of this script is one
"trial". I run it three times (trial 1, 2, 3) and change NO code in between.

    python run_capstone_trials.py 1

The service must already be running in another terminal (python app.py).
Everything the script sends uses made-up text. It only ADDS lines to the real
log; it never deletes or changes any. The full results are saved in
results/capstone_trial_<n>.txt (never overwriting an older file).
"""

import json
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime
from pathlib import Path
from unittest import mock

import requests

import config

URL = "http://127.0.0.1:5000"
ROOT = Path(__file__).resolve().parent
LOG = config.AUDIT_LOG          # the real log (read only, plus the service adds lines)
WAIT_SECONDS = 65               # longer than the 1-minute rate-limit window

GOOD_TEXT = ("Today I tested the service with a short sample. "
             "It should return a score and a label.")
SECRET = "secret internal detail"

trial = sys.argv[1] if len(sys.argv) > 1 else "1"
run_id = uuid.uuid4().hex[:6]   # makes every creator ID new, so old requests never count

# ---- where the results go (never overwrite an older file) ----
results_dir = ROOT / "results"
results_dir.mkdir(exist_ok=True)
out_path = results_dir / f"capstone_trial_{trial}.txt"
if out_path.exists():
    out_path = results_dir / f"capstone_trial_{trial}_{datetime.now():%Y%m%d_%H%M%S}.txt"
# mode "x" refuses to overwrite an existing file
out_file = out_path.open("x", encoding="utf-8")


def say(text=""):
    """Print a line AND save it in the results file."""
    print(text)
    out_file.write(text + "\n")
    out_file.flush()


def cid(tag):
    """A brand-new creator ID, so the rate limit never sees the same one twice."""
    return f"{tag}_t{trial}_{run_id}"


def log_lines():
    return LOG.read_text(encoding="utf-8").splitlines() if LOG.exists() else []


def new_entries(before_count):
    """The log lines added since `before_count`, as dictionaries."""
    entries = []
    for line in log_lines()[before_count:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return entries


def new_raw_line(before_count):
    """The first new log line exactly as written, or a note if there is none."""
    lines = log_lines()[before_count:]
    return lines[0] if lines else "(no new log line)"


def post(body):
    return requests.post(f"{URL}/submit", json=body, timeout=120)


def wait(reason):
    say(f"   (waiting {WAIT_SECONDS} s so the per-address rate limit resets: {reason})")
    time.sleep(WAIT_SECONDS)


summary = {}

# ---------------- header: proof that nothing changed between trials ----------------
commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                        capture_output=True, text=True).stdout.strip()
say(f"CAPSTONE TRIAL {trial}   started {datetime.now():%Y-%m-%d %H:%M:%S}")
say(f"code version (git commit): {commit}")
try:
    requests.get(f"{URL}/health", timeout=10).raise_for_status()
except Exception as exc:
    say(f"The service is not answering at {URL}. Start it with: python app.py ({exc})")
    sys.exit(1)

wait("start of the trial")

# ============================ CRITERION 1 ============================
say("\n=== CRITERION 1: bad input gets the right reply and exactly one log record ===")
cases = [
    ("JSON list",        ["not an object"],                                        400, "invalid_request",     "invalid_request"),
    ("missing text",     {"creator_id": cid("c1")},                                400, "text_required",       "missing_or_empty_text"),
    ("empty text",       {"creator_id": cid("c2"), "text": ""},                    400, "text_required",       "missing_or_empty_text"),
    ("no creator",       {"text": "This text has no creator attached to it."},     400, "creator_id_required", "creator_id_required"),
    ("19 characters",    {"creator_id": cid("c3"), "text": "Nineteen characters"}, 400, "text_too_short",      "text_too_short"),
    ("1,601 characters", {"creator_id": cid("c4"), "text": "a" * 1601},             413, "text_too_long",       "text_too_long"),
]
passed = 0
for name, body, exp_status, exp_error, exp_reason in cases:
    before = len(log_lines())
    reply = post(body)
    entries = new_entries(before)
    problems = []
    if reply.status_code != exp_status:
        problems.append(f"reply status {reply.status_code}, expected {exp_status}")
    try:
        got_error = reply.json().get("error")
    except ValueError:
        got_error = None
    if got_error != exp_error:
        problems.append(f"reply error {got_error!r}, expected {exp_error!r}")
    if len(entries) != 1:
        problems.append(f"{len(entries)} new log lines, expected exactly 1")
    else:
        e = entries[0]
        if e.get("reason") != exp_reason:
            problems.append(f"log reason {e.get('reason')!r}, expected {exp_reason!r}")
        if e.get("outcome") != "rejected":
            problems.append(f"log outcome {e.get('outcome')!r}, expected 'rejected'")
        if e.get("http_status") != exp_status:
            problems.append(f"log http_status {e.get('http_status')!r}, expected {exp_status}")
    ok = not problems
    passed += ok
    say(f"-- {name}: {'PASS' if ok else 'FAIL ' + '; '.join(problems)}")
    say(f"   reply: {reply.status_code} {reply.text.strip()}")
    say(f"   log:   {new_raw_line(before)}")
summary["1"] = f"{passed}/6"

wait("between criterion 1 and 2, both use the per-address limit")

# ============================ CRITERION 2 ============================
say("\n=== CRITERION 2: a creator ID that is not text is stored as text ===")
odd_ids = [("object", {"id": "x"}), ("list", ["a"]), ("number 123", 123),
           ("null", None), ("empty string", "")]
passed = 0
for name, value in odd_ids:
    before = len(log_lines())
    reply = post({"creator_id": value, "text": ""})
    entries = new_entries(before)
    stored = entries[0].get("creator_id", "(missing)") if entries else "(no new log line)"
    ok = len(entries) == 1 and isinstance(stored, str)
    passed += ok
    say(f"-- creator_id = {name}: {'PASS' if ok else 'FAIL'}   "
        f"reply {reply.status_code}; stored creator_id = {stored!r} ({type(stored).__name__})")
    say(f"   log:   {new_raw_line(before)}")
summary["2"] = f"{passed}/5"

# ============================ CRITERION 3 ============================
say("\n=== CRITERION 3: the sixth request in a minute is blocked, and recorded ===")
post({"creator_id": cid("warmup"), "text": GOOD_TEXT})   # loads the model, uses its own creator
say("   (warm-up request sent with its own creator ID)")
passed = 0
for k in range(1, 4):
    creator = cid(f"rl{k}")
    before = len(log_lines())
    statuses, last = [], None
    started = time.monotonic()
    for _ in range(6):
        last = post({"creator_id": creator, "text": GOOD_TEXT})
        statuses.append(last.status_code)
    elapsed = time.monotonic() - started
    entries = [e for e in new_entries(before)
               if e.get("creator_id") == creator and e.get("reason") == "rate_limited"]
    raw_matches = [l for l in log_lines()[before:] if '"reason": "rate_limited"' in l and creator in l]
    problems = []
    if elapsed >= 60:
        problems.append(f"the six requests took {elapsed:.1f} s, not within one minute")
    if statuses[:5] != [200] * 5:
        problems.append(f"requests 1-5 gave {statuses[:5]}, expected all 200")
    if statuses[5] != 429:
        problems.append(f"request 6 gave {statuses[5]}, expected 429")
    try:
        if last.json().get("error") != "rate_limited":
            problems.append("request 6 reply error was not 'rate_limited'")
    except ValueError:
        problems.append("request 6 reply was not JSON")
    if len(entries) != 1:
        problems.append(f"{len(entries)} rate_limited log lines, expected 1")
    else:
        e = entries[0]
        if e.get("http_status") != 429 or e.get("outcome") != "rejected":
            problems.append("record http_status/outcome wrong")
        if not e.get("request_id"):
            problems.append("record has no request_id")
        if not isinstance(e.get("duration_ms"), int):
            problems.append("record duration_ms is not a whole number")
    ok = not problems
    passed += ok
    say(f"-- set {k} (creator {creator}): {'PASS' if ok else 'FAIL ' + '; '.join(problems)}")
    say(f"   statuses: {statuses}   (six requests took {elapsed:.1f} s)")
    say(f"   6th request's log: {raw_matches[0] if raw_matches else '(none)'}")
summary["3"] = f"{passed}/3"

# ============================ CRITERION 4 ============================
say("\n=== CRITERION 4: a scoring crash gives a safe error and an error record ===")


def crash_evidence():
    """
    EVIDENCE ONLY. Does the same pretend crash as test_scoring_error.py, but
    returns the real reply and the real error record so they can be pasted.
    It does NOT decide PASS or FAIL: that comes only from the test file.
    """
    from app import app as flask_app
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        tmp_log = tmp_dir / "audit.jsonl"
        with mock.patch.object(config, "LOG_DIR", tmp_dir), \
             mock.patch.object(config, "AUDIT_LOG", tmp_log), \
             mock.patch("detector.model_signal", side_effect=RuntimeError(SECRET)):
            reply = flask_app.test_client().post("/submit", json={
                "text": GOOD_TEXT, "creator_id": cid("crash")})
        raw = tmp_log.read_text(encoding="utf-8")
    return reply, raw


passed = 0
for k in range(1, 4):
    # The PASS or FAIL for this run comes ONLY from the test file, as the criterion says.
    test = subprocess.run([sys.executable, "test_scoring_error.py"], cwd=ROOT,
                          capture_output=True, text=True)
    ok = test.returncode == 0
    passed += ok
    said = (test.stderr + test.stdout).strip().splitlines()
    say(f"-- run {k}: {'PASS' if ok else 'FAIL (test_scoring_error.py failed)'}")
    say(f"   test_scoring_error.py said: {said[-1] if said else '(no output)'}")

    # Evidence for the README: the real reply and the real error record.
    reply, raw = crash_evidence()
    lines = raw.splitlines()
    notes = []
    if reply.status_code != 500 or reply.get_json().get("error") != "scoring_error":
        notes.append("reply was not 500 scoring_error")
    if SECRET in reply.get_data(as_text=True):
        notes.append("secret message in the reply")
    if len(lines) != 1:
        notes.append(f"{len(lines)} records, expected 1")
    else:
        e = json.loads(lines[0])
        if e.get("outcome") != "error" or e.get("http_status") != 500 or not e.get("error_type"):
            notes.append("record missing outcome/http_status/error_type")
        if SECRET in lines[0]:
            notes.append("secret message in the log")
    say("   evidence only (does not change the result): the same crash, run by this script")
    say(f"   reply: {reply.status_code} {reply.get_data(as_text=True).strip()}")
    say(f"   error record (temporary log): {lines[0] if lines else '(none)'}")
    say(f"   evidence check: {'all as expected' if not notes else '; '.join(notes)}")
summary["4"] = f"{passed}/3"

# ============================ CRITERION 5 ============================
say("\n=== CRITERION 5: the preview is cleaned and cut to 40 characters ===")
previews = [
    ("line break",     "First line of a test.\nSecond line, still made up text here.",
                       "First line of a test. Second line, still"),
    ("tab",            "Column one\tcolumn two\tcolumn three and then some more words here.",
                       "Column one column two column three and t"),
    ("bell character", "Alert\x07 character inside this made up sample sentence for testing.",
                       "Alert  character inside this made up sam"),
    # chr(0x2028) is the invisible "line separator" character, written this way
    # so it can never be lost when the file is saved or copied.
    ("line separator", "Before the separator" + chr(0x2028) + "after the separator and a few more words.",
                       "Before the separator after the separator"),
    ("100 letters",    "abcdefghij" * 10,
                       "abcdefghijabcdefghijabcdefghijabcdefghij"),
]
passed = 0
for i, (name, text, expected) in enumerate(previews, 1):
    before = len(log_lines())
    reply = post({"creator_id": cid(f"pv{i}"), "text": text})
    entries = new_entries(before)
    got = entries[0].get("input_preview") if len(entries) == 1 else "(no single new log line)"
    ok = reply.status_code == 200 and got == expected
    passed += ok
    say(f"-- {name}: {'PASS' if ok else 'FAIL'}")
    say(f"   expected: {expected!r}")
    say(f"   got:      {got!r}")
    say(f"   log:      {new_raw_line(before)}")
summary["5"] = f"{passed}/5"

# ---------------- summary for the results table ----------------
say("\n=== SUMMARY (goes in the run-log table) ===")
for key, label in [("1", "bad input, 6 of 6"), ("2", "creator ID is text, 5 of 5"),
                   ("3", "rate limit, 3 of 3"), ("4", "scoring crash, 3 of 3"),
                   ("5", "preview exact, 5 of 5")]:
    say(f"Criterion {key} ({label}): {summary[key]}")
say(f"\nsaved to {out_path}")
out_file.close()
