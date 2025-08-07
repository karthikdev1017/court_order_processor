from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict
from customer_db import get_customer_id
from actions import execute_action
from vision_preprocessor import is_scanned_pdf, extract_text_vision
import logging
import os
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class State(TypedDict):
    pdf_bytes: bytes
    text: str
    fields: Dict[str, str]
    customer_id: str
    action_result: str

def extract_text(state: State) -> State:
    from utils import extract_text_from_pdf
    logger.info("Extracting text from PDF")
    try:
        # Save pdf_bytes to a temporary file
        temp_pdf_path = "/tmp/temp_pdf.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(state["pdf_bytes"])
        
        # Check if PDF is scanned
        if is_scanned_pdf(temp_pdf_path):
            logger.info("Detected scanned PDF, using Vision API")
            state["text"] = extract_text_vision(temp_pdf_path)
        else:
            logger.info("Detected regular PDF, using pymupdf")
            state["text"] = extract_text_from_pdf(state["pdf_bytes"])
        
        # Clean up temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        
        logger.info(f"Extracted text length: {len(state['text'])}")
    except Exception as e:
        logger.error(f"Text extraction failed: {str(e)}")
        state["text"] = ""
    return state

def extract_fields_node(state: State) -> State:
    from utils import extract_fields
    logger.info("Extracting fields from text")
    state["fields"] = extract_fields(state["text"])
    return state

def check_customer(state: State) -> State:
    national_id = state["fields"].get("national_id")
    logger.info(f"Checking customer for national_id: {national_id}")
    state["customer_id"] = get_customer_id(national_id) if national_id else None
    return state

def process_action(state: State) -> State:
    customer_id = state["customer_id"]
    action = state["fields"].get("action")
    logger.info(f"Processing action {action} for customer_id {customer_id}")
    state["action_result"] = execute_action(customer_id, action)
    return state

def reject_not_found(state: State) -> State:
    national_id = state["fields"].get("national_id")
    state["action_result"] = f"National ID {national_id or 'None'} not found. Order discarded."
    logger.info(state["action_result"])
    return state

def reject_invalid_action(state: State) -> State:
    action = state["fields"].get("action")
    state["action_result"] = f"Invalid action '{action}'. Cannot process."
    logger.info(state["action_result"])
    return state

def decide_next_step(state: State) -> str:
    if not state["customer_id"]:
        return "reject_not_found"
    if not state["fields"].get("action") or state["fields"]["action"] not in execute_action.__globals__["ACTION_NAMES"]:
        return "reject_invalid_action"
    return "process_action"

workflow = StateGraph(State)
workflow.add_node("extract_text", extract_text)
workflow.add_node("extract_fields", extract_fields_node)
workflow.add_node("check_customer", check_customer)
workflow.add_node("process_action", process_action)
workflow.add_node("reject_not_found", reject_not_found)
workflow.add_node("reject_invalid_action", reject_invalid_action)
workflow.add_conditional_edges("check_customer", decide_next_step, {
    "process_action": "process_action",
    "reject_not_found": "reject_not_found",
    "reject_invalid_action": "reject_invalid_action"
})
workflow.add_edge("extract_text", "extract_fields")
workflow.add_edge("extract_fields", "check_customer")
workflow.add_edge("process_action", END)
workflow.add_edge("reject_not_found", END)
workflow.add_edge("reject_invalid_action", END)
workflow.set_entry_point("extract_text")

app = workflow.compile()

def process_document(pdf_bytes: bytes) -> str:
    try:
        state = app.invoke({"pdf_bytes": pdf_bytes})
        return state["action_result"]
    except Exception as e:
        logger.error(f"Error in workflow: {str(e)}")
        return f"Error processing document: {str(e)}"