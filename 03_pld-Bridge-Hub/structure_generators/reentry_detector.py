# reentry_detector.py
# Detects reentry behavior — when a user resumes a prior intent after interruption

import openai
import os
from typing import TypedDict, List

# 📘 Related Theories:
# - PLD Paper 1: Reentry as return to latent state after drift
# - PLD Paper 2: Segment → Delay → Recombination loop

openai.api_key = os.getenv("OPENAI_API_KEY")

class ReentryResult(TypedDict):
    is_reentry: bool
    reason: str
    matching_segment: str

def detect_reentry(past_segments: List[str], current_input: str) -> ReentryResult:
    prompt = f"""
    Given the following prior interaction segments:

    {past_segments}

    And the current user input:

    "{current_input}"

    Determine whether the current input represents a reentry — i.e., a return to a previously dropped or delayed intent.

    Respond with YES or NO, and briefly explain why. If YES, indicate which past segment it reconnects to.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a structural dialogue analyst specialized in Phase Loop Dynamics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        reply = response['choices'][0]['message']['content']

        if "yes" in reply.lower():
            # Simple heuristic parsing — ideally use structured output
            matching = ""
            for seg in past_segments:
                if seg.lower() in reply.lower():
                    matching = seg
                    break
            return {
                "is_reentry": True,
                "reason": reply,
                "matching_segment": matching
            }
        else:
            return {
                "is_reentry": False,
                "reason": reply,
                "matching_segment": ""
            }
    except openai.error.OpenAIError as e:
        return {
            "is_reentry": False,
            "reason": f"API Error: {str(e)}",
            "matching_segment": ""
        }

# 📚 Related Resources:
# - Zenodo PLD Papers: ../docs/zenodo_paper_links.md
# - Notion Integration: ../notion_ui_templates/
# - Structure Generator Index: ../structure_generators/README_structure_generators.md

if __name__ == "__main__":
    past = [
        "How do I export this as PDF?",
        "Wait, what does 'latency hold' mean again?",
        "Can I try this on mobile?"
    ]
    new_input = "Actually, about the latency thing... is that why it paused?"

    result = detect_reentry(past, new_input)
    print("🌀 Reentry Detection Result:")
    print(result)
