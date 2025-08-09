#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — UX Pause Classifier (LLM-optional)

Classifies pause types in UX interaction logs into one of:
  - "⏸️ Cognitive"
  - "⏸️ UI Friction"
  - "⏸️ Disengagement"
  - "⏸️ Repair"
  - "⏸️ Latency Hold"

Modes:
  1) Local heuristic (no API needed): default if OPENAI_API_KEY is missing, or use --local
  2) OpenAI LLM (if API key is set): attempts structured JSON output

CLI:
  python pause_classifier_bot.py                      # interactive loop
  python pause_classifier_bot.py --once "log text"    # one-shot, prints JSON
  python pause_classifier_bot.py --api --model gpt-4o-mini --once "log text"

Env:
  OPENAI_API_KEY=...

Return (dict):
  {
    "classification": "<one of the PAUSE_TYPES or '⏸️ Classification Failed'>",
    "reason": "short explanation"
  }
"""

from __future__ import annotations
import os
import json
import re
import argparse
from typing import TypedDict, Optional

# ---------------- Types ----------------
class ClassificationResult(TypedDict):
    classification: str
    reason: str

PAUSE_TYPES = [
    "⏸️ Cognitive",      # Latency-driven phase shift
    "⏸️ UI Friction",    # Interface-induced hesitation
    "⏸️ Disengagement",  # Dropout / abandonment
    "⏸️ Repair",         # Cue-triggered correction
    "⏸️ Latency Hold"    # Intentional system pause
]

# ---------------- Local heuristic ----------------
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
        r"\bcorrect(ed|ion)?|undo|clarif(y|ication)|sorry\b",
        r"\bfix(ed)?|retry|re-enter|try again\b",
    ],
    "⏸️ Latency Hold": [
        r"\b(wait(ed)?|waiting|hold|pause|intentional pause|deliberate)\b",
        r"\bcountdown|shimmer|thinking indicator\b",
    ],
    "⏸️ Cognitive": [
        r"\bthinking|hesitat(e|ion)|not sure|confus(e|ed)\b",
        r"\bsearching|considering|re-reading|hmm+\b",
    ],
}

def _heuristic_classify(text: str) -> ClassificationResult:
    t = text.lower().strip()
    if not t:
        return {"classification": "⏸️ Classification Failed", "reason": "Empty log input."}

    # Rule priority: UI Friction > Repair > Latency Hold > Disengagement > Cognitive
    priority = ["⏸️ UI Friction", "⏸️ Repair", "⏸️ Latency Hold", "⏸️ Disengagement", "⏸️ Cognitive"]
    for label in priority:
        patterns = _KEYWORDS.get(label, [])
        for pat in patterns:
            if re.search(pat, t):
                return {"classification": label, "reason": f"Matched heuristic pattern: {pat}"}

    # Fallback by heuristics on durations/seconds mentions
    if re.search(r"\b(\d+(\.\d+)?)\s*(s|sec|seconds)\b", t):
        return {"classification": "⏸️ Cognitive", "reason": "Duration mentioned; defaulting to cognitive pause."}

    return {"classification": "⏸️ Cognitive", "reason": "No strong pattern; defaulting to cognitive pause."}

# ---------------- OpenAI client (new/legacy compatible) ----------------
def _get_openai_clients():
    """
    Initialize OpenAI client in a forward/backward compatible way.
    Returns tuple: (mode, client_or_module) where mode in {"new", "legacy", None}
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, None

    # Try new style
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

def _structured_prompt(user_log: str) -> str:
    fam = ", ".join(PAUSE_TYPES)
    return (
        "You are a UX pause classifier (Phase Loop Dynamics).\n"
        f"Classify the pause type for the following interaction log into exactly ONE of: {fam}.\n"
        "Respond ONLY with strict JSON using keys: classification (string), reason (string).\n"
        "Keep reason one line and concrete.\n"
        f"LOG = {json.dumps(user_log, ensure_ascii=False)}\n"
        "Example: {\"classification\":\"⏸️ UI Friction\",\"reason\":\"Long hover and misclick near back button.\"}\n"
    )

def _parse_json_safely(text: str) -> Optional[dict]:
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{"); end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                return None
    return None

def _llm_classify_new(client, user_log: str, model: str) -> ClassificationResult:
    try:
        prompt = _structured_prompt(user_log)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a UX pause classifier specialized in Phase Loop Dynamics."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = resp.choices[0].message.content or ""
        data = _parse_json_safely(content)
        if isinstance(data, dict) and "classification" in data:
            return {
                "classification": str(data.get("classification")),
                "reason": str(data.get("reason", "")),
            }
        return {"classification": "⏸️ Classification Failed", "reason": "LLM returned non-JSON or missing keys."}
    except Exception as e:
        return {"classification": "⏸️ Classification Failed", "reason": f"API Error (new): {e}"}

def _llm_classify_legacy(openai_mod, user_log: str, model: str) -> ClassificationResult:
    try:
        prompt = _structured_prompt(user_log)
        resp = openai_mod.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a UX pause classifier specialized in Phase Loop Dynamics."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = resp["choices"][0]["message"]["content"]
        data = _parse_json_safely(content or "")
        if isinstance(data, dict) and "classification" in data:
            return {
                "classification": str(data.get("classification")),
                "reason": str(data.get("reason", "")),
            }
        return {"classification": "⏸️ Classification Failed", "reason": "LLM returned non-JSON or missing keys."}
    except Exception as e:
        err_msg = getattr(e, "message", str(e))
        return {"classification": "⏸️ Classification Failed", "reason": f"API Error (legacy): {err_msg}"}

def classify_pause(user_log: str, use_api: bool = False, model: str = "gpt-4o-mini") -> ClassificationResult:
    """
    Library entry point. If use_api is True and OPENAI_API_KEY is set, uses LLM.
    Otherwise falls back to heuristic.
    """
    if use_api:
        mode, client_or_mod = _get_openai_clients()
        if mode == "new":
            return _llm_classify_new(client_or_mod, user_log, model=model)
        elif mode == "legacy":
            return _llm_classify_legacy(client_or_mod, user_log, model=model)
        # API requested but unavailable -> fallback
        h = _heuristic_classify(user_log)
        h["reason"] = "API key missing. " + h["reason"]
        return h
    else:
        return _heuristic_classify(user_log)

# ---------------- CLI ----------------
def _interactive_loop(use_api: bool, model: str) -> None:
    print("\n--- UX Pause Classifier ---")
    print("Type a user interaction log (or 'exit' to quit):")
    while True:
        try:
            user_input = input("\nLog > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[exit]"); break
        if user_input.lower() in ("exit", "quit"):
            break
        res = classify_pause(user_input, use_api=use_api, model=model)
        print(json.dumps(res, ensure_ascii=False, indent=2))

def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="PLD Pause Classifier")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--local", action="store_true", help="Force local heuristic classification (no API)")
    mode.add_argument("--api", action="store_true", help="Use OpenAI API if OPENAI_API_KEY is set")
    p.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model name (when --api)")
    p.add_argument("--once", type=str, default="", help="Classify a single log string and print JSON")
    args = p.parse_args(argv)

    use_api = bool(args.api)
    if args.once:
        res = classify_pause(args.once, use_api=use_api, model=args.model)
        print(json.dumps(res, ensure_ascii=False))
        return 0

    _interactive_loop(use_api=use_api, model=args.model)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
