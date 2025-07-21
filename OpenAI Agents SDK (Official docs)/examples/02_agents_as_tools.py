import os
import requests
from agents import (
    Agent,
    Runner,
    function_tool,
    RunConfig
)

from g_config import create_gemini_config, weather_api_key


"""
This example shows the agents-as-tools pattern. The frontline agent receives a user message and
then picks which agents to call, as tools. In this case, it picks from a set of translation
agents.
"""

provider, model = create_gemini_config()

@function_tool
def get_weather(city: str) -> str:
    """Get current weather information for a specific city."""
    try:
        # Using OpenWeatherMap API (you'll need to get a free API key)
        api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        
        if api_key == "demo_key":
            # Enhanced demo response with more realistic data based on city
            city_lower = city.lower()
            if "london" in city_lower:
                return f"Weather in {city}: 15°C, overcast with light rain expected. Humidity: 78%. Wind: 12 km/h SW. (Demo data - add OPENWEATHER_API_KEY for real-time weather)"
            elif "tokyo" in city_lower:
                return f"Weather in {city}: 24°C, partly cloudy with occasional sunshine. Humidity: 65%. Wind: 8 km/h E. (Demo data - add OPENWEATHER_API_KEY for real-time weather)"
            elif "new york" in city_lower or "nyc" in city_lower:
                return f"Weather in {city}: 18°C, clear skies with good visibility. Humidity: 55%. Wind: 15 km/h NW. (Demo data - add OPENWEATHER_API_KEY for real-time weather)"
            elif "paris" in city_lower:
                return f"Weather in {city}: 16°C, light clouds with mild breeze. Humidity: 72%. Wind: 10 km/h W. (Demo data - add OPENWEATHER_API_KEY for real-time weather)"
            elif "sydney" in city_lower:
                return f"Weather in {city}: 22°C, sunny with scattered clouds. Humidity: 60%. Wind: 14 km/h SE. (Demo data - add OPENWEATHER_API_KEY for real-time weather)"
            else:
                return f"Weather in {city}: 20°C, partly cloudy with moderate conditions. Humidity: 65%. Wind: 12 km/h. (Demo data - add OPENWEATHER_API_KEY for real-time weather)\n\nNote: For detailed 20-hour forecasts, hourly data, and extended predictions, please use dedicated weather services like Weather.com or AccuWeather.com"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"Weather in {city}: {temp}°C, {description}, humidity: {humidity}%"
        else:
            return f"Could not fetch weather data for {city}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,  # Disable tracing for this example
)
    
agent = Agent(
    name="Weather Agent",
    model=model,
    tools=[get_weather]
)

# Function to run the agent
async def main():
    try:
        prompt = input("📝 Enter your prompt (e.g., 'What's the weather in Paris?'): ")
    except EOFError:
        prompt = "What's the weather like in London today?"
        print("📝 Using default prompt for non-interactive environment")
    
    print(f"💬 Running agent with prompt: {prompt}")
    result = await Runner.run(agent, prompt, run_config=run_config)
    print(f"\n✅ Agent response: \t {result.final_output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
