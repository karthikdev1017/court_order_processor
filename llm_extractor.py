import os
import openai
import json
from actions import ACTION_NAMES
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    client = None

def validate_national_id(nid):
    return bool(nid and re.match(r"^\d{10,12}$", str(nid)))

def extract_fields_llm(text):
    if client is None:
        logger.warning("OpenAI client not initialized. Returning null values.")
        return {"national_id": None, "action": None}

    actions_list = ", ".join(sorted(ACTION_NAMES))
    prompt = f"""
Extract the following fields from the court order text:
- national_id: A 10- to 12-digit number.
- action: One of: {actions_list}. Infer the action if not explicitly listed, e.g.:
  - "Freeze all associated bank accounts" → "freeze_account"
  - "release funds" → "release_funds"
  - "accounts suspended" → "suspend_accounts"
  - "issue notice" → "issue_notice"

Return a JSON object in this exact format:
{{"national_id": "<value>", "action": "<value>"}}

If no valid fields are found, return:
{{"national_id": null, "action": null}}

Text:
{text}
"""
    try:
        logger.info(f"LLM input text: {text[:200]}...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a precise document parser. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        if not response or not response.choices:
            logger.error("OpenAI API returned no choices.")
            return {"national_id": None, "action": None}

        content = response.choices[0].message.content.strip()
        logger.info(f"Raw content from LLM: {repr(content)}")

        if not content:
            logger.error("LLM returned empty content.")
            return {"national_id": None, "action": None}

        try:
            result = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.error(f"LLM returned non-JSON content: {repr(content)}")
            return {"national_id": None, "action": None}

        national_id = result.get("national_id")
        action = result.get("action")

        if not validate_national_id(national_id):
            logger.warning(f"Invalid national_id format: {national_id}")
            national_id = None
        if action not in ACTION_NAMES:
            logger.warning(f"Invalid action: {action}")
            action = None

        logger.info(f"LLM extracted: national_id={national_id}, action={action}")
        return {
            "national_id": national_id,
            "action": action
        }
    except Exception as e:
        logger.error(f"LLM extraction error: {str(e)}")
        return {"national_id": None, "action": None}