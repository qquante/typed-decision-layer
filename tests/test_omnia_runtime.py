# Copyright 2026 OMNIA EYE Corporation.
# SPDX-License-Identifier: Apache-2.0
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from examples.omnia.__main__ import process
from examples.omnia.ledger import DecisionLedger
from examples.omnia.runtime import Settings, check_temperatures, check_token_budget


class Backend:
    def manifest(self):
        return {"test_contract": 1}

    def __call__(self, state, questions):
        return {"answers": {"match": {"type": "noul", "noul": .9}}}


class RuntimeTests(unittest.TestCase):
    def test_only_affected_temperature_bucket_is_rejected(self):
        agent = SimpleNamespace(temperature_raw=[1., 1., 1.], temperature=[1., 1., 1.],
                                temperature_by_options_raw={"choice:11+": .1},
                                temperature_by_options={"choice:11+": .5})
        question = {"type": "choice", "criteria": {str(i): "item" for i in range(11)}}
        with self.assertRaises(ValueError):
            check_temperatures(agent, {"q": question})
        check_temperatures(agent, {"q": {"type": "choice", "criteria": {"a": "one", "b": "two"}}})

    def test_complete_token_budget(self):
        class WordTokenizer:
            mask_token = "[MASK]"

            def __call__(self, value, **kwargs):
                return {"input_ids": list(range(len(value.split())))}

        tokenizer = WordTokenizer()
        questions = {"x": {"type": "choice", "instructions": "Pick a route", "criteria": {"a": "one", "b": "two"}}}
        check_token_budget(tokenizer, "small input", questions, max_len=64, head_max_len=32)
        for state, question, maximum, head in (
            ("word " * 100, questions, 64, 32),
            ("small", {"x": {**questions["x"], "instructions": "word " * 100}}, 128, 32),
            ("small", {"x": {**questions["x"], "criteria": {"a": "word " * 80, "b": "two"}}}, 128, 32),
        ):
            with self.assertRaises(ValueError):
                check_token_budget(tokenizer, state, question, max_len=maximum, head_max_len=head)

    def test_requires_immutable_revision(self):
        for revision in ("", "main", "v1.0", "a" * 39, "X" * 40):
            with self.assertRaises(ValueError):
                Settings(revision)
        Settings("a" * 40)

    def test_config_bounds(self):
        for kwargs in ({"threads": 0}, {"max_len": 8192}, {"head_max_len": 512},
                       {"min_probability": float("nan")}, {"device": "auto"},
                       {"max_bytes": 100}, {"database": ""}):
            with self.assertRaises(ValueError):
                Settings("a" * 40, **kwargs)

    def test_all_example_keys_are_consumed(self):
        values = {}
        path = Path(__file__).resolve().parents[1] / "examples/omnia/.env.example"
        for line in path.read_text().splitlines():
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                values[key] = value
        values["OMNIA_LAYA_REVISION"] = "a" * 40
        with patch.dict(os.environ, values, clear=True):
            config = Settings.from_env()
        self.assertEqual(config.revision, "a" * 40)
        self.assertEqual(config.threads, 2)
        self.assertEqual(config.model, "english")

    def test_stream_preserves_success_failure_and_replay(self):
        request = {"id": "one", "state": "valid state", "evidence": ["source:one"],
                   "questions": {"match": {"type": "noul", "instructions": "Does it match?"}}}
        line = json.dumps(request).encode() + b"\n"
        source = io.BytesIO(line + b"{broken\n" + b"x" * 3000 + b"\n" + line)
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as folder:
            ledger = DecisionLedger(Path(folder) / "decisions.sqlite3")
            try:
                failures = process(source, output, ledger, Backend(), Settings("a" * 40, max_bytes=1024))
            finally:
                ledger.close()
        rows = [json.loads(row) for row in output.getvalue().splitlines()]
        self.assertEqual(failures, 2)
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[1]["line"], 2)
        self.assertEqual(rows[2]["error_code"], "INPUT_TOO_LARGE")
        self.assertTrue(rows[3]["cache_hit"])


if __name__ == "__main__":
    unittest.main()
