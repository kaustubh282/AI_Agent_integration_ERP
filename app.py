import logging

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from agents.llm_parser import parse_user_message
from agents.response_formatter import format_response
from agents.tool_router import route_tool
from core.exceptions import ERPAgentError, ERPAPIError, ERPValidationError
from core.security import sanitize_message, sanitize_parameters, verify_api_key

load_dotenv()

logger = logging.getLogger(__name__)

app = FastAPI(title="ERP AI Agent")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    user_id: str | None = Field(default=None, max_length=100)
    role: str | None = Field(default=None, max_length=50)
    school_id: str | None = Field(default=None, max_length=100)

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        return sanitize_message(value)

    @field_validator("user_id", "role", "school_id")
    @classmethod
    def validate_optional_fields(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


@app.get("/")
def home():
    return {"message": "ERP Agent API is running"}


@app.exception_handler(ERPValidationError)
async def handle_validation_error(_: Request, exc: ERPValidationError):
    return JSONResponse(
        status_code=400,
        content={"reply": str(exc), "error_type": "validation_error"},
    )


@app.exception_handler(ERPAPIError)
async def handle_api_error(_: Request, exc: ERPAPIError):
    logger.error("ERP API error: %s", exc)
    return JSONResponse(
        status_code=503,
        content={
            "reply": "Unable to fetch ERP data right now. Please try again later.",
            "error_type": "erp_unavailable",
        },
    )


@app.exception_handler(ERPAgentError)
async def handle_agent_error(_: Request, exc: ERPAgentError):
    logger.error("Agent error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "reply": "Something went wrong while processing your request.",
            "error_type": "agent_error",
        },
    )


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "reply": "Invalid request format.",
            "error_type": "request_validation_error",
        },
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(_: Request, exc: Exception):
    logger.exception("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "reply": "Something went wrong while processing your request.",
            "error_type": "internal_error",
        },
    )


@app.post("/chat")
def chat(request: ChatRequest):
    parsed = parse_user_message(request.message)

    intent = parsed["intent"]
    parameters = sanitize_parameters(parsed["parameters"])

    tool_result = route_tool(intent, parameters)
    formatted_response = format_response(tool_result)

    return {
        "user_message": request.message,
        "detected_intent": intent,
        "parameters": parameters,
        "reply": formatted_response,
    }
