# Copyright 2026 OMNIA EYE Corporation.
# SPDX-License-Identifier: Apache-2.0
"""Explicit local checkpoint configuration and complete-input inference."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass

from .ledger import probability


@dataclass(frozen=True)
class Settings:
    revision: str
    model: str = "english"
    device: str = "cpu"
    threads: int = 2
    max_len: int = 512
    head_max_len: int = 192
    max_bytes: int = 65536
    min_probability: float = .8
    database: str = "var/omnia/decisions.sqlite3"

    def __post_init__(self):
        if not re.fullmatch(r"[0-9a-f]{40}", self.revision):
            raise ValueError("OMNIA_LAYA_REVISION must be an immutable 40-character Hub commit")
        limits = {"english": 512, "typed-decisions": 1024, "multilingual": 8192}
        if self.model not in limits or self.device not in {"cpu", "cuda", "mps"}:
            raise ValueError("unsupported model or device")
        if not 1 <= self.threads <= 64 or not 128 <= self.max_len <= limits[self.model]:
            raise ValueError("invalid thread count or context size")
        if not 32 <= self.head_max_len < self.max_len or not 1024 <= self.max_bytes <= 1048576:
            raise ValueError("invalid head or byte budget")
        probability(self.min_probability)
        if not self.database.strip():
            raise ValueError("database path is required")

    @classmethod
    def from_env(cls):
        return cls(
            revision=os.environ.get("OMNIA_LAYA_REVISION", ""),
            model=os.environ.get("OMNIA_LAYA_MODEL", "english"),
            device=os.environ.get("OMNIA_LAYA_DEVICE", "cpu"),
            threads=int(os.environ.get("OMNIA_LAYA_THREADS", "2")),
            max_len=int(os.environ.get("OMNIA_LAYA_MAX_LEN", "512")),
            head_max_len=int(os.environ.get("OMNIA_LAYA_HEAD_MAX_LEN", "192")),
            max_bytes=int(os.environ.get("OMNIA_LAYA_MAX_INPUT_BYTES", "65536")),
            min_probability=float(os.environ.get("OMNIA_LAYA_MIN_PROBABILITY", "0.8")),
            database=os.environ.get("OMNIA_LAYA_DATABASE", "var/omnia/decisions.sqlite3"),
        )
