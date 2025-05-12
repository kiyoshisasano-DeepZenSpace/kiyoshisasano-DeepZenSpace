Phase Drift Middleware – Usage Guide (Plain Text Version)
=========================================================

This guide describes how to use each file in the Phase Drift Middleware project.
It includes instructions for running the API servers, CLI tool, and unit tests.

------------------------------
1. phase_wrapper.py (Core)
------------------------------
This file contains the core decorator `@phase_wrap`, which enables:

- Randomized delay before response
- Timeout handling with a fallback message or function
- Logging of drift behavior in JSON format
- Support for both sync and async functions

This module is NOT run directly. It is imported by other scripts like app.py, app_openai.py, etc.

------------------------------
2. app.py (Mocked FastAPI Server)
------------------------------
A simple FastAPI app using `@phase_wrap` on a mocked function that simulates latency.

To run:

  uvicorn app:app --reload

To test:

  curl "http://localhost:8000/ask?prompt=Hello"

Expected behavior:

- 1–3 seconds delay before response
- Forced timeout after 5 seconds
- Returns fallback message if timeout occurs

------------------------------
3. app_openai.py (Real OpenAI Integration)
------------------------------
A FastAPI server that calls OpenAI’s Chat API, wrapped with `@phase_wrap`.

Prerequisites:

  pip install openai fastapi uvicorn
  export OPENAI_API_KEY="your-api-key-here"

To run:

  uvicorn app_openai:app --reload

To test:

  curl -X POST http://localhost:8000/ask \
       -H "Content-Type: application/json" \
       -d '{"prompt": "Explain mono no aware."}'

Expected behavior:

- Adds delay before OpenAI call
- If OpenAI takes too long, returns a fallback message
- Behavior is logged in phase_drift_log.json

------------------------------
4. cli_phase_drift.py (Command-Line Interface)
------------------------------
A CLI wrapper for OpenAI that uses `@phase_wrap`.

Setup:

  pip install openai
  export OPENAI_API_KEY="your-api-key-here"

To use:

  python cli_phase_drift.py "What is wabi-sabi?"

Expected behavior:

- Adds delay before response
- Times out after 6 seconds
- Returns fallback if OpenAI is too slow

------------------------------
5. test_phase_wrapper.py (Unit Tests with pytest)
------------------------------
Tests the behavior of the `@phase_wrap` decorator.

To install test dependencies:

  pip install pytest pytest-asyncio

To run tests:

  pytest test_phase_wrapper.py

What is tested:

- Sync and async functions complete successfully within timeout
- Timeout triggers fallback message
- JSON log is correctly written with metadata

------------------------------
6. phase_drift_log.json (Log Output)
------------------------------
Each call wrapped with `@phase_wrap` logs JSON like this:

  {
    "timestamp": "2025-05-12 14:00:02",
    "delay_seconds": 2.14,
    "timeout_seconds": 6.0,
    "silence_used": true,
    "elapsed_time": 6.03
  }

The file grows with each request. You can use it for analytics or debugging.

------------------------------
Philosophical Intent
------------------------------
This middleware enforces a conceptual layer of latency, hesitation, or silence in AI responses.

It's designed for:
- UX designers exploring delay and anticipation
- Conversational AI systems where structured quiet matters
- Developers seeking to challenge "instant gratification" paradigms

-----------------------------------------------------
End of Guide
-----------------------------------------------------
