import os
import json
import requests # For making HTTP requests
import streamlit as st

# --- Configuration ---
# Module-level variable to store the API key once loaded.
_GOOGLE_API_KEY = None

def _load_api_key():
    """Loads the Google API Key from Streamlit secrets or environment variables."""
    global _GOOGLE_API_KEY
    if _GOOGLE_API_KEY:  # Avoid reloading if already loaded
        return

    try:
        # Try Streamlit secrets first (for deployment)
        _GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except (FileNotFoundError, KeyError, AttributeError):
        # AttributeError can happen if st.secrets is not available (e.g. running script directly)
        # Fallback to environment variable (for local development)
        _GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    
    # No st.error here; the function using the key will handle its absence.

_load_api_key() # Attempt to load the API key when the module is imported.

# Define the Imagen API endpoint template.
# As per platform guidelines for imagen-3.0-generate-002, the API key is part of the URL.
IMAGEN_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
PLACEHOLDER_IMAGE_URL_PREFIX = "https://placehold.co/600x400/CCCCCC/444444?text="

def generate_image_from_text_prompt(prompt_text: str) -> str:
    """
    Generates an image from a text prompt using the Imagen API.

    Args:
        prompt_text (str): The text prompt to generate an image from.

    Returns:
        str: A data URI (data:image/png;base64,...) for the generated image,
             or a placeholder image URL if an error occurs.
    """
    _load_api_key() # Ensure key is loaded if module was reloaded or something unusual happened

    if not _GOOGLE_API_KEY:
        if 'st' in globals() and hasattr(st, 'error'): # Check if Streamlit context exists
            st.error("🔴 Imagen API: Google API Key is not configured. Cannot generate image.")
        else:
            print("ERROR: Imagen API - Google API Key is not configured.")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}API_Key_Missing"

    api_url = IMAGEN_API_URL_TEMPLATE.format(api_key=_GOOGLE_API_KEY)
    
    payload = {
        "instances": [{"prompt": prompt_text}],
        "parameters": {"sampleCount": 1}  # Generate one image
    }
    
    headers = {"Content-Type": "application/json"}

    try:
        # The spinner should be in the calling function (app.py) for better UI control
        response = requests.post(api_url, headers=headers, json=payload, timeout=90) # Increased timeout for image generation
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)

        result = response.json()

        if result.get("predictions") and \
           len(result["predictions"]) > 0 and \
           result["predictions"][0].get("bytesBase64Encoded"):
            base64_image_data = result["predictions"][0]["bytesBase64Encoded"]
            image_data_uri = f"data:image/png;base64,{base64_image_data}"
            return image_data_uri
        else:
            error_message = "Imagen API response missing image data."
            if 'st' in globals() and hasattr(st, 'warning'):
                st.warning(f"⚠️ {error_message} For prompt: '{prompt_text[:30]}...'")
            else:
                print(f"WARNING: {error_message} For prompt: '{prompt_text[:30]}...'")
            # print(f"Unexpected Imagen response structure: {json.dumps(result, indent=2)}") # For debugging
            return f"{PLACEHOLDER_IMAGE_URL_PREFIX}Response_Error"
            
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error with Imagen API: {http_err}."
        try:
            # Try to get more details from the response if available
            error_details = http_err.response.json()
            error_message += f" Details: {error_details.get('error', {}).get('message', str(error_details))}"
        except ValueError: # If response is not JSON
            error_message += f" Response: {http_err.response.text[:200]}" # Show start of non-JSON response

        if 'st' in globals() and hasattr(st, 'error'):
            st.error(f"🔴 {error_message}")
        else:
            print(f"ERROR: {error_message}")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}HTTP_Error"
    except requests.exceptions.RequestException as req_err: # Other network errors
        if 'st' in globals() and hasattr(st, 'error'):
            st.error(f"🔴 Request error with Imagen API: {req_err}")
        else:
            print(f"ERROR: Request error with Imagen API: {req_err}")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}Request_Error"
    except Exception as e:
        if 'st' in globals() and hasattr(st, 'error'):
            st.error(f"🔴 Unexpected error with Imagen API: {e}")
        else:
            print(f"ERROR: Unexpected error with Imagen API: {e}")
        return f"{PLACEHOLDER_IMAGE_URL_PREFIX}Unexpected_Error"

# --- Example Usage (for testing this file directly) ---
if __name__ == "__main__":
    print("Testing Imagen Client...")
    # To test, set GOOGLE_API_KEY environment variable
    # For example: export GOOGLE_API_KEY="your_actual_api_key"
    _load_api_key() # Explicitly load for direct script run
    if not _GOOGLE_API_KEY:
        print("Please set the GOOGLE_API_KEY environment variable to test.")
    else:
        sample_prompt = "A photorealistic image of a red apple on a wooden table, soft lighting"
        print(f"\nRequesting image for prompt: '{sample_prompt}'")
        
        image_output = generate_image_from_text_prompt(sample_prompt)

        if image_output and image_output.startswith("data:image/png;base64,"):
            print(f"\nSuccessfully generated image data URI.")
            print(f"Output (first 70 chars): {image_output[:70]}...")
            # To view, you could write the base64 part to a file or use a tool.
        else:
            print(f"\nFailed to generate image. Received: {image_output}")
