import re
import fitz  # PyMuPDF
from llm_extractor import extract_fields_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        logger.info(f"Extracted text: {text[:200]}...")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def extract_fields(text):
    try:
        normalized_text = re.sub(r'\s+', ' ', text.strip())
        logger.info(f"Normalized text: {normalized_text[:200]}...")
        nid_match = re.search(r"\b(?:National ID|ID|NID|identification number)\s*(?:number)?[:\s]*([0-9\s]{6,})\b", text, re.IGNORECASE)
        action_match = re.search(r"\bAction[:\s]*(freeze_account|release_funds|suspend_accounts|issue_notice)\b", normalized_text, re.IGNORECASE)
        national_id = nid_match.group(1).replace(" ", "") if nid_match else None
        action = action_match.group(1) if action_match else None
        if national_id:
            logger.info(f"Extracted national_id via regex: {national_id}")
        else:
            logger.info("No national_id found via regex")
        if action:
            logger.info(f"Extracted action via regex: {action}")
        else:
            logger.info("No action found via regex, falling back to LLM")
        if national_id and action:
            return {"national_id": national_id, "action": action}
        logger.info("Falling back to LLM extraction")
        return extract_fields_llm(text)
    except Exception as e:
        logger.error(f"Error extracting fields: {str(e)}")
        return {"national_id": None, "action": None}