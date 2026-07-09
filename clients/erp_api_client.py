import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import requests

from config.settings import settings
from core.exceptions import ERPAPIError

MOCK_DATA_DIR = Path("mock_data")


class ERPAPIClient:
    def __init__(self):
        self.base_url = settings.ERP_API_BASE_URL.rstrip("/")
        self.token = None
        self.tenant_id = settings.ERP_TENANT_ID
        self.academic_year_id = settings.ERP_ACADEMIC_YEAR_ID
        self.tenant_board_id = settings.ERP_TENANT_BOARD_ID
        self.user_id = settings.ERP_USER_ID

    def load_json(self, file_name: str):
        file_path = MOCK_DATA_DIR / file_name
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as exc:
            raise ERPAPIError("ERP mock data unavailable.") from exc

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _headers(self):
        headers = {
            "Content-Type": "application/json",
            "TenantCode": settings.ERP_TENANT_CODE,
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def authenticate(self):
        if self.token:
            return self.token

        if not settings.ERP_USERNAME or not settings.ERP_PASSWORD:
            raise ERPAPIError("ERP username/password not configured.")

        payload = {
            "tenantId": settings.ERP_TENANT_ID,
            "userName": settings.ERP_USERNAME,
            "password": settings.ERP_PASSWORD,
            "academicYearId": settings.ERP_ACADEMIC_YEAR_ID,
            "tenantBoardId": settings.ERP_TENANT_BOARD_ID,
        }

        response = requests.post(
            self._url("AuthenticateUser"),
            headers={
                "Content-Type": "application/json",
                "TenantCode": settings.ERP_TENANT_CODE,
            },
            json=payload,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        user = data[0] if isinstance(data, list) and data else data

        if not user or not user.get("jwtToken"):
            raise ERPAPIError("ERP login failed. JWT token not received.")

        self.token = user["jwtToken"]
        self.tenant_id = user.get("tenantId", self.tenant_id)
        self.academic_year_id = user.get("academicYearId", self.academic_year_id)
        self.tenant_board_id = user.get("tenantBoardId", self.tenant_board_id)
        self.user_id = user.get("userID", self.user_id)

        return self.token

    def request(self, method: str, endpoint: str, payload: dict | None = None):
        self.authenticate()

        response = requests.request(
            method=method,
            url=self._url(endpoint),
            headers=self._headers(),
            json=payload,
            timeout=20,
        )

        response.raise_for_status()

        if not response.text:
            return None

        return response.json()

    def get_api(self, endpoint: str):
        return self.request("GET", endpoint)

    def post_api(self, endpoint: str, payload: dict | None = None):
        return self.request("POST", endpoint, payload)

    # -----------------------------
    # Real ERP API methods found
    # -----------------------------

    def get_students_by_board_year(self):
        return self.get_api(
            f"GetStudentListByBoardYear/{self.tenant_board_id}/{self.academic_year_id}"
        )

    def get_students_by_grade(self, tenant_class_id: int):
        return self.get_api(
            f"GetStudentListByGrade/{tenant_class_id}/{self.tenant_board_id}/{self.academic_year_id}"
        )

    def get_student_fees_detail(self, student_id: int):
        return self.get_api(
            f"GetStudentFeesDetail/{self.academic_year_id}/{student_id}"
        )

    def get_mis_fees_report(self, from_date: str, to_date: str, unique_id: int = 0):
        return self.get_api(
            f"GetMISFeesReport/{self.tenant_id}/{from_date}/{to_date}/{unique_id}/{self.user_id}"
        )

    def get_enquiries_by_dates(self, from_date: str, to_date: str):
        return self.get_api(f"GetEnquiryByDates/{from_date}/{to_date}/{self.tenant_id}")

    def get_enquiry_followups_by_dates(self, from_date: str, to_date: str):
        return self.get_api(
            f"GetEnquiryFollowupByDates/{from_date}/{to_date}/{self.tenant_id}"
        )

    def get_class_exam_details(self, tenant_class_id: int):
        return self.get_api(
            f"GetClassExamDetails/{self.tenant_id}/{self.tenant_board_id}/{self.academic_year_id}/{tenant_class_id}"
        )

    def get_student_marks_classwise(self, payload: dict):
        return self.post_api("GetStudentMarksClasswise", payload)

    def get_student_grade_classwise(self, payload: dict):
        return self.post_api("GetStudentGradeClasswise", payload)

    def get_cbse_student_attendance(self, payload: dict):
        return self.post_api("GetCBSEStudentAttendance", payload)

    def get_student_attendance_by_class(self, payload: dict):
        return self.post_api("GetStudentAttendanceByClass", payload)

    # -----------------------------
    # Existing tool-facing methods
    # -----------------------------

    def get_students(self):
        if settings.ERP_DATA_MODE == "api":
            all_students = []

            for class_id in range(1, 13):
                students = self.get_students_by_grade(class_id)

                if isinstance(students, list):
                    all_students.extend(students)

            return [
                self.normalize_student(student)
                for student in all_students
                if (student.get("nameDisplayLabel") or "").strip()
            ]

        return self.load_json("students.json")

    def get_attendance(self):
        if settings.ERP_DATA_MODE == "api":
            return []
        return self.load_json("attendance.json")

    def get_fees(self):
        if settings.ERP_DATA_MODE == "api":
            return []
        return self.load_json("fees.json")

    def get_exams(self):
        if settings.ERP_DATA_MODE == "api":
            return []
        return self.load_json("exams.json")

    def get_communication(self):
        if settings.ERP_DATA_MODE == "api":
            return []
        return self.load_json("communication.json")

    def get_fees_collection_records(self):
        if settings.ERP_DATA_MODE == "api":
            from_date, to_date = "2024-01-01", date.today().isoformat()
            records = self.get_mis_fees_report(from_date, to_date)

            return [self.normalize_fees_collection(record) for record in records]

        return self.load_json("fees_collection.json")

    def get_enquiries(self):
        if settings.ERP_DATA_MODE == "api":
            from_date, to_date = "2024-01-01", date.today().isoformat()
            enquiries = self.get_enquiries_by_dates(from_date, to_date)

            return [self.normalize_enquiry(enquiry) for enquiry in enquiries]

        return self.load_json("enquiries.json")

    def get_expenses(self):
        if settings.ERP_DATA_MODE == "api":
            return []
        return self.load_json("expenses.json")

    def get_admissions(self):
        if settings.ERP_DATA_MODE == "api":
            students = self.get_students()

            return [
                {
                    "student_name": student.get("name"),
                    "class_name": student.get("display_label")
                    or student.get("class_name"),
                    "admission_date": student.get("admission_date"),
                    "parent_name": student.get("father_name")
                    or student.get("mother_name"),
                    "contact_number": student.get("father_contact")
                    or student.get("mother_contact")
                    or student.get("phone"),
                    "raw": student,
                }
                for student in students
            ]

        return self.load_json("admissions.json")

    def find_student(self, student_name, class_name=None):
        if not student_name:
            return None

        student_name = student_name.lower().strip()
        class_name = class_name.lower().strip() if class_name else None

        for student in self.get_students():
            current_name = student.get("name", "").lower().strip()
            current_class = student.get("class_name", "").lower().strip()
            current_display_label = student.get("display_label", "").lower().strip()

            name_matches = current_name == student_name

            class_matches = (
                not class_name
                or current_class == class_name
                or current_display_label == class_name
            )

            if name_matches and class_matches:
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
            if (
                class_name
                and student.get("class_name", "").lower() != class_name.lower()
            ):
                continue

            fees = self.find_by_student_id(fees_data, student.get("student_id"))

            if fees and fees.get("outstanding_fees", 0) > 0:
                records.append({"student": student, "fees": fees})

        return records

    def get_fees_collection_summary(self, date_range=None, class_name=None):
        records = self.get_fees_collection_records()

        if class_name:
            records = [
                record
                for record in records
                if record.get("class_name", "").lower() == class_name.lower()
            ]

        return {
            "date_range": date_range or "all",
            "class_name": class_name or "All",
            "total_collected": sum(record.get("amount", 0) for record in records),
            "payment_count": len(records),
            "records": records,
        }

    def get_fee_collections(self, date_range=None, class_name=None):
        return self.get_fees_collection_summary(date_range, class_name)

    def _date_range_to_api_dates(self, date_range):
        today = date.today()

        if date_range == "yesterday":
            day = today - timedelta(days=1)
            return day.isoformat(), day.isoformat()

        if date_range == "last_week":
            return (today - timedelta(days=7)).isoformat(), today.isoformat()

        if date_range == "this_month":
            return today.replace(day=1).isoformat(), today.isoformat()

        if date_range == "last_month":
            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)
            first_day_last_month = last_day_last_month.replace(day=1)
            return first_day_last_month.isoformat(), last_day_last_month.isoformat()

        return today.isoformat(), today.isoformat()

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

    def normalize_student(self, student: dict):
        return {
            "student_id": student.get("studentId") or student.get("id"),
            "name": (student.get("nameDisplayLabel") or "").strip(),
            "admission_number": student.get("prn")
            or student.get("saralID")
            or student.get("studentId"),
            "first_name": student.get("firstName"),
            "middle_name": student.get("middleName"),
            "last_name": student.get("lastName"),
            "roll_number": student.get("rollNo"),
            "class_name": student.get("tenantClassName"),
            "section": student.get("sectionName"),
            "display_label": student.get("displayLabel"),
            "tenant_class_id": student.get("tenantClassId"),
            "section_id": student.get("sectionId"),
            "current_class_section_id": student.get("currentClassSectionId"),
            "academic_year_id": student.get("academicYearId"),
            "academic_year_name": student.get("academicYearName"),
            "board_name": student.get("boardName"),
            "gender": student.get("gender"),
            "dob": student.get("dob"),
            "father_name": student.get("fatherName"),
            "father_contact": student.get("fatherContact1"),
            "father_email": student.get("fatherMailId"),
            "mother_name": student.get("motherName"),
            "mother_contact": student.get("motherContact1"),
            "mother_email": student.get("motherMailId"),
            "address": student.get("localAddress"),
            "phone": student.get("phoneNo") or student.get("primaryContactNo"),
            "raw": student,
        }

    def normalize_enquiry(self, enquiry: dict):
        full_name = " ".join(
            filter(
                None,
                [
                    enquiry.get("firstName"),
                    enquiry.get("middleName"),
                    enquiry.get("lastName"),
                ],
            )
        ).strip()

        return {
            "enquiry_id": enquiry.get("id"),
            "student_name": full_name,
            "class_name": enquiry.get("tenantClassName"),
            "board_name": enquiry.get("boardName"),
            "academic_year": enquiry.get("academicYearName"),
            "enquiry_date": enquiry.get("enquireDate"),
            "followup_date": enquiry.get("followupDate"),
            "status": enquiry.get("status"),
            "interaction_status": enquiry.get("intractionStatus"),
            "enquiry_type": enquiry.get("enquiryType"),
            "father_name": enquiry.get("fatherName"),
            "father_contact": enquiry.get("fatherContact"),
            "father_email": enquiry.get("fatherMailId"),
            "mother_name": enquiry.get("motherName"),
            "raw": enquiry,
        }

    def normalize_fees_collection(self, record: dict):
        return {
            "receipt_id": record.get("id"),
            "date": record.get("date1"),
            "student_name": record.get("name1"),
            "fees_type": record.get("feesType"),
            "amount": record.get("amount") or 0,
            "payment_mode": record.get("paymentMode"),
            "transaction_details": record.get("transDetails"),
            "particular": record.get("particular"),
            "academic_year": record.get("academicYear"),
            "board_name": record.get("boardName"),
            "class_name": record.get("className"),
            "raw": record,
        }
