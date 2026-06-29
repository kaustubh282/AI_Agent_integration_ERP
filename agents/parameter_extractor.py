import re


def extract_parameters(message: str) -> dict:
    original_message = message
    message = message.lower()

    parameters = {
        "student_name": None,
        "class_name": None,
        "date_range": None,
        "exam_name": None,
    }

    # class like 8A, 10B, class 5, class 7C
    class_match = re.search(r"(class\s*)?(\d{1,2}\s?[a-zA-Z]?)", original_message)

    if class_match:
        parameters["class_name"] = class_match.group(2).replace(" ", "").upper()

    # date range
    if "today" in message:
        parameters["date_range"] = "today"
    elif "yesterday" in message:
        parameters["date_range"] = "yesterday"
    elif "last week" in message:
        parameters["date_range"] = "last_week"
    elif "last month" in message:
        parameters["date_range"] = "last_month"
    elif "this month" in message:
        parameters["date_range"] = "this_month"

    # exam name
    if "unit test" in message:
        parameters["exam_name"] = "Unit Test"
    elif "mid term" in message or "midterm" in message:
        parameters["exam_name"] = "Mid Term"
    elif "final" in message or "annual" in message:
        parameters["exam_name"] = "Final Exam"

    # Student name extraction
    name_match = re.search(r"show\s+(.+?)\s+class", original_message, re.IGNORECASE)

    if name_match:
        parameters["student_name"] = name_match.group(1).strip()

    return parameters
