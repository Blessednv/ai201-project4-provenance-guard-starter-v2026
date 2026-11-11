"""
CAPSTONE: a repeatable test for the scoring safety net in /submit.

What it checks, in plain words:
  1. We PRETEND the model's scoring crashes, on purpose.
  2. We send a normal made-up submission.
  3. The service should answer with a clean 500 error and NO technical details.
  4. Exactly one "error" line should appear in a TEMPORARY log, with the right
     fields. Your real logs/audit.jsonl is never touched.

Run it with:   python test_scoring_error.py
"""

import json
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest import mock

import config
from app import app


class ScoringErrorTest(unittest.TestCase):
    def test_scoring_crash_leaves_an_error_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            tmp_log = tmp_dir / "audit.jsonl"

            # Point the logging at a temporary file, and make the model's
            # scoring function crash with a pretend error.
            with mock.patch.object(config, "LOG_DIR", tmp_dir), \
                 mock.patch.object(config, "AUDIT_LOG", tmp_log), \
                 mock.patch("detector.model_signal",
                            side_effect=RuntimeError("secret internal detail")):
                reply = app.test_client().post("/submit", json={
                    "text": "This is a made-up sample for the crash test.",
                    # CAPSTONE: a fresh ID every run, so the rate limit
                    # (5 per minute per creator) can never block this test.
                    "creator_id": f"test_scoring_error_{uuid.uuid4().hex[:8]}",
                })

            # The caller gets a clean 500 and no technical details.
            self.assertEqual(reply.status_code, 500)
            self.assertEqual(reply.get_json()["error"], "scoring_error")
            self.assertNotIn("secret internal detail", reply.get_data(as_text=True))

            # Exactly one record was written, and it says "error".
            lines = tmp_log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            entry = json.loads(lines[0])
            self.assertEqual(entry["outcome"], "error")
            self.assertEqual(entry["event"], "error")
            self.assertEqual(entry["reason"], "scoring_error")
            self.assertEqual(entry["http_status"], 500)
            self.assertEqual(entry["error_type"], "RuntimeError")
            self.assertEqual(entry["input_preview"],
                             "This is a made-up sample for the crash t")
            self.assertIsInstance(entry["duration_ms"], int)
            self.assertTrue(entry["request_id"])
            # Only the TYPE is logged, never the message.
            self.assertNotIn("secret internal detail", lines[0])


if __name__ == "__main__":
    unittest.main()
