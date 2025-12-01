from fastapi import Request
from fastapi.responses import JSONResponse
from .logger import logger

async def http_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on the server."},
    )
