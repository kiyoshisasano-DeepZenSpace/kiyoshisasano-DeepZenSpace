#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — Reentry Detector
Detects reentry (resuming a previously dropped intent) from a list of past segments.

Modes:
  1) Local heuristic (no API needed): default fallback if OPENAI_API_KEY is missing, or use --local
  2) OpenAI LLM (if API key is set): attempts structured JSON output

CLI:
  python reentry_detector.py
  python reentry_detector.py --local
  python reentry_detector.py --api --model gpt-4o-mini

Env:
  OPENAI_API_KEY=...

Returns (dict):
  {
    "is_reentry": bool,
    "reason": str,
    "matching_segment": str
  }
"""

from __future__ import annotations
import os
import sys
import json
import argparse
import difflib
from typing import List, TypedDict, Optional

# ---------------- Types ----------------
class ReentryResult(TypedDict):
    is_reentry: bool
    reason: str
    matching_segment: str

# ---------------- Local heuristic ----------------
def _heuristic_reentry(past_segments: List[str], current_input: str, threshold: float = 0.62) -> ReentryResult:
    """
    Simple similarity-based detector:
      - Uses difflib ratio to find the closest past segment
      - If similarity >= threshold OR past token appears in input → reentry
    """
    if not past_segments or not current_input.strip():
        return {"is_reentry": False, "reason": "Empty input or no history.", "matching_segment": ""}

    # Normalize
    cand = current_input.lower()
    scores = []
    for seg in past_segments:
        s = difflib.SequenceMatcher(a=seg.lower(), b=cand).ratio()
        scores.append((s, seg))

    scores.sort(reverse=True, key=lambda x: x[0])
    best_score, best_seg = scores[0]

    token_hit = False
    # crude token overlap check
    for seg in past_segments:
        token = seg.strip().lower()
        if token and token in cand:
            token_hit = True
            best_seg = seg
            break

    is_re = bool(best_score >= threshold or token_hit)
    reason = f"Heuristic: best_similarity={best_score:.2f}, token_hit={token_hit}"
    return {"is_reentry": is_re, "reason": reason, "matching_segment": best_seg if is_re else ""}

# ---------------- OpenAI client (new/legacy compatible) ----------------
def _get_openai_clients():
    """
    Try to initialize OpenAI client in a forward/backward compatible way.
    Returns tuple: (mode, client_or_module)
      mode in {"new", "legacy", None}
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, None

    # Try new style first
    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=api_key)
        return "new", client
    except Exception:
        pass

    # Fallback to legacy
    try:
        import openai  # type: ignore
        openai.api_key = api_key
        return "legacy", openai
    except Exception:
        return None, None

def _structured_prompt(past_segments: List[str], current_input: str) -> str:
    return (
        "You are a structural dialogue analyst (Phase Loop Dynamics).\n"
        "Task: Determine whether CURRENT input resumes a previously dropped intent in PAST segments.\n"
        "Respond ONLY with a strict JSON object using keys: is_reentry (boolean), reason (string), matching_segment (string).\n\n"
        f"PAST = {json.dumps(past_segments, ensure_ascii=False)}\n"
        f"CURRENT = {json.dumps(current_input, ensure_ascii=False)}\n\n"
        "Rules:\n"
        "- If CURRENT clearly returns to a topic present in PAST, set is_reentry=true and copy that past segment into matching_segment.\n"
        "- Else set is_reentry=false and matching_segment=\"\".\n"
        "- Keep reason short and concrete.\n"
        "Output example:\n"
        "{ \"is_reentry\": true, \"reason\": \"Resumes latency topic.\", \"matching_segment\": \"What does 'latency hold' mean?\" }\n"
    )

def _parse_json_safely(text: str) -> Optional[dict]:
    text = text.strip()
    # Try direct JSON
    try:
        return json.loads(text)
    except Exception:
        pass
    # Try to extract JSON block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            return None
    return None

def _llm_reentry_new(client, past_segments: List[str], current_input: str, model: str) -> ReentryResult:
    # new client: client.chat.completions.create(...)
    try:
        prompt = _structured_prompt(past_segments, current_input)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a structural dialogue analyst specialized in Phase Loop Dynamics."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = resp.choices[0].message.content
        data = _parse_json_safely(content or "")
        if isinstance(data, dict) and "is_reentry" in data:
            return {
                "is_reentry": bool(data.get("is_reentry")),
                "reason": str(data.get("reason", "")),
                "matching_segment": str(data.get("matching_segment", "")),
            }
        # fallback: mark not sure
        return {
            "is_reentry": False,
            "reason": "LLM returned non-JSON or missing keys.",
            "matching_segment": "",
        }
    except Exception as e:
        return {"is_reentry": False, "reason": f"API Error (new): {e}", "matching_segment": ""}

def _llm_reentry_legacy(openai_mod, past_segments: List[str], current_input: str, model: str) -> ReentryResult:
    # legacy client: openai.ChatCompletion.create(...)
    try:
        prompt = _structured_prompt(past_segments, current_input)
        resp = openai_mod.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a structural dialogue analyst specialized in Phase Loop Dynamics."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = resp["choices"][0]["message"]["content"]
        data = _parse_json_safely(content or "")
        if isinstance(data, dict) and "is_reentry" in data:
            return {
                "is_reentry": bool(data.get("is_reentry")),
                "reason": str(data.get("reason", "")),
                "matching_segment": str(data.get("matching_segment", "")),
            }
        return {
            "is_reentry": False,
            "reason": "LLM returned non-JSON or missing keys.",
            "matching_segment": "",
        }
    except Exception as e:
        # Some installs expose errors under openai_mod.error.*
        err_msg = getattr(e, "message", str(e))
        return {"is_reentry": False, "reason": f"API Error (legacy): {err_msg}", "matching_segment": ""}

def detect_reentry(past_segments: List[str], current_input: str, use_api: bool = False, model: str = "gpt-4o-mini") -> ReentryResult:
    """
    Library entry point. If use_api is True and OPENAI_API_KEY is set, uses LLM.
    Otherwise falls back to heuristic.
    """
    if use_api:
        mode, client_or_mod = _get_openai_clients()
        if mode == "new":
            return _llm_reentry_new(client_or_mod, past_segments, current_input, model=model)
        elif mode == "legacy":
            return _llm_reentry_legacy(client_or_mod, past_segments, current_input, model=model)
        # If API requested but not available, fall through to heuristic with note.
        h = _heuristic_reentry(past_segments, current_input)
        h["reason"] = "API key missing. " + h["reason"]
        return h
    else:
        return _heuristic_reentry(past_segments, current_input)

# ---------------- CLI ----------------
def _example_history() -> List[str]:
    return [
        "How do I export this as PDF?",
        "Wait, what does 'latency hold' mean again?",
        "Can I try this on mobile?"
    ]

def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="PLD Reentry Detector")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--local", action="store_true", help="Force local heuristic detection (no API)")
    mode.add_argument("--api", action="store_true", help="Use OpenAI API if OPENAI_API_KEY is set")
    p.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model name (when --api)")
    p.add_argument("--past", type=str, default="", help="JSON array of past segments; if omitted, uses example")
    p.add_argument("--current", type=str, default="Actually, about the latency thing... is that why it paused?", help="Current input text")
    args = p.parse_args(argv)

    try:
        past_segments = json.loads(args.past) if args.past.strip() else _example_history()
        if not isinstance(past_segments, list):
            raise ValueError("--past must be a JSON array of strings")
    except Exception:
        past_segments = _example_history()

    res = detect_reentry(past_segments, args.current, use_api=args.api, model=args.model)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
