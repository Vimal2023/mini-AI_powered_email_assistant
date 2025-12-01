import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_CLIENT_ID: str | None = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str | None = os.getenv("GOOGLE_REDIRECT_URI")
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    ENCRYPTION_KEY: str | None = os.getenv("ENCRYPTION_KEY")

settings = Settings()
