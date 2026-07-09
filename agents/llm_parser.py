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

10. If the user asks about:
- homework
- homework details
- notice
- notices
- circular
- announcement
- announcements
- communication
- diary
- parent message
- teacher message
- school message
- latest notice
- latest homework

→ daily_communication

If you are not confident, return:

{
  "intent": "unknown",
  "parameters": {
    "student_name": null,
    "class_name": null,
    "date_range": null,
    "exam_name": null
  }
}

Always return JSON in this exact format:

{
  "intent": "...",
  "parameters": {
    "student_name": "...",
    "class_name": "...",
    "date_range": "...",
    "exam_name": "..."
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
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "intent": "unknown",
            "parameters": {
                "student_name": None,
                "class_name": None,
                "date_range": None,
                "exam_name": None,
            },
        }
