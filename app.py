import streamlit as st
import requests
import os
import google.generativeai as genai

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(page_title="AI Trip Planner", page_icon="🌍")
st.title("🌍 AI Trip Planner Agent")

# ------------------------
# LOAD API KEYS
# ------------------------
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Missing GOOGLE_API_KEY in Secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ------------------------
# WEATHER FUNCTION
# ------------------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "main" in data:
        return f"""
Current Weather in {city}:
Temperature: {data['main']['temp']}°C
Condition: {data['weather'][0]['description']}
Humidity: {data['main']['humidity']}%
"""
    else:
        return "Weather data not found."

# ------------------------
# USER INPUT
# ------------------------
user_input = st.text_input(
    "Enter your request (Example: Plan a 3-day trip to Tokyo in May)"
)

if st.button("Plan Trip"):
    if user_input:
        with st.spinner("Planning your trip..."):

            # Extract city name (simple logic)
            words = user_input.split()
            city = words[-3] if "to" in words else words[-1]

            weather_info = get_weather(city)

            prompt = f"""
You are a travel planner.

User Request:
{user_input}

Include:
1. 1 paragraph about cultural & historical significance
2. Travel dates suggestion
3. 3-day itinerary
4. Flight suggestion (example)
5. Hotel suggestion (example)
6. Include this real weather info:

{weather_info}
"""

            response = model.generate_content(prompt)

            st.success("Trip Plan Generated!")
            st.write(response.text)

    else:
        st.warning("Please enter a trip request.")
