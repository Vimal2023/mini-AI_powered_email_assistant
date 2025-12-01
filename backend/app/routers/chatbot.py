from fastapi import APIRouter, Request, HTTPException
from ..database.session_store import get_session
from ..models.token_model import UserSession
from ..services.command_parser import parse_command
from ..services.gmail_service import fetch_last_n_emails
from ..services.ai_service import summarize_email

router = APIRouter(tags=["Chatbot"])

def _get_user_session(request: Request) -> UserSession:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="No session")
    data = get_session(session_id)
    if not data:
        raise HTTPException(status_code=401, detail="Session expired")
    return UserSession(**data)

@router.post("/message")
async def chat_message(request: Request):
    session = _get_user_session(request)
    payload = await request.json()
    user_message: str = payload.get("message", "")

    parsed = parse_command(user_message)

    if parsed["intent"] == "HELP":
        return {
            "type": "HELP",
            "message": (
                "I can help you with:\n"
                "- Read last 5 emails (say 'read my emails')\n"
                "- Suggest replies (say 'suggest replies')\n"
                "- Delete email by number (e.g. 'delete email 2')"
            ),
        }

    if parsed["intent"] == "READ":
        emails = fetch_last_n_emails(session)
        summarized = []
        idx = 1
        for email in emails:
            summary = await summarize_email(email["body"])
            summarized.append(
                {
                    "index": idx,
                    "id": email["id"],
                    "from": email["from"],
                    "subject": email["subject"],
                    "summary": summary,
                }
            )
            idx += 1
        return {"type": "READ", "emails": summarized}

    # For now, other intents can be simply echoed
    return {
        "type": parsed["intent"],
        "message": "Command recognized but not fully implemented yet.",
        "parsed": parsed,
    }
