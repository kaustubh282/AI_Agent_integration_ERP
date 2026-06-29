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
        summary = tool_result["data"]
        date_range = summary["date_range"].replace("_", " ")
        class_label = summary["class_name"] or "All Classes"

        lines = [
            "Fees Collection Report",
            "",
            f"Date Range : {date_range}",
            f"Class : {class_label}",
            f"Total Collected : ₹{summary['total_collected']}",
            f"Payment Count : {summary['payment_count']}",
            "",
        ]

        for record in summary["records"]:
            lines.extend(
                [
                    f"Date : {record['date']}",
                    f"Student : {record['student_name']}",
                    f"Class : {record['class_name']}",
                    f"Amount : ₹{record['amount']}",
                    f"Payment Mode : {record['payment_mode']}",
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
