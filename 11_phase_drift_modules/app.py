# app.py

from fastapi import FastAPI
from phase_wrapper import phase_wrap
import asyncio

app = FastAPI()


@phase_wrap(
    delay_range=(1.0, 3.0),  # artificial delay before response
    timeout=5.0,             # max execution time for the wrapped logic
    fallback_message="(No response. Silence continues…)"  # message when timeout occurs
)
async def mock_openai_call(prompt: str):
    # Simulated external API call (e.g., OpenAI)
    await asyncio.sleep(10)  # deliberately exceeds timeout
    return {"message": f"AI response to: {prompt}"}


@app.get("/ask")
async def ask(prompt: str):
    result = await mock_openai_call(prompt)
    return {"result": result}
