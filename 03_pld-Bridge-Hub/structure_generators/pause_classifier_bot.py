#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — UX Pause Classifier (Gradient-Enhanced)

Extension of the heuristic pause classifier to include a
gradient-based drift score approximation:

    𝒟(σ,t) = 1 - (‖∇C(σ,t)‖ / K_drift)

where ∇C(σ,t) is approximated via token-level perturbations and
keyword drift indicators within the utterance.

The intent is to bridge rule-based classification with
a continuous-valued coherence drift metric.

Author: DeepZenSpace / Kiyoshi Sasano (2025)
"""

from __future__ import annotations
import os
import json
import re
import math
import argparse
from typing import TypedDict, Optional

# ---------------- Constants ----------------
K_DRIFT = 5.0  # Normalization constant for drift gradient magnitude

class ClassificationResult(TypedDict):
    classification: str
    reason: str
    D_sigma_t: float
    drift_intensity: float

PAUSE_TYPES = [
    "⏸️ Cognitive",
    "⏸️ UI Friction",
    "⏸️ Disengagement",
    "⏸️ Repair",
    "⏸️ Latency Hold"
]

# ---------------- Keyword Heuristics ----------------
_KEYWORDS = {
    "⏸️ UI Friction": [
        r"\b(back button|disabled|spinner|loading|lag|bug|freeze|stuck|hovered|tooltip)\b",
        r"\bclick(ed)?\s+but\s+nothing\b",
        r"\bconfus(e|ing)|misclick|ui\b",
    ],
    "⏸️ Disengagement": [
        r"\b(left|leave|abandon|quit|timeout|went away|no response)\b",
        r"\bafk|brb\b",
    ],
    "⏸️ Repair": [
        r"\b(correct|undo|clarif(y|ication)|sorry|fix|retry|re-enter|try again)\b",
    ],
    "⏸️ Latency Hold": [
        r"\b(wait(ed)?|waiting|hold|pause|intentional pause|deliberate)\b",
        r"\bcountdown|shimmer|thinking indicator\b",
    ],
    "⏸️ Cognitive": [
        r"\b(thinking|hesitat(e|ion)|not sure|confus(e|ed)|searching|considering|re-reading|hmm+)\b",
    ],
}

# ---------------- Gradient Approximation Layer ----------------
def compute_drift_intensity(text: str) -> float:
    """
    Approximate gradient magnitude of coherence ∇C(σ,t)
    based on local textual irregularities and keyword density.
    """
    t = text.lower().strip()
    if not t:
        return 0.0

    # Structural drift factors
    pause_tokens = re.findall(r"\b(wait|pause|retry|undo|sorry|freeze|stuck)\b", t)
    hesitation_tokens = re.findall(r"\b(hmm+|uh+|um+|not sure|confus(e|ed))\b", t)
    punctuation_spikes = len(re.findall(r"[!?]{2,}", t))

    raw_score = (
        0.6 * len(pause_tokens)
        + 0.3 * len(hesitation_tokens)
        + 0.1 * punctuation_spikes
    )

    # Normalize by log token count to approximate ∥∇C∥ scaling
    token_count = max(len(t.split()), 1)
    drift_intensity = raw_score / math.log2(token_count + 2)

    return min(drift_intensity, K_DRIFT)  # cap for stability

def compute_D_sigma_t(text: str) -> float:
    """Compute 𝒟(σ,t) = 1 - (‖∇C(σ,t)‖ / K_drift)."""
    drift_intensity = compute_drift_intensity(text)
    return round(max(0.0, 1.0 - (drift_intensity / K_DRIFT)), 3)

# ---------------- Heuristic Classifier ----------------
def _heuristic_classify(text: str) -> ClassificationResult:
    t = text.lower().strip()
    if not t:
        return {
            "classification": "⏸️ Classification Failed",
            "reason": "Empty log input.",
            "D_sigma_t": 1.0,
            "drift_intensity": 0.0
        }

    drift_intensity = compute_drift_intensity(t)
    D_sigma_t = 1.0 - (drift_intensity / K_DRIFT)

    priority = ["⏸️ UI Friction", "⏸️ Repair", "⏸️ Latency Hold", "⏸️ Disengagement", "⏸️ Cognitive"]
    for label in priority:
        patterns = _KEYWORDS.get(label, [])
        for pat in patterns:
            if re.search(pat, t):
                return {
                    "classification": label,
                    "reason": f"Matched heuristic pattern: {pat}",
                    "D_sigma_t": round(D_sigma_t, 3),
                    "drift_intensity": round(drift_intensity, 3)
                }

    return {
        "classification": "⏸️ Cognitive",
        "reason": "No strong pattern; defaulting to cognitive pause.",
        "D_sigma_t": round(D_sigma_t, 3),
        "drift_intensity": round(drift_intensity, 3)
    }

# ---------------- LLM Integration (unchanged core) ----------------
def _get_openai_clients():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, None
    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=api_key)
        return "new", client
    except Exception:
        pass
    try:
        import openai  # type: ignore
        openai.api_key = api_key
        return "legacy", openai
    except Exception:
        return None, None

def classify_pause(user_log: str, use_api: bool = False, model: str = "gpt-4o-mini") -> ClassificationResult:
    """
    Public API entry point.
    Adds gradient-based drift metrics even in heuristic mode.
    """
    if not use_api:
        return _heuristic_classify(user_log)

    # API branch unchanged (simplified for reliability)
    mode, client_or_mod = _get_openai_clients()
    base = _heuristic_classify(user_log)
    if mode is None:
        base["reason"] = "API key missing. " + base["reason"]
        return base

    # If LLM available, use heuristic drift but LLM classification
    try:
        prompt = (
            "You are a UX pause classifier.\n"
            f"Classify into one of: {', '.join(PAUSE_TYPES)}.\n"
            "Respond JSON: {classification, reason}.\n"
            f"LOG = {json.dumps(user_log, ensure_ascii=False)}"
        )
        if mode == "new":
            resp = client_or_mod.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": "You classify UX pauses."},
                          {"role": "user", "content": prompt}],
                temperature=0.2
            )
            content = resp.choices[0].message.content or ""
        else:
            resp = client_or_mod.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": "You classify UX pauses."},
                          {"role": "user", "content": prompt}],
                temperature=0.2
            )
            content = resp["choices"][0]["message"]["content"]

        data = json.loads(content) if content.strip().startswith("{") else {}
        base["classification"] = data.get("classification", base["classification"])
        base["reason"] = data.get("reason", base["reason"])
        return base
    except Exception as e:
        base["reason"] = f"LLM error, fallback heuristic used: {e}"
        return base

# ---------------- CLI ----------------
def _interactive_loop():
    print("\n--- UX Pause Classifier (Gradient Edition) ---")
    print("Type a user interaction log (or 'exit' to quit):")
    while True:
        try:
            user_input = input("\nLog > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[exit]")
            break
        if user_input.lower() in ("exit", "quit"):
            break
        res = classify_pause(user_input)
        print(json.dumps(res, ensure_ascii=False, indent=2))

def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="PLD Pause Classifier (Gradient Edition)")
    p.add_argument("--once", type=str, default="", help="Classify a single log string and print JSON")
    args = p.parse_args(argv)
    if args.once:
        res = classify_pause(args.once)
        print(json.dumps(res, ensure_ascii=False))
        return 0
    _interactive_loop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
