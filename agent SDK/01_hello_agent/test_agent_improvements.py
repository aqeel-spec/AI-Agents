"""
Test script to verify that the agent properly uses tool outputs in responses.
This tests the same scenarios that were problematic before.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents import (
    Agent, 
    Runner, 
    RunConfig,
    AsyncOpenAI,
    OpenAIChatCompletionsModel, 
    function_tool
)

# Import all tools from hello.py
from hello import (
    get_weather, search_internet, web_browse, get_current_time, 
    calculate_math, generate_random_number, get_news_headlines, 
    currency_converter, text_analyzer, unit_converter, password_generator
)

# Setup (same as hello.py)
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
)

# Create agent with same configuration as hello.py
agent = Agent(
    instructions="""You are a helpful assistant with access to tools. 

**MANDATORY TOOL USAGE RULES:**
1. ALWAYS use tools when available for a request
2. NEVER provide generic responses when a tool has been called
3. ALWAYS include the EXACT tool output in your response
4. Start your response with the tool result, then add context if needed

**Tool Response Format:**
- Weather queries: Use get_weather(city) → "Weather in [city]: [exact tool output]"
- News queries: Use get_news_headlines() → "Latest news: [exact tool output]" 
- Time queries: Use get_current_time() → "Current time: [exact tool output]"
- Math queries: Use calculate_math(expression) → "Result: [exact tool output]"
- Search queries: Use search_internet(query) → "Search results: [exact tool output]"

**Examples of CORRECT responses:**
- User: "What's the weather in London?"
  Tool returns: "Weather in London: 22°C, partly cloudy"
  Response: "Weather in London: 22°C, partly cloudy"

- User: "What's the latest news?"
  Tool returns: "Demo news headlines..."
  Response: "Latest news: Demo news headlines..."

**NEVER say:**
- "I was unable to..."
- "I don't have access to..."
- "Let me help you with that..." (without tool output)

**ALWAYS include tool output first in your response.**""",
    name="Test Agent",
    tools=[
        get_weather,
        search_internet,
        web_browse,
        get_current_time,
        calculate_math,
        generate_random_number,
        get_news_headlines,
        currency_converter,
        text_analyzer,
        unit_converter,
        password_generator
    ]
)

async def test_scenarios():
    """Test various scenarios that should trigger tool usage"""
    
    test_cases = [
        ("What's the weather in London?", "get_weather"),
        ("What's the latest news?", "get_news_headlines"),
        ("What time is it?", "get_current_time"),
        ("Calculate 25 * 4", "calculate_math"),
        ("Search for Python tutorials", "search_internet"),
        ("Convert 100 USD to EUR", "currency_converter"),
    ]
    
    print("Testing agent with tool calling scenarios...")
    print("=" * 60)
    
    for query, expected_tool in test_cases:
        print(f"\n🔍 Testing: {query}")
        print(f"Expected tool: {expected_tool}")
        print("-" * 40)
        
        try:
            # Run the agent
            result = await Runner.run(
                agent,
                input=[{"role": "user", "content": query}],
                run_config=config
            )
            
            # Check if tools were used
            tool_outputs = []
            tool_used = False
            
            for item in result.new_items:
                item_type = type(item).__name__
                print(f"Item type: {item_type}")
                
                if "ToolCall" in item_type:
                    tool_used = True
                
                if hasattr(item, 'output') and item.output:
                    tool_outputs.append(str(item.output))
                    print(f"Tool output: {item.output}")
                elif hasattr(item, 'content') and item.content:
                    tool_outputs.append(str(item.content))
                    print(f"Tool content: {item.content}")
            
            print(f"\n📤 Agent Response: {result.final_output}")
            
            # Validation
            if tool_used:
                print("✅ Tool was called")
            else:
                print("❌ No tool was called")
            
            if tool_outputs:
                print(f"✅ Tool outputs detected: {len(tool_outputs)}")
                
                # Check if tool output is in the response
                output_in_response = any(
                    output.strip() in result.final_output or 
                    any(word in result.final_output.lower() for word in output.lower().split()[:5])
                    for output in tool_outputs
                )
                
                if output_in_response:
                    print("✅ Tool output is included in response")
                else:
                    print("❌ Tool output NOT included in response")
                    print(f"Tool outputs: {tool_outputs}")
            else:
                print("❌ No tool outputs detected")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_scenarios())
