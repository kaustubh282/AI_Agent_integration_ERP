ROLE_PERMISSIONS = {
    "admin": [
        "student_portfolio",
        "attendance_details",
        "fees_outstanding",
        "fees_collection",
        "expenses",
        "student_exam_report",
        "class_exam_report",
        "enquiry_report",
        "new_admission",
        "daily_communication",
    ],
    "teacher": [
        "student_portfolio",
        "attendance_details",
        "student_exam_report",
        "class_exam_report",
        "daily_communication",
    ],
    "parent": [
        "student_portfolio",
        "attendance_details",
        "fees_outstanding",
        "student_exam_report",
        "daily_communication",
    ],
    "student": [
        "student_portfolio",
        "attendance_details",
        "student_exam_report",
        "daily_communication",
    ],
}


def is_allowed(role: str, intent: str) -> bool:
    if not role or not intent:
        return False

    role = role.lower()
    allowed_intents = ROLE_PERMISSIONS.get(role, [])

    return intent in allowed_intents
