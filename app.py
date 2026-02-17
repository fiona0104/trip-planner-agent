import streamlit as st
import requests
import os
import google.generativeai as genai

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="AI Trip Planner Agent", page_icon="🌍")
st.title("🌍 AI Trip Planner Agent")

st.write("Plan your trip with AI + Real-Time Weather 🌤️")

# -----------------------------------
# LOAD API KEYS FROM STREAMLIT SECRETS
# -----------------------------------
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Missing GOOGLE_API_KEY in Secrets.")
    st.stop()

if not OPENWEATHER_KEY:
    st.error("Missing OPENWEATHER_KEY in Secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Use latest stable free model
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------------
# WEATHER FUNCTION
# -----------------------------------
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
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
    except:
        return "Error fetching weather data."

# -----------------------------------
# USER INPUT
# -----------------------------------
user_input = st.text_input(
    "Enter your request (Example: Plan a 3-day trip to Tokyo in May)"
)

if st.button("Plan Trip"):

    if not user_input:
        st.warning("Please enter a request.")
        st.stop()

    with st.spinner("Generating your trip plan..."):

        # Simple city extraction
        words = user_input.split()
        city = words[-3] if "to" in words else words[-1]

        weather_info = get_weather(city)

        prompt = f"""
You are a professional travel planner AI.

User Request:
{user_input}

Provide:

1. One paragraph about the city's cultural & historical significance.
2. Suggested travel dates.
3. 3-Day detailed itinerary.
4. Example flight option.
5. Example hotel recommendation.
6. Include this real-time weather information:

{weather_info}
"""

        try:
            response = model.generate_content(prompt)
            st.success("Trip Plan Generated Successfully!")
            st.write(response.text)

        except Exception as e:
            st.error("Error generating response. Check API keys or model access.")
