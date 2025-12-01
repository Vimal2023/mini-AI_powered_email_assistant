from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .routers import auth, gmail, chatbot
from .utils.error_handler import http_error_handler

app = FastAPI(title="Constructure AI Email Assistant API")

origins = [
    "http://localhost:3000",  # frontend dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(gmail.router, prefix="/gmail")
app.include_router(chatbot.router, prefix="/chat")

@app.get("/")
def root():
    return {"status": "ok"}

# generic error handler
app.add_exception_handler(Exception, http_error_handler)
