"""
model_factory.py — Factory for creating and managing model instances
"""

from typing import Dict, Optional, List
from models.base_model import BaseModel, ModelConfig
from models.ocr_model import OCRModel
from models.layout_model import LayoutModel
from models.general_doc_model import GeneralDocModel
from models.invoice_model import InvoiceModel
from models.receipt_model import ReceiptModel


class ModelFactory:
    """Factory for creating and managing document analysis models."""
    
    # Registry of prebuilt models
    PREBUILT_MODELS: Dict[str, type] = {
        "prebuilt-read": OCRModel,
        "prebuilt-layout": LayoutModel,
        "prebuilt-document": GeneralDocModel,
        "prebuilt-invoice": InvoiceModel,
        "prebuilt-receipt": ReceiptModel,
    }
    
    # Display name to model ID mapping
    DISPLAY_NAME_MAP: Dict[str, str] = {
        "OCR (Read)": "prebuilt-read",
        "Layout Analyzer": "prebuilt-layout",
        "General Document": "prebuilt-document",
        "Invoice": "prebuilt-invoice",
        "Receipt": "prebuilt-receipt",
    }
    
    def __init__(self):
        """Initialize factory with prebuilt models."""
        self._models: Dict[str, BaseModel] = {}
        self._initialize_prebuilt()
    
    def _initialize_prebuilt(self):
        """Initialize all prebuilt models."""
        for model_id, model_class in self.PREBUILT_MODELS.items():
            try:
                self._models[model_id] = model_class()
            except Exception as e:
                print(f"Warning: Failed to initialize {model_id}: {str(e)}")
    
    def get_model(self, model_id: str) -> Optional[BaseModel]:
        """
        Get model by ID.
        
        Args:
            model_id: Model identifier (e.g., 'prebuilt-invoice')
            
        Returns:
            BaseModel instance or None if not found
        """
        return self._models.get(model_id)
    
    def get_model_by_display_name(self, display_name: str) -> Optional[BaseModel]:
        """
        Get model by display name.
        
        Args:
            display_name: Display name (e.g., 'Invoice')
            
        Returns:
            BaseModel instance or None if not found
        """
        model_id = self.DISPLAY_NAME_MAP.get(display_name)
        if model_id:
            return self.get_model(model_id)
        return None
    

    def list_prebuilt_models(self) -> List[Dict[str, str]]:
        """
        Get list of available prebuilt models.
        
        Returns:
            List of dicts with model_id and display_name
        """
        models = []
        for display_name, model_id in self.DISPLAY_NAME_MAP.items():
            models.append({
                "model_id": model_id,
                "display_name": display_name,
            })
        return models
    
    def list_custom_models(self) -> List[Dict[str, str]]:
        """
        Get list of registered custom models.
        
        Returns:
            List of dicts with model_id and display_name
        """
        custom_models = []
        for model_id, model in self._models.items():
            if model.config.category == "custom":
                custom_models.append({
                    "model_id": model_id,
                    "display_name": model.config.display_name,
                })
        return custom_models
    
    def list_all_models(self) -> List[Dict[str, str]]:
        """
        Get list of all available models (prebuilt + custom).
        
        Returns:
            List of dicts with model_id and display_name
        """
        return self.list_prebuilt_models() + self.list_custom_models()
    
    def get_model_config(self, model_id: str) -> Optional[ModelConfig]:
        """
        Get configuration for a model.
        
        Args:
            model_id: Model identifier
            
        Returns:
            ModelConfig or None if not found
        """
        model = self.get_model(model_id)
        if model:
            return model.get_config()
        return None


# Global factory instance
_factory = ModelFactory()


def get_factory() -> ModelFactory:
    """Get the global model factory."""
    return _factory
