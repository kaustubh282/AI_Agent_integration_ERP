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
        return datetime.fromisoformat(str(value).replace("Z", "")).strftime("%d-%m-%Y")
    except Exception:
        return value


def is_show_all(tool_result: dict, nested_data: dict | None = None) -> bool:
    raw_value = tool_result.get("show_all", False)

    if raw_value is not True and isinstance(nested_data, dict):
        raw_value = nested_data.get("show_all", False)

    return raw_value is True


def limited_records(records: list, show_all: bool, limit: int = 10) -> list:
    return records if show_all else records[:limit]


def add_limit_message(
    lines: list, show_all: bool, total_count: int, label: str, show_all_text: str
):
    if not show_all and total_count > 10:
        lines.append("")
        lines.append(f"Showing latest 10 of {total_count} {label}.")
        lines.append(show_all_text)


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
        records = tool_result.get("data", [])
        show_all = is_show_all(tool_result)
        display_records = limited_records(records, show_all)

        lines = ["Fees Outstanding Report", ""]

        for record in display_records:
            student = record.get("student", {})
            fees = record.get("fees", {})

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

        add_limit_message(
            lines,
            show_all,
            len(records),
            "students",
            "Ask 'show all fees outstanding records' if you want the full list.",
        )

        return "\n".join(lines).strip()

    if response_type == "fees_collection":
        data = tool_result["data"]
        records = data.get("records", [])

        records = sorted(
            records,
            key=lambda record: record.get("date") or "",
            reverse=True,
        )

        show_all = is_show_all(tool_result, data)
        display_records = limited_records(records, show_all)

        date_labels = {
            "today": "Today",
            "yesterday": "Yesterday",
            "this_week": "This Week",
            "last_week": "Last Week",
            "this_month": "This Month",
            "last_month": "Last Month",
            "all": "All Time",
            None: "All Time",
        }

        raw_date_range = data.get("date_range")
        date_label = date_labels.get(
            raw_date_range, str(raw_date_range).replace("_", " ").title()
        )

        lines = [
            "Fees Collection Report",
            "",
            f"Date Range : {date_label}",
            f"Class : {data.get('class_name') or 'All'}",
            f"Total Collected : ₹{data.get('total_collected', 0)}",
            f"Payment Count : {data.get('payment_count', 0)}",
            "",
            "Payments",
        ]

        for record in display_records:
            lines.append(
                f"- {record.get('student_name', 'Unknown')} | "
                f"Class {record.get('class_name')} | "
                f"₹{record.get('amount')} | "
                f"{format_date(record.get('date'))} | "
                f"{record.get('payment_mode') or record.get('mode')}"
            )

        add_limit_message(
            lines,
            show_all,
            len(records),
            "payments",
            "Ask 'show all fees collection records' if you want the full list.",
        )

        return "\n".join(lines).strip()

    if response_type == "expenses":
        expenses = tool_result.get("data", [])

        expenses = sorted(
            expenses,
            key=lambda expense: expense.get("date") or "",
            reverse=True,
        )

        show_all = is_show_all(tool_result)
        display_expenses = limited_records(expenses, show_all)

        lines = ["Expenses Report", ""]

        for expense in display_expenses:
            lines.extend(
                [
                    f"Date : {format_date(expense.get('date'))}",
                    f"Category : {expense.get('category')}",
                    f"Description : {expense.get('description')}",
                    f"Amount : ₹{expense.get('amount')}",
                    "",
                ]
            )

        add_limit_message(
            lines,
            show_all,
            len(expenses),
            "expenses",
            "Ask 'show all expenses' if you want the full list.",
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

        show_all = is_show_all(tool_result)
        display_enquiries = limited_records(enquiries, show_all)

        lines = [
            "Enquiry Report",
            "",
            f"Total Enquiries : {len(enquiries)}",
            "",
            "Enquiries",
        ]

        for enquiry in display_enquiries:
            lines.append(
                f"- {enquiry.get('student_name', 'Unknown')} | "
                f"Class {enquiry.get('class_name', 'N/A')} | "
                f"{enquiry.get('status', 'N/A')} | "
                f"{format_date(enquiry.get('enquiry_date') or enquiry.get('date'))}"
            )

        add_limit_message(
            lines,
            show_all,
            len(enquiries),
            "enquiries",
            "Ask 'show all enquiries' if you want the full list.",
        )

        return "\n".join(lines).strip()

    if response_type == "new_admission":
        admissions = tool_result.get("data", [])

        admissions = sorted(
            admissions,
            key=lambda admission: admission.get("admission_date") or "",
            reverse=True,
        )

        show_all = is_show_all(tool_result)
        display_admissions = limited_records(admissions, show_all)

        filters = tool_result.get("filters", {})

        date_labels = {
            "today": "Today",
            "yesterday": "Yesterday",
            "this_week": "This Week",
            "last_week": "Last Week",
            "this_month": "This Month",
            "last_month": "Last Month",
            "all": "All Time",
            None: "All Time",
        }

        raw_date_range = filters.get("date_range")
        date_label = date_labels.get(
            raw_date_range,
            str(raw_date_range).replace("_", " ").title(),
        )

        lines = [
            "New Admissions Report",
            "",
            f"Date Range : {date_label}",
            f"Class : {filters.get('class_name', 'All')}",
            f"Total Admissions : {len(admissions)}",
            "",
            "Admissions",
        ]

        for admission in display_admissions:
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

        add_limit_message(
            lines,
            show_all,
            len(admissions),
            "admissions",
            "Ask 'show all new admissions' if you want the full list.",
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
        records = tool_result.get("data", [])
        show_all = is_show_all(tool_result)
        display_records = limited_records(records, show_all)

        lines = ["Class Exam Report", ""]

        for record in display_records:
            student = record.get("student", {})
            exam = record.get("exam", {})

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

        add_limit_message(
            lines,
            show_all,
            len(records),
            "students",
            "Ask 'show all class exam records' if you want the full list.",
        )

        return "\n".join(lines).strip()

    if response_type == "daily_communication":
        communications = tool_result.get("data", [])
        show_all = is_show_all(tool_result)
        display_communications = limited_records(communications, show_all)

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

        for communication in display_communications:
            lines.extend(
                [
                    f"Notice : {communication.get('last_notice', 'N/A')}",
                    f"Homework : {communication.get('last_homework', 'N/A')}",
                    "",
                ]
            )

        add_limit_message(
            lines,
            show_all,
            len(communications),
            "communications",
            "Ask 'show all daily communications' if you want the full list.",
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
