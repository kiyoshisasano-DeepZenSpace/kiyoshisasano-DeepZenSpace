"""
pause_classifier_bot.py

A lightweight GPT-powered classifier that labels user pauses in UX interactions.
Classifies pause types such as Cognitive, UI Friction, Disengagement, Repair, and Latency Hold.
Supports both command-line and Colab-style usage.

📚 Related Resources:
- PLD Theory: ../docs/zenodo_paper_links.md
- Notion Template: ../notion_ui_templates/README_notion_ui_templates.md
- Bot Integration Guide: ../structure_generators/README_structure_generators.md

⚠️ Usage Note:
Set your OpenAI API key as environment variable:
`export OPENAI_API_KEY="sk-..."` (Linux/Mac)
`set OPENAI_API_KEY="sk-..."` (Windows)
"""

import os
import openai
from typing import TypedDict

# Environment variable API key usage
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("⚠️ Warning: OPENAI_API_KEY not set. See configuration guide.")

class ClassificationResult(TypedDict):
    classification: str
    reason: str

PAUSE_TYPES = [
    "⏸️ Cognitive",      # PLD Paper1: Latency-driven phase shift
    "⏸️ UI Friction",    # PLD Paper2: Forced drift by interface
    "⏸️ Disengagement",  # PLD Paper1: Unrepaired drift (see also: Recombination failure in Paper2)
    "⏸️ Repair",         # PLD Paper2: Cue-triggered realignment
    "⏸️ Latency Hold"    # PLD Paper1: Intentional pause
]

SYSTEM_PROMPT = f"""
You are a UX diagnosis assistant (Part of Phase Loop Dynamics system).

Your task is to classify the type of pause detected in user interaction logs.
Based on timing, content, and context, assign one of the following categories:
{', '.join(PAUSE_TYPES)}

Expected Input Patterns:
- Mouse/touch inactivity > {PAUSE_TYPES[0]} or {PAUSE_TYPES[4]}
- Repeated back-and-forth > {PAUSE_TYPES[1]}
- Session abandonment > {PAUSE_TYPES[2]}
- Correction behaviors > {PAUSE_TYPES[3]}

Also, provide a one-line reasoning for your classification.
"""

def classify_pause(user_log: str) -> ClassificationResult:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Interaction log: {user_log}"}
            ],
            temperature=0.3
        )
        reply = response["choices"][0]["message"]["content"]
        return {
            "classification": reply.split('\n')[0],
            "reason": '\n'.join(reply.split('\n')[1:]).strip()
        }
    except openai.error.OpenAIError as e:
        return {
            "classification": "⏸️ Classification Failed",
            "reason": f"API Error: {str(e)}"
        }

if __name__ == "__main__":
    print("\n--- UX Pause Classifier ---")
    print("Type a user interaction log (or 'exit' to quit):")
    while True:
        user_input = input("\nLog > ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = classify_pause(user_input)
        print(f"\n🧠 Classification: {result['classification']}\n💬 Reason: {result['reason']}")
