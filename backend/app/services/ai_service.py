import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def call_gemini(prompt: str):
    response = genai.generate(
        model="gemini-pro",
        prompt=prompt
    )
    return response.text

async def summarize_email(body: str):
    prompt = f"Summarize this email in 2 lines:\n\n{body}"
    return call_gemini(prompt)

async def generate_reply(body: str):
    prompt = f"Write a professional reply to this email:\n\n{body}\n\nReply:"
    return call_gemini(prompt)
