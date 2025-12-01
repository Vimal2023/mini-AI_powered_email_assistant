import google.generativeai as genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def call_gemini(prompt: str):
    res = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return res.text

async def summarize_email(body: str):
    prompt = f"Summarize this email in 2 lines:\n\n{body}"
    return call_gemini(prompt)

async def generate_reply(body: str):
    prompt = f"Write a professional reply to this email:\n\n{body}\n\nReply:"
    return call_gemini(prompt)
