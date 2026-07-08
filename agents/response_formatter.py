def format_response(tool_result: dict) -> str:
    if tool_result["status"] != "success":
        return tool_result.get("message", "No data found.")

    response_type = tool_result.get("type")

    if response_type == "attendance_details":
        student = tool_result["student"]
        attendance = tool_result["data"]

        return f"""
Attendance Details

Name : {student['name']}
Class : {student['class_name']}
Roll Number : {student['roll_number']}

Present Days : {attendance['present_days']}
Absent Days : {attendance['absent_days']}
Attendance Percentage : {attendance['attendance_percentage']}%
""".strip()

    if response_type == "fees_outstanding":
        lines = ["Fees Outstanding Report", ""]

        for record in tool_result["data"]:
            student = record["student"]
            fees = record["fees"]

            lines.extend(
                [
                    f"Name : {student['name']}",
                    f"Class : {student['class_name']}",
                    f"Roll Number : {student['roll_number']}",
                    f"Total Fees : ₹{fees['total_fees']}",
                    f"Paid Fees : ₹{fees['paid_fees']}",
                    f"Outstanding Fees : ₹{fees['outstanding_fees']}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "fees_collection":
        data = tool_result["data"]

        lines = [
            "Fees Collection Report",
            "",
            f"Date Range : {data.get('date_range', 'all')}",
            f"Class : {data.get('class_name') or 'All'}",
            f"Total Collected : ₹{data.get('total_collected', 0)}",
            f"Payment Count : {data.get('payment_count', 0)}",
            "",
            "Payments",
        ]

        for record in data.get("records", []):
            lines.extend(
                [
                    f"- {record.get('student_name', 'Unknown')} | Class {record.get('class_name')} | ₹{record.get('amount')} | {record.get('date')} | {record.get('mode')}"
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "expenses":
        lines = ["Expenses Report", ""]

        for expense in tool_result["data"]:
            lines.extend(
                [
                    f"Date : {expense.get('date')}",
                    f"Category : {expense.get('category')}",
                    f"Description : {expense.get('description')}",
                    f"Amount : ₹{expense.get('amount')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "enquiry_report":
        lines = ["Enquiry Report", ""]

        for enquiry in tool_result["data"]:
            lines.extend(
                [
                    f"Name : {enquiry.get('student_name')}",
                    f"Class Interested : {enquiry.get('class_name')}",
                    f"Parent : {enquiry.get('parent_name')}",
                    f"Contact : {enquiry.get('contact_number')}",
                    f"Date : {enquiry.get('date')}",
                    f"Status : {enquiry.get('status')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "new_admission":
        lines = ["New Admissions Report", ""]

        for admission in tool_result["data"]:
            lines.extend(
                [
                    f"Student Name : {admission.get('student_name')}",
                    f"Class : {admission.get('class_name')}",
                    f"Admission Date : {admission.get('admission_date')}",
                    f"Parent : {admission.get('parent_name')}",
                    f"Contact : {admission.get('contact_number')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "student_exam_report":
        student = tool_result["student"]
        exam = tool_result["data"]

        return f"""
Student Exam Report

Name : {student['name']}
Class : {student['class_name']}
Roll Number : {student['roll_number']}

Exam : {exam.get('exam_name')}
Percentage : {exam.get('percentage')}%
Grade : {exam.get('grade')}
""".strip()

    if response_type == "class_exam_report":
        lines = ["Class Exam Report", ""]

        for record in tool_result["data"]:
            student = record["student"]
            exam = record["exam"]

            lines.extend(
                [
                    f"Name : {student['name']}",
                    f"Roll Number : {student['roll_number']}",
                    f"Exam : {exam.get('exam_name')}",
                    f"Percentage : {exam.get('percentage')}%",
                    f"Grade : {exam.get('grade')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "daily_communication":
        lines = ["Daily Communication", ""]

        if tool_result.get("student"):
            student = tool_result["student"]
            lines.extend(
                [f"Student : {student['name']}", f"Class : {student['class_name']}", ""]
            )

        for communication in tool_result["data"]:
            lines.extend(
                [
                    f"Notice : {communication.get('last_notice')}",
                    f"Homework : {communication.get('last_homework')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    data = tool_result["data"]

    student = data["basic_details"]
    attendance = data["attendance"]
    fees = data["fees"]
    exams = data["exams"]
    communication = data["communication"]

    return f"""
Student Portfolio

Basic Details
Student ID : {student['student_id']}
Name : {student['name']}
Class : {student['class_name']}
Roll Number : {student['roll_number']}
Admission No : {student['admission_number']}
Date of Birth : {student['dob']}
Gender : {student['gender']}
Parent : {student['parent_name']}
Contact : {student['contact_number']}
Address : {student['address']}
Admission Date : {student['admission_date']}

Attendance
Present Days : {attendance['present_days']}
Absent Days : {attendance['absent_days']}
Attendance Percentage : {attendance['attendance_percentage']}%

Fees
Total Fees : ₹{fees['total_fees']}
Paid Fees : ₹{fees['paid_fees']}
Outstanding Fees : ₹{fees['outstanding_fees']}

Exam Report
Exam Name : {exams['exam_name']}
Percentage : {exams['percentage']}%
Grade : {exams['grade']}

Communication
Last Notice : {communication['last_notice']}
Last Homework : {communication['last_homework']}
""".strip()
