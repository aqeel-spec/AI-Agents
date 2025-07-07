"""
Test the API fallback system
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from hello import (
    create_gemini_config, create_openai_config, 
    current_provider_type, agent, run_with_fallback
)
from agents import RunConfig

async def test_fallback_system():
    """Test the API fallback functionality"""
    
    print("Testing API Fallback System")
    print("=" * 40)
    
    # Check available providers
    gemini_provider, gemini_model = create_gemini_config()
    openai_provider, openai_model = create_openai_config()
    
    print(f"Gemini available: {gemini_provider is not None}")
    print(f"OpenAI available: {openai_provider is not None}")
    print(f"Current provider: {current_provider_type}")
    
    if not openai_provider:
        print("\n❌ OpenAI API key not found!")
        print("Please add OPENAI_API_KEY to your .env file to test fallback.")
        return
    
    # Test a simple query that should work
    test_query = "What time is it?"
    history = [{"role": "user", "content": "Use get_current_time tool for: " + test_query}]
    
    try:
        # Create initial config
        if gemini_provider and gemini_model:
            config = RunConfig(
                model=gemini_model,
                model_provider=gemini_provider,
                tracing_disabled=True
            )
        else:
            config = RunConfig(
                model=openai_model,
                model_provider=openai_provider,
                tracing_disabled=True
            )
        
        print(f"\nTesting query: {test_query}")
        
        # Test the fallback system
        result, used_provider = await run_with_fallback(agent, history, config)
        
        print(f"✅ Success!")
        print(f"Used provider: {used_provider}")
        print(f"Response: {result.final_output}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_fallback_system())
