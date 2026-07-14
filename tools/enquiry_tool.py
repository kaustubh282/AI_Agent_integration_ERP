from clients.erp_api_client import ERPAPIClient


def get_enquiry_report(parameters: dict) -> dict:
    date_range = parameters.get("date_range")
    class_name = parameters.get("class_name")
    show_all = parameters.get("show_all", False)

    client = ERPAPIClient()

    enquiries = client.get_enquiries(
        date_range=date_range,
        class_name=class_name,
    )

    if not enquiries:
        return {
            "status": "not_found",
            "message": "No enquiry records found for the requested filters.",
        }

    return {
        "status": "success",
        "type": "enquiry_report",
        "show_all": show_all,
        "filters": {
            "date_range": date_range or "all",
            "class_name": class_name or "All",
        },
        "data": enquiries,
    }
