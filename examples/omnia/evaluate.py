# Copyright 2026 OMNIA EYE Corporation.
# SPDX-License-Identifier: Apache-2.0
"""Evaluate labeled choice decisions using probabilities, calibration and coverage."""

import argparse
import json
import math

from .ledger import probability


def choice_metrics(rows, *, threshold=.8, bins=10):
    threshold = probability(threshold)
    if not isinstance(bins, int) or isinstance(bins, bool) or not 1 <= bins <= 100:
        raise ValueError("bins must be between one and 100")
    buckets = [[] for _ in range(bins)]
    seen, correct, accepted, accepted_errors = set(), 0, 0, 0
    brier, nll = 0., 0.
    for row in rows:
        identifier = row["id"]
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise ValueError("evaluation identifiers must be unique nonempty strings")
        seen.add(identifier)
        values, expected = row["probabilities"], row["expected"]
        if not isinstance(values, dict) or not values or expected not in values:
            raise ValueError("expected class must be in the distribution")
        values = {label: probability(value) for label, value in values.items()}
        if abs(sum(values.values()) - 1) > len(values) * .000051:
            raise ValueError("distribution must sum to one")
        # Stable label ordering gives ties an explicit rule, independent of JSON order.
        predicted = max(sorted(values), key=values.get)
        confidence = values[predicted]
        hit = int(predicted == expected)
        correct += hit
        brier += sum((value - int(label == expected)) ** 2 for label, value in values.items())
        nll -= math.log(max(values[expected], 1e-15))
        buckets[min(int(confidence * bins), bins - 1)].append((confidence, hit))
        if confidence >= threshold:
            accepted += 1
            accepted_errors += 1 - hit
    count = len(seen)
    if not count:
        raise ValueError("at least one labeled decision is required")
    ece = sum(abs(sum(c - hit for c, hit in bucket)) for bucket in buckets) / count
    return {"count": count, "accuracy": correct / count, "brier_multiclass": brier / count,
            "negative_log_likelihood": nll / count, "ece": ece, "ece_bins": bins,
            "threshold": threshold, "accepted": accepted, "coverage": accepted / count,
            "selective_error_rate": accepted_errors / accepted if accepted else None}


def main():
    parser = argparse.ArgumentParser(description="Evaluate reviewed OMNIA choice decisions")
    parser.add_argument("--input", required=True, help="JSONL with id, expected and probabilities")
    parser.add_argument("--threshold", type=float, default=.8)
    args = parser.parse_args()
    with open(args.input, encoding="utf-8-sig") as source:
        rows = (json.loads(line) for line in source if line.strip())
        print(json.dumps(choice_metrics(rows, threshold=args.threshold), allow_nan=False))


if __name__ == "__main__":
    main()
