import re


def normalize_class_name(value: str | None):
    if not value:
        return None

    value = value.strip().upper()
    value = value.replace("_", "-")
    value = re.sub(r"\s+", "-", value)

    return value


def extract_parameters(message: str) -> dict:
    original_message = message
    message_lower = message.lower()

    parameters = {
        "student_name": None,
        "class_name": None,
        "date_range": None,
        "exam_name": None,
    }

    # Date range
    if "today" in message_lower:
        parameters["date_range"] = "today"
    elif "yesterday" in message_lower:
        parameters["date_range"] = "yesterday"
    elif "last week" in message_lower:
        parameters["date_range"] = "last_week"
    elif "last month" in message_lower:
        parameters["date_range"] = "last_month"
    elif "this month" in message_lower:
        parameters["date_range"] = "this_month"

    # Exam name
    if "unit test" in message_lower:
        parameters["exam_name"] = "Unit Test"
    elif "mid term" in message_lower or "midterm" in message_lower:
        parameters["exam_name"] = "Mid Term"
    elif "final" in message_lower or "annual" in message_lower:
        parameters["exam_name"] = "Final Exam"

    # Class extraction examples:
    # JRKG, JRKG-A, jrkg a, SRKG-A, Nursery, I-A, II-B, class I-A
    class_patterns = [
        r"\b(?:class\s+)?(nursery(?:[-_\s]?[a-z])?)\b",
        r"\b(?:class\s+)?(jrkg(?:[-_\s]?[a-z])?)\b",
        r"\b(?:class\s+)?(srkg(?:[-_\s]?[a-z])?)\b",
        r"\b(?:class\s+)?((?:i|ii|iii|iv|v|vi|vii|viii|ix|x)(?:[-_\s]?[a-z])?)\b",
        r"\b(?:class\s+)?(\d{1,2}(?:[-_\s]?[a-z])?)\b",
    ]

    for pattern in class_patterns:
        class_match = re.search(pattern, original_message, re.IGNORECASE)
        if class_match:
            parameters["class_name"] = normalize_class_name(class_match.group(1))
            break

    # Student name extraction
    name_patterns = [
        r"of\s+(.+?)\s+from\s+",
        r"for\s+(.+?)\s+from\s+",
        r"of\s+(.+?)\s+class\s+",
        r"for\s+(.+?)\s+class\s+",
        r"student\s+portfolio\s+of\s+(.+)$",
        r"attendance\s+of\s+(.+)$",
        r"exam\s+report\s+of\s+(.+)$",
    ]

    for pattern in name_patterns:
        name_match = re.search(pattern, original_message, re.IGNORECASE)
        if name_match:
            parameters["student_name"] = name_match.group(1).strip()
            break

    return parameters
