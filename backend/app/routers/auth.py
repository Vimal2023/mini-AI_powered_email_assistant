from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from uuid import uuid4
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import requests as http_requests

from ..config import settings
from ..database.session_store import save_session, get_session, delete_session
from ..models.token_model import UserSession

router = APIRouter(tags=["Auth"])

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

@router.get("/google/login-url")
def google_login_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return {"url": auth_url}

@router.get("/google/callback")
def google_callback(request: Request, code: str | None = None):
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        },
        scopes=SCOPES,
    )
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Get user info
    userinfo_response = http_requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {credentials.token}"},
        timeout=10,
    )
    userinfo = userinfo_response.json()

    user_session = UserSession(
        email=userinfo.get("email"),
        name=userinfo.get("name"),
        picture=userinfo.get("picture"),
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
        token_type=credentials.token_uri,
        expiry=int(credentials.expiry.timestamp()) if credentials.expiry else None,
    )

    session_id = str(uuid4())
    save_session(session_id, user_session.dict())

    response = RedirectResponse(url="http://localhost:3000/dashboard")
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # set True on production HTTPS
        samesite="lax",
    )
    return response

@router.get("/me")
def get_me(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="No session")

    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Session expired")

    return {
        "email": session["email"],
        "name": session.get("name"),
        "picture": session.get("picture"),
    }

@router.post("/logout")
def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)
    response = JSONResponse({"detail": "Logged out"})
    response.delete_cookie("session_id")
    return response
