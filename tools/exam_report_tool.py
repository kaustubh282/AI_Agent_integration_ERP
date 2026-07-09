from clients.erp_api_client import ERPAPIClient
from config.settings import settings


def get_student_exam_report(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()
    student = client.find_student(student_name, class_name)

    if not student:
        return {
            "status": "not_found",
            "message": "Student not found for exam report.",
        }

    if settings.ERP_DATA_MODE == "api":
        return {
            "status": "not_found",
            "message": (
                "Student exam report is not available yet from the ERP API. "
                "The marks endpoint is currently returning HTTP 400 or no data. "
                "The correct request payload or ERP endpoint is required."
            ),
        }

    exam = client.find_by_student_id(client.get_exams(), student["student_id"])

    if not exam:
        return {
            "status": "not_found",
            "message": "Exam report not found.",
        }

    return {
        "status": "success",
        "type": "student_exam_report",
        "student": student,
        "data": exam,
    }


def get_class_exam_report(parameters: dict) -> dict:
    class_name = parameters.get("class_name")

    client = ERPAPIClient()

    if settings.ERP_DATA_MODE == "api":
        return {
            "status": "not_found",
            "message": (
                "Class exam report is not available yet from the ERP API. "
                "The current endpoint is returning an empty response. "
                "A valid exam endpoint or request payload is required."
            ),
        }

    students = client.get_students_by_class(class_name)
    exams = client.get_exams()

    records = []

    for student in students:
        exam = client.find_by_student_id(exams, student["student_id"])
        if exam:
            records.append(
                {
                    "student": student,
                    "exam": exam,
                }
            )

    if not records:
        return {
            "status": "not_found",
            "message": "No class exam report found.",
        }

    return {
        "status": "success",
        "type": "class_exam_report",
        "data": records,
    }