# Verification

The OMNIA checks cover typed answer contracts, probability gates, cache identity,
restart/replay, malformed records, failed inference, complete-input token budgets
and active calibration-bucket validation. Evaluation formulas are checked against
hand-calculated cases.

```bash
python -m unittest discover -s tests -p 'test_omnia*.py' -v
ruff check laya/ examples/omnia/ tests/test_omnia*.py --select=E9,F63,F7,F82,F401,F811 --line-length=120
python -m compileall -q laya/ tests/ examples/omnia/
python tests/test_hooks_api.py
zensical build --strict --clean
```

Contract tests exercise controlled responses and failure conditions without
downloading model weights. Local model inference is checked separately through
the JSONL runner with a pinned checkpoint. The two quickstart requests establish
that the integration runs end to end; they are not a domain-accuracy benchmark.

See `verification.json` for the recorded local validation receipt. CI repeats
the contract checks on Python 3.10 and 3.12 and builds the documentation in strict
mode. Preserve separate records for local verification and GitHub workflow runs.
