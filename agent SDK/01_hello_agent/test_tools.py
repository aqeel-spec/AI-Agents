import os
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    """Get current weather information for a specific city."""
    return f"Weather in {city}: 22°C, partly cloudy with light winds. (Demo data)"

@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    now = datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

# Setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Test agent
agent = Agent(
    instructions="You are a helpful assistant. When users ask for weather, use get_weather tool. When users ask for time, use get_current_time tool. Always use the appropriate tool when available.",
    name="Test Agent",
    tools=[get_weather, get_current_time]
)

# Test
async def test():
    result = await Runner.run(
        agent,
        input="What's the weather in London?",
        run_config=config
    )
    print("Final output:", result.final_output)
    print("New items:", len(result.new_items))
    for item in result.new_items:
        print(f"Item type: {type(item).__name__}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
