import os
from google.cloud import vision
from google.cloud.vision_v1 import types
import logging
import fitz  # pymupdf
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Google Cloud Vision client
try:
    client = vision.ImageAnnotatorClient()
    logger.info("Google Cloud Vision client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Vision client: {str(e)}")
    client = None

def is_scanned_pdf(pdf_path):
    """Check if PDF is likely scanned (image-based)."""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            if not page.get_text("text") and page.get_images(full=True):
                doc.close()
                return True
        doc.close()
        return False
    except Exception as e:
        logger.error(f"Error checking PDF type: {str(e)}")
        return True  # Assume scanned if error occurs

def extract_text_vision(pdf_path):
    """Extract text from PDF using Google Cloud Vision OCR."""
    if client is None:
        logger.warning("Vision client not initialized. Returning empty text.")
        return ""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # Render at 300 DPI
            img_bytes = pix.tobytes("png")
            image = vision.Image(content=img_bytes)
            logger.info(f"Processing page {page_num + 1} with Vision API")
            response = client.text_detection(image=image)
            if response.error.message:
                logger.error(f"Vision API error: {response.error.message}")
                continue
            page_text = response.text_annotations[0].description if response.text_annotations else ""
            text += page_text + "\n"
        doc.close()
        logger.info(f"Extracted text length: {len(text)}")
        return text.strip()
    except Exception as e:
        logger.error(f"Vision extraction error: {str(e)}")
        return ""