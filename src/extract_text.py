import fitz  # PyMuPDF
import os
from loguru import logger
from .segment_sections import segment_into_sections

def process_all_pdfs(docs_folder, filenames):
    """Processes a list of PDF files and returns a flat list of all sections."""
    all_sections = []
    for filename in filenames:
        pdf_path = os.path.join(docs_folder, filename)
        if not os.path.exists(pdf_path):
            logger.warning(f"File not found: {pdf_path}. Skipping.")
            continue
        try:
            doc = fitz.open(pdf_path)
            sections = segment_into_sections(doc, filename)
            all_sections.extend(sections)
            logger.success(f"Extracted {len(sections)} sections from {filename}.")
        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}")
    return all_sections