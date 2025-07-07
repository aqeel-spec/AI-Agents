"""
Test the enhanced agent with forced tool usage to ensure it works reliably.
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Import the updated components from hello.py
from hello import agent, config, should_force_tool_usage
from agents import Runner

async def test_enhanced_agent():
    """Test the enhanced agent with various queries"""
    
    test_queries = [
        "What's the weather in London?",
        "What's the latest news?", 
        "What time is it?",
        "Calculate 15 * 8",
        "Search for Python programming tutorials",
        "Generate a random number",
        "Create a strong password",
        "Convert 100 USD to EUR"
    ]
    
    print("Testing Enhanced Agent with Forced Tool Usage")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n🔍 Testing Query: {query}")
        print("-" * 40)
        
        # Test the tool forcing logic
        should_force, tool_name, modified_query = should_force_tool_usage(query)
        print(f"Should force tool: {should_force}")
        if should_force:
            print(f"Tool name: {tool_name}")
            print(f"Modified query: {modified_query}")
        
        try:
            # Use the modified query if forcing tools
            input_query = modified_query if should_force else query
            
            # Run the agent
            result = await Runner.run(
                agent,
                input=[{"role": "user", "content": input_query}],
                run_config=config
            )
            
            # Check results
            tool_calls_count = 0
            tool_outputs = []
            
            for item in result.new_items:
                item_type = type(item).__name__
                if "ToolCall" in item_type:
                    tool_calls_count += 1
                
                # Extract tool outputs
                if hasattr(item, 'output') and item.output:
                    tool_outputs.append(str(item.output))
                elif hasattr(item, 'content') and item.content:
                    tool_outputs.append(str(item.content))
            
            print(f"🔧 Tool calls made: {tool_calls_count}")
            print(f"📄 Tool outputs: {len(tool_outputs)}")
            print(f"📤 Agent response: {result.final_output}")
            
            # Validation
            if tool_calls_count > 0:
                print("✅ Tools were called")
            else:
                print("❌ No tools were called")
            
            if tool_outputs:
                # Check if tool output is reflected in response
                output_reflected = any(
                    output.strip() in result.final_output or
                    any(word in result.final_output.lower() for word in output.lower().split()[:3])
                    for output in tool_outputs
                )
                if output_reflected:
                    print("✅ Tool output is in response")
                else:
                    print("❌ Tool output NOT in response")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_enhanced_agent())
