from tools.student_portfolio_tool import get_student_portfolio
from tools.attendance_tool import get_attendance_details
from tools.fees_outstanding_tool import get_fees_outstanding
from tools.fees_collection_tool import get_fees_collection


def route_tool(intent: str, parameters: dict) -> dict:
    if intent == "student_portfolio":
        return get_student_portfolio(parameters)

    if intent == "attendance_details":
        return get_attendance_details(parameters)

    if intent == "fees_outstanding":
        return get_fees_outstanding(parameters)

    if intent == "fees_collection":
        return get_fees_collection(parameters)

    return {
        "status": "error",
        "message": "No suitable tool found.",
        "parameters": parameters,
    }
