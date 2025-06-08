# utils/gemini_client.py

import os
import json
import streamlit as st
import google.generativeai as genai
# Import the new prompt creation function
from prompts.itinerary_prompts import create_itinerary_prompt

# --- Configuration ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        st.error(f"🔴 Error configuring Google AI SDK: {e}")
else:
    if 'st' in globals() and hasattr(st, 'error'):
        st.error("🔴 Google API Key is missing. Please set it in st.secrets or as an environment variable.")

# --- Model Initialization ---
def get_gemini_model(model_name="gemini-2.0-flash"):
    """Initializes and returns a GenerativeModel instance."""
    try:
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        st.error(f"🔴 Error initializing Gemini model ({model_name}): {e}")
        return None

# --- Core Function to Get Itinerary ---
def get_itinerary_from_gemini(interests, time_available, budget, location_query):
    """
    Generates itinerary suggestions using the Gemini API.
    """
    if not GOOGLE_API_KEY:
        st.error("🔴 Gemini API cannot be called: Google API Key is not configured.")
        return None, None

    model = get_gemini_model()
    if not model:
        return None, None

    # --- UPDATED: Use the imported function to create the prompt ---
    prompt_template = create_itinerary_prompt(
        interests, time_available, budget, location_query
    )

    try:
        st.info(f"⚙️ Calling Gemini API for {location_query}...")
        response = model.generate_content(prompt_template)

        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_response_text)
        
        suggested_places = data.get("suggested_places", [])
        itinerary_steps = data.get("itinerary_steps", [])

        if not suggested_places and not itinerary_steps:
            st.warning("⚠️ Gemini returned an empty response. Try different inputs.")
        
        st.success("✅ Successfully received and parsed suggestions from Gemini!")
        return suggested_places, itinerary_steps

    except json.JSONDecodeError as e:
        st.error(f"🔴 Error parsing JSON response from Gemini: {e}")
        st.error(f"Raw Gemini response snippet: {response.text[:500]}...")
        return None, None
    except Exception as e:
        st.error(f"🔴 An unexpected error occurred while interacting with Gemini API: {e}")
        return None, None
