from clients.erp_api_client import ERPAPIClient


def get_fees_outstanding(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()

    if student_name and class_name:
        selected_student = client.find_student(student_name, class_name)

        if not selected_student:
            return {
                "status": "not_found",
                "message": "Student not found with given name and class.",
            }

        fees = client.find_by_student_id(
            client.get_fees(), selected_student["student_id"]
        )

        if not fees or fees["outstanding_fees"] <= 0:
            return {
                "status": "not_found",
                "message": "No outstanding fees for this student.",
            }

        return {
            "status": "success",
            "type": "fees_outstanding",
            "data": [{"student": selected_student, "fees": fees}],
        }

    records = client.get_students_with_outstanding_fees(class_name)

    if not records:
        message = (
            f"No outstanding fees found for class {class_name}."
            if class_name
            else "No outstanding fees found."
        )
        return {"status": "not_found", "message": message}

    return {
        "status": "success",
        "type": "fees_outstanding",
        "data": records,
    }
