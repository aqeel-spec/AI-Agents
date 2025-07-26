import os
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
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
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

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