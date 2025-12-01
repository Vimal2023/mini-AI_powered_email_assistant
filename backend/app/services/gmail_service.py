from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ..config import settings
from ..models.token_model import UserSession

def _build_credentials(session: UserSession) -> Credentials:
    return Credentials(
        token=session.access_token,
        refresh_token=session.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        scopes=[
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.modify",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ],
    )

def get_gmail_service(session: UserSession):
    creds = _build_credentials(session)
    service = build("gmail", "v1", credentials=creds)
    return service

def fetch_last_n_emails(session: UserSession, n: int = 5) -> List[Dict[str, Any]]:
    service = get_gmail_service(session)
    results = service.users().messages().list(userId="me", maxResults=n, labelIds=["INBOX"]).execute()
    messages = results.get("messages", [])

    emails: List[Dict[str, Any]] = []
    for msg in messages:
        msg_full = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
        headers = msg_full.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
        from_ = next((h["value"] for h in headers if h["name"] == "From"), "(unknown sender)")

        # Simple body extraction (text/plain first part)
        body = ""
        parts = msg_full.get("payload", {}).get("parts", [])
        if parts:
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    import base64
                    data = part.get("body", {}).get("data", "")
                    body = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("UTF-8", errors="ignore")
                    break

        emails.append(
            {
                "id": msg["id"],
                "subject": subject,
                "from": from_,
                "body": body,
            }
        )

    return emails

def send_email_reply(session: UserSession, to_email: str, subject: str, body: str) -> None:
    import base64
    from email.mime.text import MIMEText

    service = get_gmail_service(session)

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = "Re: " + subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()

def delete_email(session: UserSession, message_id: str) -> None:
    service = get_gmail_service(session)
    service.users().messages().trash(userId="me", id=message_id).execute()
