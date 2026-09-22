# Copyright 2026 OMNIA EYE Corporation.
# SPDX-License-Identifier: Apache-2.0
"""Validated, replayable decision records without persisting input text."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

SCHEMA = "omnia.decision.v1"


class DecisionError(RuntimeError):
    """A processing error whose public message never includes provider text."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def text(value: Any, maximum: int = 512) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError("invalid bounded string")
    return value


def probability(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("probability must be a finite number")
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("probability must be between zero and one")
    return value
