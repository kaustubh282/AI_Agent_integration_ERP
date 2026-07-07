from clients.erp_api_client import ERPAPIClient


def get_student_exam_report(parameters: dict) -> dict:
    student_name = parameters.get("student_name")
    class_name = parameters.get("class_name")

    client = ERPAPIClient()
    student = client.find_student(student_name, class_name)

    if not student:
        return {"status": "not_found", "message": "Student not found for exam report."}

    exam = client.find_by_student_id(client.get_exams(), student["student_id"])

    if not exam:
        return {"status": "not_found", "message": "Exam report not found."}

    return {
        "status": "success",
        "type": "student_exam_report",
        "student": student,
        "data": exam,
    }


def get_class_exam_report(parameters: dict) -> dict:
    class_name = parameters.get("class_name")

    client = ERPAPIClient()
    students = client.get_students_by_class(class_name)
    exams = client.get_exams()

    records = []

    for student in students:
        exam = client.find_by_student_id(exams, student["student_id"])
        if exam:
            records.append({"student": student, "exam": exam})

    if not records:
        return {"status": "not_found", "message": "No class exam report found."}

    return {
        "status": "success",
        "type": "class_exam_report",
        "data": records,
    }
