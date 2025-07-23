import os
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig
)
from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file
load_dotenv(find_dotenv())

# Step 1: Load environment variables
# Step 2: Check if the required API keys are set
# Step 3: Create configurations for Gemini and OpenAI models
# Step 4: Runner configuration with the selected model and provider
# Step 5: Tools to interact with the models

# 1. Get API keys
open_ai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# 2. Conditional check for API keys
if not open_ai_api_key or not gemini_api_key:
    raise ValueError("Please set the OPENAI_API_KEY and GEMINI_API_KEY environment variables.")

# Step 3: Create Gemini and OpenAI configurations
def create_gemini_config():
    """Create Gemini configuration"""
    if not gemini_api_key:
        return None, None
    
    provider = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash-exp",
        openai_client=provider
    )
    
    print(f"Using Gemini model: *** {model.model} ***")
    
    return provider, model

def create_openai_config():
    """Create OpenAI configuration"""
    if not open_ai_api_key:
        return None, None
    
    provider = AsyncOpenAI(api_key=open_ai_api_key)
    model = OpenAIChatCompletionsModel(
        model="gpt-4o-mini",  # Use a cost-effective OpenAI model
        openai_client=provider
    )
    print(f"Using OpenAI model: *** {model.model} ***")
    return provider, model

# Prompt user to select a model
print("🤖 Choose a model:")
print("1. Gemini")
print("2. OpenAI")
model_choice = input("Enter the number of your choice: ")

# Create configuration based on user choice
if model_choice == "1":
    provider, model = create_gemini_config()
elif model_choice == "2":
    provider, model = create_openai_config()
else:
    print("❌ Invalid choice. Defaulting to Gemini.")
    provider, model = create_gemini_config()

# Step 4: Config
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,  # Disable tracing for this example
)

# Initialize the agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

# Function to run the agent
async def main():
    prompt = input("📝 Enter your prompt: ")
    print(f"💬 Running agent with prompt: {prompt}")
    result = await Runner.run(agent, prompt, run_config=run_config)
    print(f"\n✅ Agent response: \t {result.final_output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
