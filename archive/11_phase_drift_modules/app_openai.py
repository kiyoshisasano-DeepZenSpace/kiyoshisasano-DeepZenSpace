# app_openai.py

from fastapi import FastAPI
from pydantic import BaseModel
from phase_wrapper import phase_wrap
import openai
import os
import asyncio

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@phase_wrap(
    delay_range=(1.0, 2.5),
    timeout=7.0,
    fallback_message="(The response has faded into structured silence...)"
)
async def call_openai(prompt: str) -> str:
    # Minimal OpenAI Chat Completion call
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


@app.post("/ask")
async def ask_openai(request: PromptRequest):
    result = await call_openai(request.prompt)
    return {"result": result}
