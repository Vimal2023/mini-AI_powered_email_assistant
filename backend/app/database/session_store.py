from typing import Dict, Any
from datetime import datetime, timedelta

# In-memory session store: session_id -> data
_sessions: Dict[str, Dict[str, Any]] = {}

SESSION_TTL_HOURS = 8

def save_session(session_id: str, data: Dict[str, Any]) -> None:
    _sessions[session_id] = {
        **data,
        "expires_at": datetime.utcnow() + timedelta(hours=SESSION_TTL_HOURS),
    }

def get_session(session_id: str) -> Dict[str, Any] | None:
    session = _sessions.get(session_id)
    if not session:
        return None
    if session["expires_at"] < datetime.utcnow():
        # expired
        _sessions.pop(session_id, None)
        return None
    return session

def delete_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
