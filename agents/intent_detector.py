def detect_intent(message: str) -> str:
    message = message.lower()

    if any(word in message for word in ["portfolio", "profile", "full details", "complete details", "student information", "students details", "student profile"]):
        return "student_portfolio"

    if any(word in message for word in ["attendance", "present", "absent", "leave", "total attendance", "total absent", "total present", "total leave", "present details", "absent details"]):
        return "attendance_details"

    if any(word in message for word in ["fee collection", "fees overview", "fees analysis", "fees collection", "collected fees", "payment received", "fees received", "school fees collection"]):
        return "fees_collection"

    if any(word in message for word in ["fees pending", "fee pending", "outstanding", "dues", "balance fees", "fees defaulter"]):
        return "fees_outstanding"

    if any(word in message for word in ["expense", "expenses", "spent", "expenditure"]):
        return "expenses"

    if any(word in message for word in ["exam", "marks", "result", "report card", "student marks"]):
        if any(word in message for word in ["class report", "full class", "whole class"]):
            return "class_exam_report"
        return "student_exam_report"

    if any(word in message for word in ["admission", "new admission", "admitted"]):
        return "new_admission"

    if any(word in message for word in ["enquiry", "inquiry", "lead", "follow up"]):
        return "enquiry_report"

    if any(word in message for word in ["homework", "notice", "circular", "communication", "chart", "daily notice"]):
        return "daily_communication"

    return "unknown"