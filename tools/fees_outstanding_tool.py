from clients.erp_api_client import ERPAPIClient


def get_fees_outstanding(parameters: dict) -> dict:
    class_name = parameters.get("class_name")

    client = ERPAPIClient()
    records = client.get_students_with_outstanding_fees(class_name=class_name)

    if not records:
        return {"status": "not_found", "message": "No outstanding fees found."}

    return {"status": "success", "type": "fees_outstanding", "data": records}
