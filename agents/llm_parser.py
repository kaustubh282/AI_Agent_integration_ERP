import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_user_message(message: str) -> dict:
    system_prompt = """
You are an ERP AI Agent Intent Parser.

Your ONLY responsibility is to understand the user's request and return structured JSON.

Do NOT answer the user's question.
Do NOT generate ERP data.
Do NOT explain anything.
Return ONLY valid JSON.

Available intents:

- student_portfolio
- attendance_details
- fees_outstanding
- fees_collection
- expenses
- student_exam_report
- class_exam_report
- enquiry_report
- new_admission
- daily_communication
- unknown

Intent Rules:

1. If the user asks for complete profile, profile, portfolio, complete details, all details, student details, student information, complete information, student card or complete record
→ student_portfolio

2. If the user asks for attendance, present, absent or attendance percentage
→ attendance_details

3. If the user asks for pending fees, outstanding fees, due fees, unpaid fees
→ fees_outstanding

4. If the user asks for fees collected, collection report, collected amount, payment report
→ fees_collection

5. If the user asks for expenses, expenditure, spending or expense report
→ expenses

6. If the user asks for student exam report, marks, percentage, grade or result of one student
→ student_exam_report

7. If the user asks for class exam report, class result, overall class marks or class performance
→ class_exam_report

8. If the user asks for enquiries, enquiry report, admission enquiry or parent enquiry
→ enquiry_report

9. If the user asks for admissions, newly admitted students or admission report
→ new_admission

10. If the user asks about homework, notices, circulars, announcements, communication, diary, parent message, teacher message, school message, latest notice, or latest homework
→ daily_communication

Parameter Rules:

- student_name: Extract student name if user mentions one.
- class_name: Extract class if user mentions one.
- - date_range:
  Use one of:
  today,
  yesterday,
  last_week,
  this_week,
  last_month,
  this_month,
  january,
  february,
  march,
  april,
  may,
  june,
  july,
  august,
  september,
  october,
  november,
  december.
  Otherwise null.
- exam_name: Extract exam name if mentioned.
- show_all: true if the user asks for all records, full report, complete report, full list, complete list, show all, all payments, all enquiries, all collection records, total records, or everything.

Always return JSON in this format:

{
  "intent": "...",
  "parameters": {
    "student_name": "...",
    "class_name": "...",
    "date_range": "...",
    "exam_name": "...",
    "show_all": true
  }
}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)

        if "parameters" not in parsed:
            parsed["parameters"] = {}

        parsed["parameters"].setdefault("student_name", None)
        parsed["parameters"].setdefault("class_name", None)
        parsed["parameters"].setdefault("date_range", None)
        parsed["parameters"].setdefault("exam_name", None)
        parsed["parameters"].setdefault("show_all", False)

        # -------------------------------
        # Deterministic show_all override
        # -------------------------------
        lower_message = message.lower().strip()

        show_all_phrases = [
            "show all enquiry",
            "show all enquiries",
            "all enquiry",
            "all enquiries",
            "complete enquiry report",
            "full enquiry report",
            "show all",
            "show me all",
            "give all",
            "give me all",
            "get all",
            "view all",
            "all records",
            "all record",
            "full report",
            "complete report",
            "full list",
            "complete list",
            "all payments",
            "all enquiries",
            "all collection records",
            "show complete",
            "everything",
            "entire report",
        ]

        normal_limited_phrases = [
            "show fees collection",
            "fees collection",
            "show collection report",
            "collection report",
            "show fees collected",
            "fees collected",
            "show payment report",
            "payment report",
        ]

        if lower_message in normal_limited_phrases:
            parsed["parameters"]["show_all"] = False
        elif any(phrase in lower_message for phrase in show_all_phrases):
            parsed["parameters"]["show_all"] = True
        else:
            parsed["parameters"]["show_all"] = False

        return parsed

    except Exception:
        return {
            "intent": "unknown",
            "parameters": {
                "student_name": None,
                "class_name": None,
                "date_range": None,
                "exam_name": None,
                "show_all": False,
            },
        }
