from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi.responses import FileResponse

# --- Force load the correct .env from project root ---

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("OPENAI_API_KEY")

print("DEBUG: Loaded OPENAI_API_KEY from:", ENV_PATH)
print("DEBUG: OPENAI_API_KEY starts with:", API_KEY[:12] if API_KEY else "None")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=API_KEY)

# --- FastAPI setup ---

app = FastAPI(title="Supportive Mental Coach")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        user_message = request.message

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a supportive mental coach. "
                        "Help users manage stress, emotions, and motivation. "
                        "Be kind, concise, and practical. "
                        "Response MUST be concise and less than 600 words"
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling OpenAI API: {str(e)}"
        )
