#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — Reentry Detector

Detects user reentry into a previous conversational intent or state.
Includes both heuristic and (optional) model-assisted detection.
"""

from dataclasses import dataclass
from typing import List, Optional
import difflib
import argparse
import json
import sys

@dataclass
class ReentryResult:
    is_reentry: bool
    reason: str
    matching_segment: Optional[str]
    similarity_score: float

def _similarity(a: str, b: str) -> float:
    """Compute normalized similarity between two strings."""
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def _heuristic_reentry(past_segments: List[str], current_input: str, threshold: float = 0.62) -> ReentryResult:
    """Heuristic reentry detection using string similarity."""
    if not past_segments:
        return ReentryResult(False, "no past segments", None, 0.0)

    scores = [(_similarity(seg, current_input), seg) for seg in past_segments]
    scores.sort(reverse=True, key=lambda x: x[0])
    top_score, match_seg = scores[0]

    if top_score >= threshold:
        return ReentryResult(True, f"similarity {top_score:.2f} ≥ threshold {threshold}", match_seg, top_score)
    return ReentryResult(False, f"similarity {top_score:.2f} < threshold {threshold}", match_seg, top_score)

def detect_reentry(past_segments: List[str], current_input: str,
                   use_api: bool = False, model: str = "gpt-4o-mini",
                   threshold: float = 0.62) -> ReentryResult:
    """
    Detect reentry either heuristically or using API-based similarity (if enabled).
    """
    if use_api:
        try:
            import openai
            client = openai.OpenAI()
            joined = "\n".join(f"- {seg}" for seg in past_segments)
            prompt = (
                "Given the following past user segments, determine whether the current input "
                f'resumes or repeats a previous intent. Respond with JSON: {{"is_reentry": bool, "reason": str, "match": str}}.\n\n'
                f"Past:\n{joined}\n\nCurrent: {current_input}"
            )
            resp = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
            content = resp.choices[0].message.content.strip()
            data = json.loads(content)
            return ReentryResult(bool(data.get("is_reentry")), data.get("reason", ""), data.get("match"), 1.0)
        except Exception as e:
            print(f"[warn] API reentry detection failed: {e}. Falling back to heuristic.", file=sys.stderr)
            return _heuristic_reentry(past_segments, current_input, threshold=threshold)
    else:
        return _heuristic_reentry(past_segments, current_input, threshold=threshold)

def main():
    p = argparse.ArgumentParser(description="PLD Bridge Hub Reentry Detector")
    p.add_argument("past", nargs="+", help="Past user segments (space-separated or quoted)")
    p.add_argument("--current", required=True, help="Current user input")
    p.add_argument("--api", action="store_true", help="Use OpenAI API for detection")
    p.add_argument("--model", type=str, default="gpt-4o-mini", help="Model for API mode")
    p.add_argument("--threshold", type=float, default=0.62, help="Similarity threshold for reentry (0–1)")
    args = p.parse_args()

    res = detect_reentry(args.past, args.current,
                         use_api=args.api, model=args.model, threshold=args.threshold)
    print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
