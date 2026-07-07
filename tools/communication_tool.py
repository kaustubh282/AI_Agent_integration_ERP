from clients.erp_api_client import ERPAPIClient


def get_daily_communication(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()

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
