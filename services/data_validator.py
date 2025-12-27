"""
data_validator.py
-----------------

Purpose:
- Securely connect to Ollama Cloud using API key from .env
- Extract structured scheduling data from natural language input
- Return JSON-ready values for ontology validation

Design:
- LLM is used ONLY for data extraction
- No scheduling decisions are made here
- Fully separated from UI and ontology logic
"""

import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv
import os


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if not OLLAMA_API_KEY or not OLLAMA_API_URL or not OLLAMA_MODEL:
    raise EnvironmentError(
        "Missing required environment variables. "
        "Check OLLAMA_API_KEY, OLLAMA_API_URL, and OLLAMA_MODEL in .env file."
    )


# --------------------------------------------------
# Ollama Cloud API Call
# --------------------------------------------------

def call_ollama(messages: list) -> str:
    """
    Sends a request to the local Ollama server and returns model output.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=180
        )

        response.raise_for_status()
        result = response.json()

        # Ollama returns response here
        return result["message"]["content"].strip()

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"Ollama returned an HTTP error.\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Ollama communication failed: {str(e)}"
        )



# --------------------------------------------------
# Natural Language → Structured Data
# --------------------------------------------------

def extract_schedule_data(user_prompt: str) -> Dict[str, Any]:
    """
    Extracts structured hospital scheduling information
    from a natural language user prompt.

    Returns a dictionary with:
    - surgeon_name
    - patient_name
    - operation_type
    - theatre_name
    - date
    - start_time
    - end_time
    """

    system_prompt = (
        "You are a hospital scheduling assistant.\n"
        "Your task is to extract structured data from user requests.\n"
        "You MUST return valid JSON only.\n"
        "Do not add explanations, comments, or extra text."
    )

    user_prompt_instruction = f"""
Extract the following fields from the request.
If a value is missing or not mentioned, return null.

Fields:
- surgeon_name
- patient_name
- operation_type
- theatre_name
- date
- start_time
- end_time

Request:
\"\"\"{user_prompt}\"\"\"
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_instruction}
    ]

    try:
        raw_response = call_ollama(messages)
        extracted_data = json.loads(raw_response)

    except json.JSONDecodeError:
        extracted_data = {
            "error": "Invalid JSON returned by LLM",
            "raw_response": raw_response
        }

    except Exception as e:
        extracted_data = {
            "error": "Failed to extract scheduling data",
            "details": str(e)
        }

    return extracted_data
