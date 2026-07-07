import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def parse_user_message(message: str) -> dict:
    system_prompt = """
You are an ERP AI Agent parser.

Your job is only to extract intent and parameters.
Do not answer the user.
Do not generate ERP data.
Return only valid JSON.

Allowed intents:
student_portfolio
attendance_details
fees_outstanding
fees_collection
expenses
student_exam_report
class_exam_report
enquiry_report
new_admission
daily_communication
unknown

Return format:
{
  "intent": "...",
  "parameters": {
    "student_name": null,
    "class_name": null,
    "date_range": null,
    "exam_name": null
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