from datetime import datetime


def format_date(value):
    if not value:
        return "N/A"

    if value in (
        "0001-01-01T00:00:00",
        "0001-01-01",
        "1900-01-01T00:00:00",
    ):
        return "N/A"

    try:
        return datetime.fromisoformat(value.replace("Z", "")).strftime("%d-%m-%Y")
    except Exception:
        return value


def format_response(tool_result: dict) -> str:
    if tool_result["status"] != "success":
        return tool_result.get("message", "No data found.")

    response_type = tool_result.get("type")

    if response_type == "attendance_details":
        student = tool_result["student"]
        attendance = tool_result["data"]

        return f"""
Attendance Details

Name : {student.get('name')}
Class : {student.get('class_name')}
Roll Number : {student.get('roll_number', 'N/A')}

Present Days : {attendance.get('present_days', 'N/A')}
Absent Days : {attendance.get('absent_days', 'N/A')}
Attendance Percentage : {attendance.get('attendance_percentage', 'N/A')}%
""".strip()

    if response_type == "fees_outstanding":
        lines = ["Fees Outstanding Report", ""]

        for record in tool_result["data"]:
            student = record["student"]
            fees = record["fees"]

            lines.extend(
                [
                    f"Name : {student.get('name')}",
                    f"Class : {student.get('class_name')}",
                    f"Roll Number : {student.get('roll_number', 'N/A')}",
                    f"Total Fees : ₹{fees.get('total_fees', 0)}",
                    f"Paid Fees : ₹{fees.get('paid_fees', 0)}",
                    f"Outstanding Fees : ₹{fees.get('outstanding_fees', 0)}",
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

        records = data.get("records", [])

        records = sorted(
            records,
            key=lambda record: record.get("date") or "",
            reverse=True,
        )

        for record in records[:10]:
            lines.append(
                f"- {record.get('student_name', 'Unknown')} | Class {record.get('class_name')} | ₹{record.get('amount')} | {format_date(record.get('date'))} | {record.get('payment_mode') or record.get('mode')}"
            )

        if len(records) > 10:
            lines.append("")
            lines.append(f"Showing latest 10 of {len(records)} payments.")
            lines.append(
                "Ask 'show all fees collection records' if you want the full list."
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
        enquiries = tool_result.get("data", [])

        enquiries = sorted(
            enquiries,
            key=lambda enquiry: enquiry.get("enquiry_date")
            or enquiry.get("date")
            or "",
            reverse=True,
        )

        lines = [
            "Enquiry Report",
            "",
            f"Total Enquiries : {len(enquiries)}",
            "",
            "Latest Enquiries",
        ]

        for enquiry in enquiries[:10]:
            lines.extend(
                [
                    f"- {enquiry.get('student_name', 'Unknown')} | Class {enquiry.get('class_name', 'N/A')} | {enquiry.get('status', 'N/A')} | {format_date(enquiry.get('enquiry_date') or enquiry.get('date'))}",
                ]
            )

        if len(enquiries) > 10:
            lines.append("")
            lines.append(f"Showing latest 10 of {len(enquiries)} enquiries.")
            lines.append("Ask 'show all enquiries' if you want the full list.")

        return "\n".join(lines).strip()

    if response_type == "new_admission":
        lines = ["New Admissions Report", ""]

        for admission in tool_result["data"]:
            lines.extend(
                [
                    f"Student Name : {admission.get('student_name') or admission.get('name')}",
                    f"Class : {admission.get('class_name')}",
                    f"Admission Date : {format_date(admission.get('admission_date'))}",
                    f"Parent : {admission.get('parent_name') or admission.get('father_name')}",
                    f"Contact : {admission.get('contact_number') or admission.get('father_contact')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "student_exam_report":
        student = tool_result["student"]
        exam = tool_result["data"]

        return f"""
Student Exam Report

Name : {student.get('name')}
Class : {student.get('class_name')}
Roll Number : {student.get('roll_number', 'N/A')}

Exam : {exam.get('exam_name', 'N/A')}
Percentage : {exam.get('percentage', 'N/A')}%
Grade : {exam.get('grade', 'N/A')}
""".strip()

    if response_type == "class_exam_report":
        lines = ["Class Exam Report", ""]

        for record in tool_result["data"]:
            student = record["student"]
            exam = record["exam"]

            lines.extend(
                [
                    f"Name : {student.get('name')}",
                    f"Roll Number : {student.get('roll_number', 'N/A')}",
                    f"Exam : {exam.get('exam_name', 'N/A')}",
                    f"Percentage : {exam.get('percentage', 'N/A')}%",
                    f"Grade : {exam.get('grade', 'N/A')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    if response_type == "daily_communication":
        lines = ["Daily Communication", ""]

        if tool_result.get("student"):
            student = tool_result["student"]
            lines.extend(
                [
                    f"Student : {student.get('name')}",
                    f"Class : {student.get('class_name')}",
                    "",
                ]
            )

        for communication in tool_result["data"]:
            lines.extend(
                [
                    f"Notice : {communication.get('last_notice', 'N/A')}",
                    f"Homework : {communication.get('last_homework', 'N/A')}",
                    "",
                ]
            )

        return "\n".join(lines).strip()

    data = tool_result["data"]

    student = data.get("basic_details") or {}
    attendance = data.get("attendance") or {}
    fees = data.get("fees") or {}
    exams = data.get("exams") or {}
    communication = data.get("communication") or {}

    return f"""
Student Portfolio

Basic Details
Student ID : {student.get('student_id')}
Name : {student.get('name')}
Class : {student.get('class_name')}
Section : {student.get('section', 'N/A')}
Roll Number : {student.get('roll_number') or 'N/A'}
Admission No : {student.get('admission_number', 'N/A')}
Date of Birth : {format_date(student.get('dob'))}
Gender : {student.get('gender') or 'N/A'}
Parent : {student.get('parent_name') or student.get('father_name') or student.get('mother_name') or 'N/A'}
Father : {student.get('father_name', 'N/A')}
Mother : {student.get('mother_name', 'N/A')}
Contact : {student.get('contact_number') or student.get('father_contact') or student.get('mother_contact') or student.get('phone') or 'N/A'}
Address : {student.get('address') or 'N/A'}
Admission Date : {format_date(student.get('admission_date'))}

Attendance
Present Days : {attendance.get('present_days', 'N/A')}
Absent Days : {attendance.get('absent_days', 'N/A')}
Attendance Percentage : {attendance.get('attendance_percentage', 'N/A')}%

Fees
Total Fees : ₹{fees.get('total_fees', 0)}
Paid Fees : ₹{fees.get('paid_fees', 0)}
Outstanding Fees : ₹{fees.get('outstanding_fees', 0)}

Exam Report
Exam Name : {exams.get('exam_name', 'N/A')}
Percentage : {exams.get('percentage', 'N/A')}%
Grade : {exams.get('grade', 'N/A')}

Communication
Last Notice : {communication.get('last_notice', 'N/A')}
Last Homework : {communication.get('last_homework', 'N/A')}
""".strip()
