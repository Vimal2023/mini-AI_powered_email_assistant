from pydantic import BaseModel

class UserSession(BaseModel):
    email: str
    name: str | None = None
    picture: str | None = None
    access_token: str
    refresh_token: str | None = None
    token_type: str | None = None
    expiry: int | None = None
