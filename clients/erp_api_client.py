import json
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

from config.settings import settings
from core.exceptions import ERPAPIError

MOCK_DATA_DIR = Path("mock_data")


class ERPAPIClient:
    def load_json(self, file_name: str):
        if Path(file_name).name != file_name:
            raise ERPAPIError("Invalid data source.")

        file_path = (MOCK_DATA_DIR / file_name).resolve()
        mock_data_root = MOCK_DATA_DIR.resolve()

        if not str(file_path).startswith(str(mock_data_root)):
            raise ERPAPIError("Invalid data source.")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            raise ERPAPIError("ERP data is temporarily unavailable.") from exc

        if not isinstance(data, list):
            raise ERPAPIError("ERP data is temporarily unavailable.")

        return data

    def call_api(self, endpoint: str, params: dict | None = None):
        if not settings.ERP_API_BASE_URL:
            raise ERPAPIError("ERP API base URL is not configured.")

        url = f"{settings.ERP_API_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

        headers = {"Content-Type": "application/json"}

        if settings.ERP_API_KEY:
            headers["Authorization"] = f"Bearer {settings.ERP_API_KEY}"

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            raise ERPAPIError("Unable to connect to ERP API.") from exc
        except ValueError as exc:
            raise ERPAPIError("Invalid response received from ERP API.") from exc

        if not isinstance(data, list):
            raise ERPAPIError("ERP API returned invalid data format.")

        return data

    def get_students(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/students")
        return self.load_json("students.json")

    def get_attendance(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/attendance")
        return self.load_json("attendance.json")

    def get_fees(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/fees")
        return self.load_json("fees.json")

    def get_exams(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/exams")
        return self.load_json("exams.json")

    def get_communication(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/communication")
        return self.load_json("communication.json")

    def get_fees_collection_records(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/fees-collection")
        return self.load_json("fees_collection.json")

    def get_enquiries(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/enquiries")
        return self.load_json("enquiries.json")

    def get_expenses(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/expenses")
        return self.load_json("expenses.json")

    def get_admissions(self):
        if settings.ERP_DATA_MODE == "api":
            return self.call_api("/admissions")
        return self.load_json("admissions.json")

    def find_student(self, student_name, class_name):
        if not student_name or not class_name:
            return None

        for student in self.get_students():
            if (
                student.get("name", "").lower() == student_name.lower()
                and student.get("class_name", "").lower() == class_name.lower()
            ):
                return student

        return None

    def find_by_student_id(self, data, student_id):
        for item in data:
            if item.get("student_id") == student_id:
                return item
        return None

    def get_students_by_class(self, class_name):
        if not class_name:
            return []

        return [
            student
            for student in self.get_students()
            if student.get("class_name", "").lower() == class_name.lower()
        ]

    def get_students_with_outstanding_fees(self, class_name=None):
        records = []
        fees_data = self.get_fees()

        for student in self.get_students():
            if class_name and student.get("class_name", "").lower() != class_name.lower():
                continue

            fees = self.find_by_student_id(fees_data, student.get("student_id"))

            if fees and fees.get("outstanding_fees", 0) > 0:
                records.append({"student": student, "fees": fees})

        return records

    def get_fees_collection_summary(self, date_range=None, class_name=None):
        records = self.get_fees_collection_records()
        students = {student["student_id"]: student for student in self.get_students()}
        filtered_records = []

        for record in records:
            if class_name and record.get("class_name", "").lower() != class_name.lower():
                continue

            if date_range and not self._matches_date_range(record.get("date"), date_range):
                continue

            student = students.get(record.get("student_id"), {})

            filtered_records.append(
                {
                    **record,
                    "student_name": student.get("name", "Unknown"),
                }
            )

        return {
            "date_range": date_range or "all",
            "class_name": class_name,
            "total_collected": sum(record.get("amount", 0) for record in filtered_records),
            "payment_count": len(filtered_records),
            "records": filtered_records,
        }

    def get_fee_collections(self, date_range=None, class_name=None):
        return self.get_fees_collection_summary(date_range, class_name)

    def _matches_date_range(self, record_date, date_range):
        if not record_date:
            return False

        parsed_date = datetime.strptime(record_date, "%Y-%m-%d").date()
        today = date.today()

        if date_range == "today":
            return parsed_date == today

        if date_range == "yesterday":
            return parsed_date == today - timedelta(days=1)

        if date_range == "last_week":
            return today - timedelta(days=7) <= parsed_date <= today

        if date_range == "this_month":
            return parsed_date.year == today.year and parsed_date.month == today.month

        if date_range == "last_month":
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            return first_day_last_month <= parsed_date <= last_day_last_month

        return True