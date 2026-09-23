# Copyright 2026 OMNIA EYE Corporation.
# SPDX-License-Identifier: Apache-2.0
"""Process bounded JSONL requests; emit one safe result per nonempty input line."""

import argparse
import json
import sys

from .ledger import DecisionLedger
from .runtime import LocalLaya, Settings


def process(source, output, ledger, backend, settings):
    failures = 0
    manifest = backend.manifest()
    line_number = 0
    while True:
        line = source.readline(settings.max_bytes + 1)
        if not line:
            break
        line_number += 1
        if len(line) > settings.max_bytes:
            while line and not line.endswith(b"\n"):
                line = source.readline(settings.max_bytes + 1)
            record = {"status": "failed", "line": line_number, "error_code": "INPUT_TOO_LARGE"}
            failures += 1
        elif not line.strip():
            continue
        else:
            try:
                request = json.loads(line.decode("utf-8"))
                record = ledger.decide(request, backend, manifest=manifest,
                                       min_probability=settings.min_probability, max_bytes=settings.max_bytes)
            except Exception as error:
                record = {"status": "failed", "line": line_number, "error_code": type(error).__name__}
                failures += 1
        output.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")
        output.flush()
    return failures


def main():
    parser = argparse.ArgumentParser(description="OMNIA Laya decision ledger")
    parser.add_argument("--input", default="-", help="JSONL file, or - for stdin")
    args = parser.parse_args()
    ledger = None
    source = None
    try:
        settings = Settings.from_env()
        backend = LocalLaya(settings)
        ledger = DecisionLedger(settings.database)
        source = sys.stdin.buffer if args.input == "-" else open(args.input, "rb")
        failures = process(source, sys.stdout, ledger, backend, settings)
        return 1 if failures else 0
    except Exception as error:
        print(json.dumps({"status": "failed", "error_code": type(error).__name__}), file=sys.stderr)
        return 2
    finally:
        if source is not None and args.input != "-":
            source.close()
        if ledger is not None:
            ledger.close()


if __name__ == "__main__":
    raise SystemExit(main())
