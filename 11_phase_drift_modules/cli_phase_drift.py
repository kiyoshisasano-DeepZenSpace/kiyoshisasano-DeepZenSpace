# cli_phase_drift.py

import asyncio
from phase_wrapper import phase_wrap
import openai
import os
import argparse

# Set your OpenAI API key (recommend using env var)
openai.api_key = os.getenv("OPENAI_API_KEY")


@phase_wrap(
    delay_range=(1.5, 3.5),
    timeout=6.0,
    fallback_message="(The machine has chosen silence over speech...)"
)
async def ask_openai(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Phase Drift CLI Prompt")
    parser.add_argument("prompt", type=str, help="Your prompt to OpenAI")
    args = parser.parse_args()

    print("\n[Phase Drift Middleware Activated... Waiting for response...]\n")
    result = asyncio.run(ask_openai(args.prompt))
    print(f"\n[Result]:\n{result}\n")


if __name__ == "__main__":
    main()
