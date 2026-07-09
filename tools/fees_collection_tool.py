from clients.erp_api_client import ERPAPIClient


def get_fees_collection(parameters: dict) -> dict:
    class_name = parameters.get("class_name")
    date_range = parameters.get("date_range")
    show_all = parameters.get("show_all", False)

    client = ERPAPIClient()
    records = client.get_fee_collections(
        date_range=date_range,
        class_name=class_name,
    )

    if not records:
        return {
            "status": "not_found",
            "message": "No fees collection records found.",
        }

    return {
        "status": "success",
        "type": "fees_collection",
        "show_all": show_all,
        "data": records,
    }
