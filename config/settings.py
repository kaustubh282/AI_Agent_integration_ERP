import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # mock = local JSON, api = live ERP API
    ERP_DATA_MODE = os.getenv("ERP_DATA_MODE", "mock")

    # EdurayzLatest React frontend
    ERP_API_BASE_URL = os.getenv("ERP_API_BASE_URL", "http://43.254.41.48:5102")
    ERP_TENANT_CODE = os.getenv("ERP_TENANT_CODE", "RAHATANI")

    # Login details for /AuthenticateUser
    ERP_USERNAME = os.getenv("ERP_USERNAME")
    ERP_PASSWORD = os.getenv("ERP_PASSWORD")
    ERP_TENANT_ID = int(os.getenv("ERP_TENANT_ID", "0"))
    ERP_ACADEMIC_YEAR_ID = int(os.getenv("ERP_ACADEMIC_YEAR_ID", "0"))
    ERP_TENANT_BOARD_ID = int(os.getenv("ERP_TENANT_BOARD_ID", "0"))
    ERP_USER_ID = int(os.getenv("ERP_USER_ID", "0"))

    # Optional protection for our AI Agent API
    AGENT_API_KEY = os.getenv("AGENT_API_KEY")


settings = Settings()
