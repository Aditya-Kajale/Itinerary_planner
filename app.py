import streamlit as st
import os
import concurrent.futures

# Import the client functions from your utils package
from utils.gemini_client import get_itinerary_from_gemini
from utils.imagen_client import generate_image_from_text_prompt

# --- Page Configuration ---
st.set_page_config(
    page_title="Your Trip, My Problem (Solving)",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- NEW FUNCTION TO LOAD CSS ---
def load_css(file_name):
    """Loads a CSS file and injects it into the app."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Don't worry if the CSS file is not found, the app will still work.
        pass

# --- UI Sections ---
def main():
    # --- APPLY CUSTOM CSS ---
    load_css("assets/style.css")

    # --- Sidebar for User Inputs ---
    with st.sidebar:
        st.header("✨ Plan Your Trip")
        st.markdown("---")

        interests_input = st.text_area(
            "Enter your interests (e.g., history, food, nature, art, shopping)",
            "historical sites, local cuisine, scenic viewpoints"
        )
        location_query_input = st.text_input(
            "What city or area are you interested in?",
            "Chhatrapati Sambhaji Nagar"
        )
        time_available_options = ["A few hours (2-3)", "Half-day (4-5 hours)", "Full-day (6-8 hours)"]
        time_available_input = st.selectbox("How much time do you have?", time_available_options)

        budget_options = ["💰 Budget-friendly (Free to low cost)", "💰💰 Moderate (Mid-range)", "💰💰💰 Flexible (Willing to spend)"]
        budget_input = st.selectbox("What's your budget preference?", budget_options)

        st.markdown("---")

        if st.button("🚀 Generate Itinerary", type="primary", use_container_width=True):
            if not interests_input or not location_query_input:
                st.warning("Please enter your interests and a location to get suggestions.")
            else:
                interests_list = [interest.strip() for interest in interests_input.split(',') if interest.strip()]
                if not interests_list:
                    st.warning("Please provide valid interests.")
                else:
                    st.session_state.itinerary_generated = False
                    st.session_state.places = None
                    st.session_state.itinerary_steps = None

                    with st.spinner("Thinking of the best spots and crafting your itinerary... ✨"):
                        places_data, itinerary_steps_data = get_itinerary_from_gemini(
                            interests_list, time_available_input, budget_input, location_query_input
                        )

                    if places_data:
                        with st.spinner("Generating images for your trip... 📸 (This might take a moment)"):
                            image_prompts = [p.get('image_prompt', f"Image of {p.get('name', 'a nice place')}") for p in places_data]

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                image_urls = list(executor.map(generate_image_from_text_prompt, image_prompts))

                            for i, place in enumerate(places_data):
                                place['image_url'] = image_urls[i]

                    if places_data is not None and itinerary_steps_data is not None:
                        if not places_data and not itinerary_steps_data:
                             st.info("We couldn't find specific suggestions for your query. Try broadening your interests or location!")
                        else:
                            st.session_state.places = places_data
                            st.session_state.itinerary_steps = itinerary_steps_data
                            st.session_state.itinerary_generated = True
                            st.success("Your personalized itinerary is ready!")
                    else:
                        st.error("Sorry, something went wrong while generating the itinerary. Please try again.")

        st.markdown("---")

    # --- Main Content Area ---
    st.header("Your Trip, My Problem (Solving)")
    st.markdown("We're doing the hard work to plan your trip, so you don't have to.")
    
    if 'itinerary_generated' in st.session_state and st.session_state.itinerary_generated:
        if 'places' in st.session_state and st.session_state.places:
            st.subheader("📍 Your Suggested Places")
            num_places = len(st.session_state.places)
            cols = st.columns(min(num_places, 3) if num_places > 0 else 1)

            for i, place in enumerate(st.session_state.places):
                with cols[i % min(num_places, 3) if num_places > 0 else 0]:
                    with st.container(border=True):
                        st.markdown(f"**{place.get('name', 'N/A')}**")
                        image_url_or_data_uri = place.get('image_url')
                        if image_url_or_data_uri:
                            st.image(image_url_or_data_uri, caption=f"Visual for {place.get('name', 'N/A')}", use_container_width=True)
                        else:
                            st.info("Image could not be generated.")
                        st.markdown(f"*{place.get('description', 'No description available.')}*")

        if 'itinerary_steps' in st.session_state and st.session_state.itinerary_steps:
            st.subheader("📜 Your Personalized Itinerary")
            with st.container(border=True):
                for step in st.session_state.itinerary_steps:
                    st.markdown(f"&nbsp;&nbsp;•&nbsp; {step}")
        else:
            st.info("No detailed itinerary steps were generated.")
            
    else:
        st.info("Enter your preferences in the sidebar and click 'Generate Itinerary' to start your adventure planning!")

    # --- Open Innovation Section  ---
    st.markdown("---")
    with st.expander("💡 Open Innovation Corner: Help Us Improve!"):
        user_feedback = st.text_area("Have a suggestion for a place or a feature? (Conceptual for now)")
        if st.button("Submit Feedback (Conceptual)", use_container_width=False):
            if user_feedback:
                st.toast("Thanks for your feedback! (This is a conceptual feature for the hackathon)")
            else:
                st.toast("Please enter some feedback first.")


if __name__ == "__main__":
    if not os.path.exists("utils"):
        os.makedirs("utils")
    if not os.path.exists("prompts"):
        os.makedirs("prompts")
    if not os.path.exists("assets"):
        os.makedirs("assets")
    main()
