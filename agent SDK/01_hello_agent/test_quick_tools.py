#!/usr/bin/env python3
"""
Quick Tool Testing Script - Test just a few key tools
"""

import asyncio
import os
from hello import agent, config
from agents import Runner

async def test_single_tool(query: str, tool_name: str):
    """Test a single query and return results."""
    print(f"\n🔍 Testing {tool_name.upper()}: '{query}'")
    print("-" * 60)
    
    try:
        # Run the agent with the query using Runner
        result = await Runner.run(
            agent,
            input=query,
            run_config=config
        )
        
        # Extract the response content from the result
        response_text = ""
        if hasattr(result, 'final_output') and result.final_output:
            response_text = str(result.final_output)
        
        # Check for tool usage in new_items
        tool_outputs = []
        if hasattr(result, 'new_items') and result.new_items:
            for item in result.new_items:
                if hasattr(item, 'output') and item.output:
                    tool_outputs.append(str(item.output))
        
        print(f"✅ Response: {response_text}")
        
        if tool_outputs:
            print(f"🔧 Tool Outputs ({len(tool_outputs)}):")
            for i, output in enumerate(tool_outputs):
                print(f"    {i+1}: {output}")
        
        # Check if it looks like the tool was used
        success = len(tool_outputs) > 0 or len(response_text) > 50
        print(f"🎯 Success: {'YES' if success else 'NO'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

async def main():
    """Run quick testing of key tools."""
    print("🚀 QUICK TOOL TESTING")
    print("=" * 60)
    
    # Test key tools with simple queries
    tests = [
        ("What's the weather in London?", "weather"),
        ("What time is it?", "time"),
        ("Calculate 2 + 2", "math"),
        ("Get latest news", "news"),
        ("Search for Python programming", "search")
    ]
    
    successful = 0
    total = len(tests)
    
    for query, tool_name in tests:
        success = await test_single_tool(query, tool_name)
        if success:
            successful += 1
        await asyncio.sleep(1)  # Brief pause between tests
    
    print(f"\n🏁 SUMMARY: {successful}/{total} tests successful ({successful/total*100:.1f}%)")
    
    if successful == total:
        print("🏆 Excellent! All key tools working!")
    elif successful >= total * 0.8:
        print("👍 Good! Most tools working well.")
    else:
        print("⚠️ Some tools need attention.")

if __name__ == "__main__":
    asyncio.run(main())
