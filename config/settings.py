import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    ERP_DATA_MODE = os.getenv("ERP_DATA_MODE", "mock")
    ERP_API_BASE_URL = os.getenv("ERP_API_BASE_URL")
    ERP_API_KEY = os.getenv("ERP_API_KEY")


settings = Settings()
