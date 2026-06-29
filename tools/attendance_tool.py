from clients.erp_api_client import ERPAPIClient


def get_attendance_details(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()
    selected_student = client.find_student(student_name, class_name)

    if not selected_student:
        return {
            "status": "not_found",
            "message": "Student not found for attendance details.",
        }

    attendance = client.find_by_student_id(
        client.get_attendance(), selected_student["student_id"]
    )

    if not attendance:
        return {
            "status": "not_found",
            "message": "Attendance data not found for this student.",
        }

    return {
        "status": "success",
        "type": "attendance_details",
        "student": selected_student,
        "data": attendance,
    }
