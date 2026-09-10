from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers.employee_router import router as employee_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Personal Details API (FastAPI)",
    version="1.0.0",
    lifespan=lifespan
)

raw_client_url = settings.CLIENT_URL or "http://localhost:5173"
allowed_origins = [url.strip().rstrip('/') for url in raw_client_url.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(employee_router)

@app.get("/", response_model=None)
async def root():
    return {"success": True, "message": "Personal Details API is running."}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    sanitized_errors = []
    for error in exc.errors():
        msg = error.get("msg", "Invalid value")
        if msg.startswith("Value error, "):
            msg = msg[len("Value error, "):]
        error_messages.append(msg)
        
        safe_error = {k: v for k, v in error.items() if k != "ctx"}
        if "ctx" in error:
            safe_error["ctx"] = {k: str(v) for k, v in error["ctx"].items()}
        sanitized_errors.append(safe_error)
    
    combined_message = ", ".join(error_messages)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"success": False, "message": combined_message, "errors": sanitized_errors}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] {request.method} {request.url.path} — {str(exc)}")
    message = "Internal Server Error" if settings.NODE_ENV == "production" else str(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": message}
    )
