from clients.erp_api_client import ERPAPIClient

client = ERPAPIClient()

try:
    client.authenticate()
    print("✅ ERP LOGIN SUCCESS")

    print("\n1. New Admissions / Students")
    students = client.get_students()
    print("Total:", len(students))
    print(students[:2])

    print("\n2. Attendance API")
    attendance_payload = {
        "academicYearId": client.academic_year_id,
        "tenantBoardId": client.tenant_board_id,
        "tenantClassId": 2,
        "sectionId": 1,
        "studentId": 1075,
    }
    try:
        attendance = client.get_cbse_student_attendance(attendance_payload)
        print(type(attendance))
        print(attendance)
    except Exception as e:
        print("Attendance failed:", e)

    print("\n3. Fees Outstanding / Student Fees")
    try:
        fees = client.get_student_fees_detail(1075)
        print(type(fees))
        print(fees)
    except Exception as e:
        print("Fees failed:", e)

    print("\n4. Class Exam Details")
    try:
        exams = client.get_class_exam_details(2)
        print(type(exams))
        print(exams)
    except Exception as e:
        print("Exam failed:", e)

    print("\n5. Student Marks Classwise")
    marks_payload = {
        "tenantId": client.tenant_id,
        "tenantBoardId": client.tenant_board_id,
        "academicYearId": client.academic_year_id,
        "tenantClassId": 2,
        "sectionId": 1,
        "studentId": 1075,
    }
    try:
        marks = client.get_student_marks_classwise(marks_payload)
        print(type(marks))
        print(marks)
    except Exception as e:
        print("Marks failed:", e)

    print("\n6. Communication APIs not confirmed yet")
    print("Need GET homework/notice/circular APIs from backend or Swagger.")

    print("\n7. Expenses")
    print("No direct expense API confirmed from frontend yet.")

except Exception as e:
    print("❌ TEST FAILED")
    print(e)
