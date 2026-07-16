from clients.erp_api_client import ERPAPIClient


def get_student_portfolio(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    if not student_name:
        return {
            "status": "validation_error",
            "message": "Please mention the student name for the portfolio.",
        }

    client = ERPAPIClient()

    selected_student = client.find_student(
        student_name,
        class_name,
    )

    if not selected_student:
        return {
            "status": "not_found",
            "message": "Student not found for the given name and class.",
        }

    student_id = selected_student["student_id"]

    attendance = client.find_by_student_id(
        client.get_attendance(),
        student_id,
    )
    fees = client.find_by_student_id(
        client.get_fees(),
        student_id,
    )
    exams = client.find_by_student_id(
        client.get_exams(),
        student_id,
    )
    communication = client.find_by_student_id(
        client.get_communication(),
        student_id,
    )

    return {
        "status": "success",
        "type": "student_portfolio",
        "data": {
            "basic_details": selected_student,
            "attendance": attendance,
            "fees": fees,
            "exams": exams,
            "communication": communication,
        },
    }
