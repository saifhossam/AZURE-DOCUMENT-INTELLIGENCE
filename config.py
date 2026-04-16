"""
config.py — Single source of truth for all app settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class AzureConfig:
    """Azure Document Intelligence credentials."""
    ENDPOINT: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    KEY: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    @classmethod
    def is_configured(cls) -> bool:
        return bool(cls.ENDPOINT and cls.KEY)


class AppConfig:
    """General app settings."""
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs")
    SUPPORTED_EXTENSIONS: list = [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
    MAX_FILE_SIZE_MB: int = 50
