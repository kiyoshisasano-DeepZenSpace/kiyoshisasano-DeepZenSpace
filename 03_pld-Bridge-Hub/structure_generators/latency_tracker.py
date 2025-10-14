#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — Latency Tracker (Gradient Edition)

Extends latency event tracking with gradient-based coherence metrics.

Implements:
    Δ𝒟 = 𝒟(σ,t₂) - 𝒟(σ,t₁)

where 𝒟(σ,t) = 1 - (‖∇C(σ,t)‖ / K_drift)
and ∇C is approximated via token-level perturbations or
pause-inducing linguistic cues.

Author: DeepZenSpace / Kiyoshi Sasano (2025)
"""

import json
import time
import uuid
import math
import re
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------
K_DRIFT = 5.0  # normalization factor for ∥∇C∥

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def _iso_utc(ts=None):
    """Return ISO8601 UTC string with 'Z'."""
    if ts is None:
        ts = time.time()
    return (
        datetime.fromtimestamp(ts, tz=timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

def _approx_drift_intensity(reason: str) -> float:
    """
    Estimate gradient magnitude ∥∇C(σ,t)∥ from reason/context text.
    Uses the same drift proxy as pause_classifier.
    """
    t = (reason or "").lower().strip()
    if not t:
        return 0.0

    pause_tokens = re.findall(r"\b(wait|pause|retry|freeze|stuck|thinking|sorry|confus(e|ed))\b", t)
    punctuation_spikes = len(re.findall(r"[!?]{2,}", t))
    raw_score = 0.7 * len(pause_tokens) + 0.3 * punctuation_spikes
    token_count = max(len(t.split()), 1)
    drift_intensity = raw_score / math.log2(token_count + 2)
    return min(drift_intensity, K_DRIFT)

def _compute_D_sigma_t(reason: str) -> float:
    """Compute coherence score 𝒟(σ,t)."""
    drift_intensity = _approx_drift_intensity(reason)
    return round(max(0.0, 1.0 - (drift_intensity / K_DRIFT)), 3)

# ---------------------------------------------------------------------
# Core Class
# ---------------------------------------------------------------------
class LatencyEvent:
    """Represents a latency-hold or related timing segment."""

    def __init__(self, session_id: str, reason: str, duration_ms: float, context=None, prev_D: float | None = None):
        self.session_id = session_id
        self.reason = reason
        self.duration_ms = duration_ms
        self.context = context or {}
        self.start_time = time.time()
        self.end_time = None
        self.event_id = str(uuid.uuid4())

        # Gradient coherence metrics
        self.prev_D = prev_D if prev_D is not None else 1.0
        self.D_sigma_t = _compute_D_sigma_t(reason)
        self.delta_D = round(self.D_sigma_t - self.prev_D, 4)

    def end(self):
        self.end_time = time.time()

    @property
    def end_time_iso(self):
        return _iso_utc(self.end_time or time.time())

    def to_jsonl(self):
        """Return schema-compliant JSONL line with gradient metrics."""
        return json.dumps(
            {
                "event_type": "latency_hold",
                "timestamp": self.end_time_iso,
                "session_id": self.session_id,
                "metadata": {
                    "duration_ms": self.duration_ms,
                    "reason": self.reason,
                    "context": self.context,
                    "event_id": self.event_id,
                },
                "gradient_metrics": {
                    "D_sigma_t": self.D_sigma_t,
                    "delta_D": self.delta_D,
                    "K_drift": K_DRIFT,
                },
            },
            ensure_ascii=False,
        )

# ---------------------------------------------------------------------
# Emit function
# ---------------------------------------------------------------------
def emit_pld_jsonl(event: LatencyEvent, out_path: Path):
    """Emit a JSONL line to the specified file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(event.to_jsonl() + "\n")
    return out_path

# ---------------------------------------------------------------------
# Demo run
# ---------------------------------------------------------------------
if __name__ == "__main__":
    OUT = Path("demo_quick/latency_demo.jsonl")

    # Simulate previous drift baseline (from earlier pause)
    prev_D = 0.86

    ev = LatencyEvent(
        "sess_demo_001",
        reason="soft_repair_probe (user hesitated after lag)",
        duration_ms=820.0,
        context={"phase": "checkout"},
        prev_D=prev_D,
    )
    time.sleep(0.1)
    ev.end()
    emit_pld_jsonl(ev, OUT)
    print(f"[ok] Wrote latency event with gradient metrics to {OUT}")
    print(json.dumps(json.loads(ev.to_jsonl()), indent=2, ensure_ascii=False))
