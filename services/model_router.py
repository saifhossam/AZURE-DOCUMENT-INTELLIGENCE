"""
model_router.py — Map display names → Azure prebuilt model IDs
"""

from utils.config import AppConfig


def get_all_model_options() -> dict[str, str]:
    """
    Return a dict of {display_name: model_id} for prebuilt Azure models.
    """
    return dict(AppConfig.MODEL_MAP)


def resolve_model_id(display_name: str) -> str:
    """
    Given a display name from the dropdown, return the Azure model ID.
    Raises ValueError if not found.
    """
    all_models = get_all_model_options()
    if display_name not in all_models:
        raise ValueError(f"Model '{display_name}' not found.")
    return all_models[display_name]


def get_prebuilt_names() -> list[str]:
    """Return the prebuilt model display names."""
    return list(AppConfig.MODEL_MAP.keys())


def get_model_description(display_name: str) -> str:
    """Return a short description for UI tooltips."""
    descriptions = {
        "Layout Analyzer": "Extracts text, tables, and layout structure. No semantic field extraction.",
        "OCR (Read)": "Fast optical character recognition — extracts all raw text, lines, and words.",
        "General Document": "Extracts key-value pairs and text from any document type.",
        "Invoice": "Extracts vendor, customer, line items, totals, dates from invoices.",
        "Receipt": "Extracts merchant, items, subtotals, tax, and total from receipts.",
    }
    return descriptions.get(display_name, "")
