"""
PDF Document parser service.

This module provides functions for extracting plain text from PDF documents using pypdf.
"""

import pypdf

def extract_text_from_pdf(file_stream) -> str:
    """Extract plain text from an in-memory PDF file stream."""
    try:
        reader = pypdf.PdfReader(file_stream)
        text = ""
        # Iterate over all pages and merge text blocks
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")
