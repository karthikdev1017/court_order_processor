import os
import openai
import json
from actions import ACTION_NAMES
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = openai.OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    client = None

def validate_national_id(nid):
    return bool(nid and re.match(r"^\d{10,12}$", str(nid)))

def extract_fields_llm(text):
    if client is None:
        logger.warning("OpenAI client not initialized")
        return {
            "national_id": None,
            "action": None,
            "status": "error",
            "error_message": "OpenAI client not initialized"
        }
    actions_list = ", ".join(sorted(ACTION_NAMES))
    prompt = f"""
Extract from the court order text:
- national_id: A 10- to 12-digit number.
- action: One of: {actions_list}. Infer if not explicit, e.g.:
  - "Freeze all associated bank accounts" → "freeze_account"
  - "release funds" → "release_funds"
  - "accounts suspended" → "suspend_accounts"
  - "issue notice" → "issue_notice"
Return JSON:
{{
  "national_id": "<value>",
  "action": "<value>",
  "status": "success",
  "error_message": ""
}}
If no valid fields, return null values with status "error" and an error_message.
Text:
{text}
"""
    try:
        logger.info(f"LLM input text: {text[:200]}...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        if not response or not response.choices:
            logger.error("OpenAI API returned no choices")
            return {
                "national_id": None,
                "action": None,
                "status": "error",
                "error_message": "OpenAI API returned no choices"
            }
        content = response.choices[0].message.content.strip()
        logger.info(f"Raw content from LLM: {repr(content)}")
        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return {
                "national_id": None,
                "action": None,
                "status": "error",
                "error_message": f"JSON parsing failed: {str(e)}"
            }
        national_id = result.get("national_id")
        action = result.get("action")
        if not validate_national_id(national_id):
            logger.warning(f"Invalid national_id format: {national_id}")
            national_id = None
            result["status"] = "error"
            result["error_message"] = f"Invalid national_id format: {national_id}"
        if action not in ACTION_NAMES:
            logger.warning(f"Invalid action: {action}")
            action = None
            result["status"] = "error"
            result["error_message"] = f"Invalid action: {action}"
        logger.info(f"LLM extracted: national_id={national_id}, action={action}")
        return {
            "national_id": national_id,
            "action": action,
            "status": result.get("status", "success"),
            "error_message": result.get("error_message", "")
        }
    except Exception as e:
        logger.error(f"LLM extraction error: {str(e)}")
        return {
            "national_id": None,
            "action": None,
            "status": "error",
            "error_message": f"LLM extraction error: {str(e)}"
        }