"""
main.py — Streamlit app entry point; ties together layout, display, and inference
"""

import streamlit as st
from typing import Optional
import tempfile
import os

from ui.layout import (
    configure_page,
    apply_custom_styling,
    setup_sidebar,
    render_header,
    render_summary_metrics,
    render_metadata,
)
from ui.display import (
    render_results_tabs,
    render_error_message,
    render_success_message,
    render_pages_summary,
)
from controllers.inference_controller import run_inference
from utils.config import AppConfig


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "upload_filename" not in st.session_state:
        st.session_state.upload_filename = None
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None


def page_upload_analyze():
    """Upload & Analyze page."""
    st.subheader("📤 Upload & Analyze Document")
    
    st.write(
        "Upload a document to extract and analyze data using Azure Document Intelligence."
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a document:",
        type=[ext.lstrip(".") for ext in AppConfig.SUPPORTED_EXTENSIONS],
        help="Supported formats: PDF, PNG, JPG, JPEG, TIFF, BMP",
    )
    
    if uploaded_file is not None:
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filename", uploaded_file.name)
        with col2:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.metric("File Size", f"{file_size_mb:.2f} MB")
        with col3:
            file_ext = os.path.splitext(uploaded_file.name)[1].upper()
            st.metric("Type", file_ext)
        
        st.divider()
        
        # Get model from sidebar
        model_display_name = st.session_state.selected_model
        
        # Analysis button
        if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
            # Read file bytes
            file_bytes = uploaded_file.read()
            
            # Run inference with spinner
            with st.spinner("🔄 Sending document to Azure and analyzing..."):
                result = run_inference(
                    file_bytes=file_bytes,
                    filename=uploaded_file.name,
                    model_display_name=model_display_name,
                )
            
            # Store result in session state
            st.session_state.analysis_result = result
            st.session_state.upload_filename = uploaded_file.name
            
            # Display result
            if result["success"]:
                render_success_message(result.get("saved_json_path", ""))
                
                # Show metrics
                st.divider()
                render_summary_metrics(result["parsed"])
                
                # Show metadata
                st.divider()
                render_metadata(result["parsed"])
                
                # Show pages summary
                st.divider()
                render_pages_summary(result["parsed"])
                
                # Show detailed results in tabs
                st.divider()
                render_results_tabs(result["parsed"])
            else:
                render_error_message(result["error"])
    
    else:
        st.info("👆 Upload a document to get started.")


def page_view_results():
    """View Results page."""
    st.subheader("📊 View Analysis Results")
    
    if st.session_state.analysis_result is None:
        st.info("📋 No analysis results yet. Go to **Upload & Analyze** tab to analyze a document.")
        return
    
    result = st.session_state.analysis_result
    
    if not result["success"]:
        st.error(f"❌ Previous analysis failed: {result['error']}")
        return
    
    parsed = result["parsed"]
    
    st.write(f"**Document:** {parsed['meta']['filename']}")
    st.write(f"**Model:** {parsed['meta']['model']}")
    
    st.divider()
    
    # Show metrics
    render_summary_metrics(parsed)
    
    st.divider()
    
    # Show metadata
    render_metadata(parsed)
    
    st.divider()
    
    # Show pages summary
    render_pages_summary(parsed)
    
    st.divider()
    
    # Show results tabs
    render_results_tabs(parsed)


def page_model_info():
    """Model Info page."""
    st.subheader("📋 Supported Models")
    
    st.markdown(
        """
        This application supports the following Azure Document Intelligence prebuilt models:
        """
    )
    
    st.divider()
    
    # Model information
    model_info = {
        "Layout Analyzer": {
            "id": "prebuilt-layout",
            "description": "Extracts text, tables, and layout structure from documents.",
            "best_for": "General documents, reports, forms with tables",
            "features": ["Text extraction", "Table detection", "Layout analysis"],
        },
        "OCR (Read)": {
            "id": "prebuilt-read",
            "description": "Optical Character Recognition for extracting all text from documents.",
            "best_for": "Scanned documents, images, PDFs",
            "features": ["Text recognition", "Handwriting detection", "Multi-language support"],
        },
        "General Document": {
            "id": "prebuilt-document",
            "description": "Extracts key information and entities from general documents.",
            "best_for": "Mixed document types without specific structure",
            "features": ["Entity extraction", "Key-value pairs", "Table detection"],
        },
        "Invoice": {
            "id": "prebuilt-invoice",
            "description": "Specialized for invoice analysis and data extraction.",
            "best_for": "Financial documents, invoices, billing records",
            "features": [
                "Invoice number extraction",
                "Amount parsing",
                "Vendor/customer info",
                "Line item extraction",
            ],
        },
        "Receipt": {
            "id": "prebuilt-receipt",
            "description": "Optimized for receipt and transaction document analysis.",
            "best_for": "Receipts, tickets, transaction records",
            "features": [
                "Total amount extraction",
                "Merchant detection",
                "Transaction items",
                "Date/time parsing",
            ],
        },
    }
    
    for model_name, info in model_info.items():
        with st.expander(f"**{model_name}** — {info['id']}", expanded=False):
            st.write(f"**Description:** {info['description']}")
            st.write(f"**Best for:** {info['best_for']}")
            st.write("**Features:**")
            for feature in info["features"]:
                st.write(f"  • {feature}")
    
    st.divider()
    
    # File format info
    st.subheader("Supported File Formats")
    st.write(
        f"""
        - **Image formats:** PNG, JPG, JPEG, BMP, TIFF
        - **Document formats:** PDF
        - **Maximum file size:** {AppConfig.MAX_FILE_SIZE_MB} MB
        """
    )
    
    st.divider()
    
    # Tips
    st.subheader("Tips for Best Results")
    st.markdown(
        """
        1. **Document Quality:** Ensure documents are clear and well-lit.
        2. **Resolution:** For images, use minimum 200 DPI for best OCR results.
        3. **Orientation:** Make sure documents are properly oriented.
        4. **Model Selection:** Choose the model that best matches your document type.
        5. **File Size:** Keep files under the 50 MB limit.
        """
    )


def main():
    """Main Streamlit app."""
    # Configure page
    configure_page()
    apply_custom_styling()
    
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Setup sidebar and get navigation
    page, selected_model = setup_sidebar()
    st.session_state.selected_model = selected_model
    
    # Route to appropriate page
    if page == "📤 Upload & Analyze":
        page_upload_analyze()
    elif page == "📊 View Results":
        page_view_results()
    elif page == "📋 Model Info":
        page_model_info()


if __name__ == "__main__":
    main()
