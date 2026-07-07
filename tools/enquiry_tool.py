from clients.erp_api_client import ERPAPIClient


def get_enquiry_report(parameters: dict) -> dict:
    date_range = parameters.get("date_range")

    client = ERPAPIClient()
    enquiries = client.get_enquiries()

    if not enquiries:
        return {"status": "not_found", "message": "No enquiry records found."}

    return {
        "status": "success",
        "type": "enquiry_report",
        "date_range": date_range,
        "data": enquiries,
    }
