import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_travel_plan(
    destination: str,
    duration: int,
    budget: str,
    travel_style: str,
    interests: list[str],
    travelers: int,
) -> str:
    """Generate a full travel plan using OpenAI GPT."""
    interests_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = f"""You are an expert travel planner. Create a detailed {duration}-day travel itinerary for {travelers} traveler(s) visiting {destination}.

Travel Details:
- Budget: {budget}
- Travel Style: {travel_style}
- Interests: {interests_str}
- Number of Travelers: {travelers}
- Duration: {duration} days

Please provide:
1. A brief introduction to the destination
2. Day-by-day itinerary with morning, afternoon, and evening activities
3. Recommended accommodations (with budget estimates)
4. Local food and restaurant recommendations
5. Transportation tips
6. Important travel tips and cultural notes
7. Estimated total budget breakdown

Format the response clearly with headers and bullet points."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional travel planner with deep knowledge of destinations worldwide. Provide detailed, practical, and personalized travel plans.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2500,
        temperature=0.7,
    )

    return response.choices[0].message.content


def get_destination_info(destination: str) -> str:
    """Get general information about a destination."""
    prompt = f"""Provide a comprehensive overview of {destination} as a travel destination. Include:

1. Best time to visit
2. Top 10 must-see attractions
3. Local culture and customs
4. Typical weather patterns
5. Safety tips
6. Visa requirements (general)
7. Local currency and payment tips
8. Language basics (if non-English)

Keep the response informative and practical for travelers."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable travel expert. Provide accurate, helpful destination information.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.5,
    )

    return response.choices[0].message.content


def refine_itinerary(original_itinerary: str, feedback: str) -> str:
    """Refine an existing itinerary based on user feedback."""
    prompt = f"""Here is an existing travel itinerary:

{original_itinerary}

The traveler has provided the following feedback/requests for changes:
{feedback}

Please revise the itinerary according to the feedback while keeping the overall structure. Clearly indicate what was changed."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional travel planner. Refine travel plans based on traveler feedback while maintaining quality and practicality.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=2500,
        temperature=0.7,
    )

    return response.choices[0].message.content


def suggest_packing_list(destination: str, duration: int, travel_style: str, season: str) -> str:
    """Generate a personalized packing list."""
    prompt = f"""Create a comprehensive packing list for a {duration}-day trip to {destination} during {season} season.
Travel style: {travel_style}

Include categories:
1. Clothing & Footwear
2. Toiletries & Health
3. Electronics & Gadgets
4. Documents & Money
5. Destination-specific items
6. Optional extras

Keep it practical and specific to the destination and season."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a seasoned traveler. Provide smart, practical packing lists tailored to specific trips.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.6,
    )

    return response.choices[0].message.content
