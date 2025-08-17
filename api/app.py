from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import os

# OpenAI SDK (modern client)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="Sentiment API", version="1.0")

from fastapi.middleware.cors import CORSMiddleware

# CORS so the Next.js dev server can call us locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # okay for this challenge
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentIn(BaseModel):
    text: str = Field(..., description="Raw customer product review")

class SentimentOut(BaseModel):
    label: Literal["positive", "neutral", "negative"]
    confidence: float = Field(..., ge=0, le=1)

@app.get("/")
def root():
    return {"message": "Sentiment Analysis API", "version": "1.0", "endpoints": ["/health", "/sentiment"]}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/sentiment", response_model=SentimentOut)
def classify_sentiment(inp: SentimentIn):
    """
    Uses OpenAI with Structured Outputs to force JSON that matches SentimentOut.
    """
    system = "You are a strict sentiment classifier."
    user = f"""Classify the sentiment of the following product review.
Return ONLY JSON with keys: "label" in ["positive","neutral","negative"] and "confidence" (0..1).
Review: {inp.text}"""

    # Structured outputs via chat.completions.parse (SDK provides Pydantic parsing)
    # See: DataCamp tutorial on structured outputs (uses parse with a Pydantic model).
    resp = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",     # as referenced by the challenge repo
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format=SentimentOut
    )
    # parsed object guaranteed to follow SentimentOut
    parsed = resp.choices[0].message.parsed
    return parsed