import json
from datetime import date, datetime, timedelta
from pathlib import Path

from core.exceptions import ERPAPIError

MOCK_DATA_DIR = Path("mock_data")


class ERPAPIClient:

    def load_json(self, file_name):
        if Path(file_name).name != file_name:
            raise ERPAPIError("Invalid data source.")

        file_path = (MOCK_DATA_DIR / file_name).resolve()
        mock_data_root = MOCK_DATA_DIR.resolve()

        if not str(file_path).startswith(str(mock_data_root)):
            raise ERPAPIError("Invalid data source.")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise ERPAPIError("ERP data is temporarily unavailable.") from exc
        except json.JSONDecodeError as exc:
            raise ERPAPIError("ERP data is temporarily unavailable.") from exc

        if not isinstance(data, list):
            raise ERPAPIError("ERP data is temporarily unavailable.")

        return data

    def get_students(self):
        return self.load_json("students.json")

    def get_attendance(self):
        return self.load_json("attendance.json")

    def get_fees(self):
        return self.load_json("fees.json")

    def get_exams(self):
        return self.load_json("exams.json")

    def get_communication(self):
        return self.load_json("communication.json")

    def get_fees_collection_records(self):
        return self.load_json("fees_collection.json")

    def find_student(self, student_name, class_name):
        if not student_name or not class_name:
            return None

        students = self.get_students()

        for student in students:
            if (
                student["name"].lower() == student_name.lower()
                and student["class_name"].lower() == class_name.lower()
            ):
                return student

        return None

    def find_by_student_id(self, data, student_id):
        for item in data:
            if item["student_id"] == student_id:
                return item

        return None

    def get_students_with_outstanding_fees(self, class_name=None):
        students = self.get_students()
        fees_data = self.get_fees()
        records = []

        for student in students:
            if class_name and student["class_name"].lower() != class_name.lower():
                continue

            fees = self.find_by_student_id(fees_data, student["student_id"])

            if fees and fees["outstanding_fees"] > 0:
                records.append({"student": student, "fees": fees})

        return records

    def get_fees_collection_summary(self, date_range=None, class_name=None):
        records = self.get_fees_collection_records()
        students = {student["student_id"]: student for student in self.get_students()}
        filtered_records = []

        for record in records:
            if (
                class_name
                and record.get("class_name", "").lower() != class_name.lower()
            ):
                continue

            if date_range and not self._matches_date_range(record["date"], date_range):
                continue

            student = students.get(record["student_id"], {})
            filtered_records.append(
                {
                    **record,
                    "student_name": student.get("name", "Unknown"),
                }
            )

        total_collected = sum(record["amount"] for record in filtered_records)

        return {
            "date_range": date_range or "all",
            "class_name": class_name,
            "total_collected": total_collected,
            "payment_count": len(filtered_records),
            "records": filtered_records,
        }

    def _matches_date_range(self, record_date, date_range):
        parsed_date = datetime.strptime(record_date, "%Y-%m-%d").date()
        today = date.today()

        if date_range == "today":
            return parsed_date == today

        if date_range == "yesterday":
            return parsed_date == today - timedelta(days=1)

        if date_range == "last_week":
            start_date = today - timedelta(days=7)
            return start_date <= parsed_date <= today

        if date_range == "this_month":
            return parsed_date.year == today.year and parsed_date.month == today.month

        if date_range == "last_month":
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            return first_day_last_month <= parsed_date <= last_day_last_month

        return True

    def get_enquiries(self):
        return self.load_json("mock_data/enquiries.json")

    def get_expenses(self):
        return self.load_json("mock_data/expenses.json")

    def get_admissions(self):
        return self.load_json("mock_data/admissions.json")

    def get_students_by_class(self, class_name):
        students = self.get_students()
        return [
            student
            for student in students
            if student["class_name"].lower() == class_name.lower()
        ]

    def get_fee_collections(self, date_range=None, class_name=None):
        students = self.get_students()
        fees_data = self.get_fees()
        records = []

        for student in students:
            if class_name and student["class_name"].lower() != class_name.lower():
                continue

            fees = self.find_by_student_id(fees_data, student["student_id"])
            if fees and fees["paid_fees"] > 0:
                records.append({"student": student, "fees": fees})

        return records

    def get_students_with_outstanding_fees(self, class_name=None):
        students = self.get_students()
        fees_data = self.get_fees()
        records = []

        for student in students:
            if class_name and student["class_name"].lower() != class_name.lower():
                continue

            fees = self.find_by_student_id(fees_data, student["student_id"])
            if fees and fees["outstanding_fees"] > 0:
                records.append({"student": student, "fees": fees})

            return records
