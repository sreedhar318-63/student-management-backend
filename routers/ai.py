import os

from fastapi import APIRouter, HTTPException
from fastapi  import APIRouter ,Depends, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dependencies import get_current_user
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(prefix="/ai", tags=["AI"])
if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINIAPI_KEY is not set in .env")
client=genai.Client()
MODEL_NAME="gemini-3.1-flash-lite"
GENERATION_CONFIG=types.GenerateContentConfig(
    temperature=2.0,
    max_output_tokens=512,
)
SYSTEM_CONTEXT="""You are a helpful programming assistant for college
students learning Python full stack development. Explain concepts clearly
and concisely using simple real-world analogies. Use short code examples
when helpful. Keep answers beginner-friendly and under 200 words unless
the question genuinely requires more detail."""

class ChatMessage(BaseModel):
    role: str
    text: str


class AskRequest(BaseModel):
    messages: list[ChatMessage]

class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse)
def ask_ai(
    request: AskRequest,
    current_user=Depends(get_current_user)   
):
    contents = []
    for msg in request.messages:
        role = "user" if msg.role == "user" else "model"
        contents.append(
            types.Content(role=role, parts=[types.Part.from_text(text=msg.text)])
        )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=2.0,
                max_output_tokens=512,
                system_instruction=SYSTEM_CONTEXT
            ),
        )
        return AskResponse(answer=response.text)

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="This question could not be answered. Please rephrase it."
        )
    except Exception as e:
        print(f"Gemini error: {e}")   
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Try again in a moment."
        )


