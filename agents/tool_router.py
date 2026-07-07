from tools.student_portfolio_tool import get_student_portfolio
from tools.attendance_tool import get_attendance_details
from tools.fees_outstanding_tool import get_fees_outstanding
from tools.fees_collection_tool import get_fees_collection
from tools.expenses_tool import get_expenses
from tools.exam_report_tool import get_student_exam_report, get_class_exam_report
from tools.enquiry_tool import get_enquiry_report
from tools.admission_tool import get_new_admissions
from tools.communication_tool import get_daily_communication


def route_tool(intent: str, parameters: dict) -> dict:
    if intent == "student_portfolio":
        return get_student_portfolio(parameters)

    if intent == "attendance_details":
        return get_attendance_details(parameters)

    if intent == "fees_outstanding":
        return get_fees_outstanding(parameters)

    if intent == "fees_collection":
        return get_fees_collection(parameters)

    if intent == "expenses":
        return get_expenses(parameters)

    if intent == "student_exam_report":
        return get_student_exam_report(parameters)

    if intent == "class_exam_report":
        return get_class_exam_report(parameters)

    if intent == "enquiry_report":
        return get_enquiry_report(parameters)

    if intent == "new_admission":
        return get_new_admissions(parameters)

    if intent == "daily_communication":
        return get_daily_communication(parameters)

    return {
        "status": "error",
        "message": "No suitable tool found.",
        "parameters": parameters,
    }
