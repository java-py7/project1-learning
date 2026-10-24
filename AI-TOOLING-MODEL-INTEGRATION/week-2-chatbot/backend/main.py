import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from openai import APIError as OpenAIAPIError
from google import genai
from google.genai import errors as gemini_errors
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(title="Simple AI Chatbot API")

# Allow the local frontend to communicate with the backend.
# Restrict this to your frontend origin when deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "https://simplechatbot-v1.vercel.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    provider: str = "openai"


class ChatResponse(BaseModel):
    reply: str
    provider: str


@app.get("/")
def home():
    return {"message": "AI Chatbot API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty or whitespace."
        )

    provider = request.provider.lower().strip()

    if provider not in {"openai", "gemini"}:
        raise HTTPException(
            status_code=400,
            detail="Provider must be 'openai' or 'gemini'."
        )

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="OpenAI API key is not configured."
            )

        try:
            client = OpenAI(api_key=api_key, timeout=20.0)
            result = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                input=message,
            )

            reply = result.output_text

        except OpenAIAPIError:
            raise HTTPException(
                status_code=502,
                detail="The OpenAI provider request failed."
            ) from None
        except Exception:
            raise HTTPException(
                status_code=502,
                detail="An unexpected error occurred while contacting OpenAI."
            ) from None

    else:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="Gemini API key is not configured."
            )

        try:
            client = genai.Client(api_key=api_key)
            result = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                contents=message,
                config={"http_options": {"timeout": 20000}},
            )

            reply = result.text

        except gemini_errors.APIError:
            raise HTTPException(
                status_code=502,
                detail="The Gemini provider request failed."
            ) from None
        except Exception:
            raise HTTPException(
                status_code=502,
                detail="An unexpected error occurred while contacting Gemini."
            ) from None

    if not reply:
        raise HTTPException(
            status_code=502,
            detail="The provider returned an empty response."
        )

    return ChatResponse(reply=reply, provider=provider)
