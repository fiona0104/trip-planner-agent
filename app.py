import streamlit as st
import requests
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool

# -------------------------------
# SET PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Trip Planner", page_icon="🌍")
st.title("🌍 AI Trip Planner Agent")
st.write("Plan your trip with real-time weather + AI itinerary")

# -------------------------------
# LOAD API KEYS FROM SECRETS
# -------------------------------
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Missing GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# -------------------------------
# WEATHER TOOL FUNCTION
# -------------------------------
def get_weather(city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if "main" in data:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]

            return f"""
            Current Weather in {city}:
            Temperature: {temp}°C
            Condition: {desc}
            Humidity: {humidity}%
            """
        else:
            return "Weather data not found."
    except:
        return "Error fetching weather data."


# -------------------------------
# INITIALIZE LLM
# -------------------------------
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7
)

# -------------------------------
# DEFINE TOOLS
# -------------------------------
tools = [
    Tool(
        name="Weather Tool",
        func=get_weather,
        description="Use this tool to get current weather information of a city."
    )
]

# -------------------------------
# CREATE AGENT
# -------------------------------
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# -------------------------------
# USER INPUT
# -------------------------------
user_input = st.text_input(
    "Enter your request (Example: Plan a 3-day trip to Tokyo in May)"
)

# -------------------------------
# RUN AGENT
# -------------------------------
if st.button("Plan Trip"):
    if user_input:
        with st.spinner("Planning your trip..."):
            try:
                result = agent.run(user_input)
                st.success("Trip Plan Generated Successfully!")
                st.write(result)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a trip request.")

