from clients.erp_api_client import ERPAPIClient
from config.settings import settings


def get_daily_communication(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()

    if settings.ERP_DATA_MODE == "api":
        if student_name:
            student = client.find_student(student_name, class_name)

            if not student:
                return {
                    "status": "not_found",
                    "message": "Student not found for communication details.",
                }

        return {
            "status": "not_found",
            "message": (
                "Daily communication data is not available yet from the ERP API. "
                "The frontend code shows save APIs for homework, notice, and circulars, "
                "but the required GET APIs for reading communication data are not confirmed yet."
            ),
        }

    if student_name and class_name:
        student = client.find_student(student_name, class_name)

        if not student:
            return {
                "status": "not_found",
                "message": "Student not found for communication details.",
            }

        communication = client.find_by_student_id(
            client.get_communication(), student["student_id"]
        )

        if not communication:
            return {
                "status": "not_found",
                "message": "No communication found for this student.",
            }

        return {
            "status": "success",
            "type": "daily_communication",
            "student": student,
            "data": [communication],
        }

    return {
        "status": "success",
        "type": "daily_communication",
        "data": client.get_communication(),
    }
