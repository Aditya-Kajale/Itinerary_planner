# utils/imagen_client.py

import json
import requests
import streamlit as st
# --- UPDATED: Import the new helper function ---
from utils.helpers import load_google_api_key

# --- UPDATED: Simplified Configuration ---
_GOOGLE_API_KEY = load_google_api_key()

IMAGEN_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
PLACEHOLDER_IMAGE_URL_PREFIX = "https://placehold.co/600x400/CCCCCC/444444?text="

def generate_image_from_text_prompt(prompt_text: str) -> str:
    """
    Generates an image from a text prompt using the Imagen API.
    """
    if not _GOOGLE_API_KEY:
        # The error is already shown by the helper, just return a placeholder.
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}API_Key_Missing"

    api_url = IMAGEN_API_URL_TEMPLATE.format(api_key=_GOOGLE_API_KEY)
    
    payload = {
        "instances": [{"prompt": prompt_text}],
        "parameters": {"sampleCount": 1}
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()

        result = response.json()

        if result.get("predictions") and result["predictions"][0].get("bytesBase64Encoded"):
            base64_image_data = result["predictions"][0]["bytesBase64Encoded"]
            return f"data:image/png;base64,{base64_image_data}"
        else:
            st.warning(f"⚠️ Imagen API response missing image data for prompt: '{prompt_text[:30]}...'")
            return f"{PLACEHOLDER_IMAGE_URL_PREFIX}Response_Error"
            
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error with Imagen API: {http_err}."
        try:
            error_details = http_err.response.json()
            error_message += f" Details: {error_details.get('error', {}).get('message', str(error_details))}"
        except ValueError:
            error_message += f" Response: {http_err.response.text[:200]}"

        st.error(f"🔴 {error_message}")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}HTTP_Error"
    except requests.exceptions.RequestException as req_err:
        st.error(f"🔴 Request error with Imagen API: {req_err}")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}Request_Error"
    except Exception as e:
        st.error(f"🔴 Unexpected error with Imagen API: {e}")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}Unexpected_Error"
