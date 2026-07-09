import os
import re

from fastapi import Header, HTTPException

from core.exceptions import ERPValidationError

MAX_MESSAGE_LENGTH = 2000
MAX_NAME_LENGTH = 100

ALLOWED_DATE_RANGES = {
    "today",
    "yesterday",
    "last_week",
    "last_month",
    "this_month",
}

# Flexible ERP class format:
# 8, 8A, 8-A, JRKG, JRKG-A, SRKG-A, Nursery-A, I-A, II-B, X
CLASS_NAME_PATTERN = re.compile(
    r"^(NURSERY|JRKG|SRKG|I|II|III|IV|V|VI|VII|VIII|IX|X|\d{1,2})(-[A-Z])?$",
    re.IGNORECASE,
)

STUDENT_NAME_PATTERN = re.compile(r"^[\w\s.\-'()]+$", re.UNICODE)
CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def sanitize_message(message: str) -> str:
    if not isinstance(message, str):
        raise ERPValidationError("Message must be a text value.")

    cleaned = CONTROL_CHAR_PATTERN.sub("", message).strip()

    if not cleaned:
        raise ERPValidationError("Message cannot be empty.")

    if len(cleaned) > MAX_MESSAGE_LENGTH:
        raise ERPValidationError(
            f"Message is too long. Maximum {MAX_MESSAGE_LENGTH} characters allowed."
        )

    return cleaned


def normalize_class_name(class_name: str) -> str:
    class_name = CONTROL_CHAR_PATTERN.sub("", str(class_name)).strip().upper()
    class_name = class_name.replace("_", "-")
    class_name = re.sub(r"\s+", "-", class_name)

    return class_name


def sanitize_parameters(parameters: dict) -> dict:
    sanitized = dict(parameters)

    class_name = sanitized.get("class_name")
    if class_name is not None:
        class_name = normalize_class_name(class_name)

        if not CLASS_NAME_PATTERN.match(class_name):
            raise ERPValidationError("Invalid class name format.")

        sanitized["class_name"] = class_name

    student_name = sanitized.get("student_name")
    if student_name is not None:
        student_name = CONTROL_CHAR_PATTERN.sub("", str(student_name)).strip()

        if not student_name:
            sanitized["student_name"] = None
        elif len(student_name) > MAX_NAME_LENGTH:
            raise ERPValidationError("Student name is too long.")
        elif not STUDENT_NAME_PATTERN.match(student_name):
            raise ERPValidationError("Student name contains invalid characters.")
        else:
            sanitized["student_name"] = student_name

    date_range = sanitized.get("date_range")
    if date_range is not None and date_range not in ALLOWED_DATE_RANGES:
        raise ERPValidationError("Invalid date range.")

    exam_name = sanitized.get("exam_name")
    if exam_name is not None:
        sanitized["exam_name"] = CONTROL_CHAR_PATTERN.sub("", str(exam_name)).strip()

    return sanitized


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected_key = os.getenv("AGENT_API_KEY")

    if not expected_key:
        return

    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
