# prompts/itinerary_prompts.py

def create_itinerary_prompt(interests, time_available, budget, location_query):
    """
    Constructs the prompt for the Gemini API to generate an itinerary.

    Args:
        interests (list): List of user's interests.
        time_available (str): User's available time.
        budget (str): User's budget preference.
        location_query (str): The city or area of interest.

    Returns:
        str: The fully formatted prompt string.
    """
    prompt_template = f"""
    You are an expert local tour guide and itinerary planner.
    A user is looking for things to do in "{location_query}".
    Their preferences are:
    - Interests: {', '.join(interests)}
    - Time Available: {time_available}
    - Budget: {budget}

    Please suggest 3-4 relevant places or activities. For each place/activity, provide:
    1. "name": A concise name for the place/activity.
    2. "description": A brief, engaging description (1-2 sentences).
    3. "image_prompt": A short, descriptive prompt (5-10 words) that could be used to generate a representative image for this place/activity (e.g., "bustling local market scene," "serene park pathway," "historic building facade detail").

    Then, create a simple, step-by-step itinerary that logically connects these places/activities within the given timeframe and budget.
    The itinerary should be a list of strings.

    Please format your entire response as a single JSON object with two main keys: "suggested_places" (a list of objects) and "itinerary_steps" (a list of strings).

    Example of the desired JSON structure:
    {{
      "suggested_places": [
        {{
          "name": "Example Place 1",
          "description": "A wonderful place to visit with historical significance.",
          "image_prompt": "ancient ruins sunny day"
        }},
        {{
          "name": "Example Cafe Vista",
          "description": "Enjoy local delicacies with a great view.",
          "image_prompt": "cozy cafe mountain view"
        }}
      ],
      "itinerary_steps": [
        "Morning: Visit Example Place 1 and explore its history.",
        "Lunch: Head to Example Cafe Vista for a delicious meal.",
        "Afternoon: Take a leisurely walk in the nearby park (optional)."
      ]
    }}

    Ensure the response is only the JSON object and nothing else.
    Provide suggestions specifically relevant to "{location_query}".
    """
    return prompt_template
