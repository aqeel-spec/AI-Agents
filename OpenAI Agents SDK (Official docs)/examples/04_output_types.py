import os
import requests
from agents import (
    Agent,
    function_tool,
    Runner,
    RunConfig
)

from g_config import create_gemini_config, weather_api_key
from pydantic import BaseModel



provider, model = create_gemini_config()

#  return f"Weather in {city}: {temp}°C, {description}, humidity: {humidity}%"

# output models for responses
class WeatherResponse(BaseModel):
    city: str
    temp: str
    description: str
    humidity: str

# Output types
# By default, agents produce plain text (i.e. str) outputs. If you want the agent 
# to produce a particular type of output, you can use the output_type parameter. 
# A common choice is to use Pydantic objects, but we support any type that can be wrapped in a Pydantic TypeAdapter - 
# dataclasses, lists, TypedDict, etc.

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


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that provides weather information.",
    model=model,
    output_type=WeatherResponse,
    tools=[get_weather]  # No tools needed for this example
)


# Create the run configuration
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,  # Disable tracing for this example
)

# Function to run the agent
async def main():
    prompt = input("📝 Enter your prompt (e.g., 'Get user information'): ")
    print(f"💬 Running agent with prompt: {prompt}")
    result = await Runner.run(agent, prompt, run_config=run_config)
    print(f"✅ Agent response: {result.final_output}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())