from fastapi import APIRouter, Request, HTTPException
from ..database.session_store import get_session
from ..models.token_model import UserSession
from ..services.gmail_service import fetch_last_n_emails, send_email_reply, delete_email
from ..services.ai_service import summarize_email, generate_reply

router = APIRouter(tags=["Gmail"])

def _get_user_session(request: Request) -> UserSession:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="No session")
    data = get_session(session_id)
    if not data:
        raise HTTPException(status_code=401, detail="Session expired")
    return UserSession(**data)

@router.get("/read")
async def read_last_5(request: Request):
    session = _get_user_session(request)
    emails = fetch_last_n_emails(session)

    summarized = []
    index = 1
    for email in emails:
        summary = await summarize_email(email["body"])
        summarized.append(
            {
                "index": index,
                "id": email["id"],
                "from": email["from"],
                "subject": email["subject"],
                "summary": summary,
            }
        )
        index += 1

    return {"emails": summarized}

@router.post("/generate-replies")
async def generate_replies(request: Request):
    session = _get_user_session(request)
    body = await request.json()
    emails = body.get("emails", [])
    results = []

    for email in emails:
        reply = await generate_reply(
            subject=email["subject"],
            body=email.get("body", ""),
            user_intent=email.get("user_intent", ""),
        )
        results.append(
            {
                "id": email["id"],
                "to": email["from"],
                "subject": email["subject"],
                "reply": reply,
            }
        )
    return {"replies": results}

@router.post("/send")
async def send_reply(request: Request):
    session = _get_user_session(request)
    payload = await request.json()
    to_email = payload["to"]
    subject = payload["subject"]
    body = payload["body"]

    send_email_reply(session, to_email, subject, body)
    return {"detail": "Email sent"}

@router.post("/delete")
async def delete_email_route(request: Request):
    session = _get_user_session(request)
    payload = await request.json()
    message_id = payload["id"]
    delete_email(session, message_id)
    return {"detail": "Email deleted"}
