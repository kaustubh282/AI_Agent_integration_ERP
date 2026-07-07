from clients.erp_api_client import ERPAPIClient

def get_new_admissions(parameters: dict) -> dict:
    date_range = parameters.get("date_range")

    client = ERPAPIClient()
    admissions = client.get_admissions()

    if not admissions:
        return {
            "status": "not_found",
            "message": "No admission records found."
        }

    return {
        "status": "success",
        "type": "new_admission",
        "date_range": date_range,
        "data": admissions
    }