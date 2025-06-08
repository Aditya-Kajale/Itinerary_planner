# utils/helpers.py
import os
import streamlit as st

def load_google_api_key():
    """
    Loads the Google API Key securely from Streamlit secrets or environment variables.
    
    This centralized function ensures consistent key loading across the app.

    Returns:
        str: The API key if found, otherwise None.
    """
    try:
        # Prioritize loading from Streamlit secrets, which is best for deployment.
        api_key = st.secrets["GOOGLE_API_KEY"]
    except (FileNotFoundError, KeyError, AttributeError):
        # Fallback to an environment variable for local development.
        # This allows running the app locally without a secrets.toml file.
        api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        # If the key is not found in either location, display an error.
        # This check prevents the app from proceeding to make API calls that will fail.
        if 'st' in globals() and hasattr(st, 'error'):
             st.error("🔴 Google API Key not found. Please set it in st.secrets or as an environment variable.")
        else:
            # Fallback for running scripts outside of a Streamlit context
            print("ERROR: Google API Key not found. Please set it as an environment variable.")
        return None
        
    return api_key
