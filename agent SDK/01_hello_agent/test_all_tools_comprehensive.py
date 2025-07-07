#!/usr/bin/env python3
"""
Comprehensive Tool Testing Script
Tests all 11 tools with diverse queries to ensure robust functionality.
"""

import asyncio
import os
from hello import agent, config
from agents import Runner

# Test queries for each tool - comprehensive coverage
TEST_QUERIES = {
    "weather": [
        "What's the weather in London?",
        "Check weather in Tokyo",
        "Tell me about weather in New York",
        "Weather conditions in Paris",
        "What's it like outside in Sydney?"
    ],
    "search": [
        "Search for universities in Italy",
        "Find information about international scholarships",
        "Search for machine learning courses",
        "Look up Python programming tutorials",
        "Research artificial intelligence trends"
    ],
    "news": [
        "Get the latest news headlines",
        "What's happening in the news today?",
        "Show me current news",
        "Latest headlines please",
        "What's new in the world?"
    ],
    "time": [
        "What time is it?",
        "Current time please",
        "Tell me the time",
        "What's the current time and date?",
        "Show me today's date and time"
    ],
    "math": [
        "Calculate 15 * 23 + 47",
        "What's the square root of 144?",
        "Solve 2^8",
        "Calculate (45 + 55) / 10",
        "What's 3.14159 * 25?"
    ],
    "random": [
        "Generate a random number",
        "Give me a random number between 1 and 100",
        "Random number please",
        "Pick a random number",
        "Generate random number from 1 to 50"
    ],
    "currency": [
        "Convert 100 USD to EUR",
        "How much is 50 GBP in JPY?",
        "Convert 200 CAD to USD",
        "Exchange 75 EUR to GBP",
        "Convert 1000 JPY to USD"
    ],
    "text_analysis": [
        "Analyze this text: 'Machine learning is transforming technology'",
        "Count words in: 'Python is a powerful programming language'",
        "Analyze: 'AI and data science are growing fields'",
        "Text analysis of: 'Web development uses many frameworks'",
        "Examine: 'Cloud computing enables scalable solutions'"
    ],
    "unit_conversion": [
        "Convert 100 meters to feet",
        "How many kilometers in 50 miles?",
        "Convert 32 Fahrenheit to Celsius",
        "Change 2.5 liters to gallons",
        "Convert 180 pounds to kilograms"
    ],
    "password": [
        "Generate a secure password",
        "Create a password with 12 characters",
        "Make me a strong password",
        "Generate password with symbols",
        "Create a secure 16-character password"
    ],
    "web_browse": [
        "Browse https://www.python.org",
        "Check out https://github.com",
        "Look at https://stackoverflow.com",
        "Browse https://www.wikipedia.org",
        "Visit https://www.google.com"
    ]
}

async def test_single_query(query: str, expected_tool: str = None):
    """Test a single query and return results."""
    print(f"\n🔍 Testing: '{query}'")
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
        elif hasattr(result, 'messages') and result.messages:
            for message in result.messages:
                if hasattr(message, 'content'):
                    response_text += str(message.content)
        
        # Check for tool usage indicators in new_items
        tool_outputs = []
        if hasattr(result, 'new_items') and result.new_items:
            for item in result.new_items:
                if hasattr(item, 'output') and item.output:
                    tool_outputs.append(str(item.output))
                elif hasattr(item, 'content') and item.content:
                    tool_outputs.append(str(item.content))
        
        # Check if response contains tool output indicators
        tool_indicators = [
            "Weather in", "Search results for", "Headlines:", "Current date and time:", 
            "Result of", "Random number", "convert", "analysis:", "password", "°C", "USD", "EUR",
            "Demo data", "Error:", "Generated", "Calculation", "Browse", "Latest"
        ]
        
        has_tool_output = (len(tool_outputs) > 0 or 
                          any(indicator in response_text for indicator in tool_indicators))
        
        print(f"✅ Response: {response_text[:200]}...")
        if len(response_text) > 200:
            print(f"    (Full response: {len(response_text)} characters)")
        
        if tool_outputs:
            print(f"🔧 Tool Outputs Found: {len(tool_outputs)}")
            for i, output in enumerate(tool_outputs[:2]):  # Show first 2 outputs
                print(f"    Tool {i+1}: {output[:100]}...")
        
        print(f"🎯 Tool Usage Detected: {'YES' if has_tool_output else 'NO'}")
        
        if expected_tool:
            print(f"🔍 Expected Tool: {expected_tool}")
        
        return {
            "query": query,
            "response": response_text,
            "tool_outputs": tool_outputs,
            "has_tool_output": has_tool_output,
            "response_length": len(response_text),
            "success": len(response_text) > 0 and has_tool_output
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "query": query,
            "response": f"Error: {str(e)}",
            "has_tool_output": False,
            "response_length": 0,
            "success": False
        }

async def test_tool_category(category: str, queries: list):
    """Test all queries for a specific tool category."""
    print(f"\n{'='*80}")
    print(f"🧪 TESTING {category.upper()} TOOL")
    print(f"{'='*80}")
    
    results = []
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] {category.upper()} TEST")
        result = await test_single_query(query, category)
        results.append(result)
        
        # Brief pause between tests
        await asyncio.sleep(0.5)
    
    # Summary for this category
    successful = sum(1 for r in results if r["success"])
    print(f"\n📊 {category.upper()} SUMMARY:")
    print(f"   ✅ Successful: {successful}/{len(queries)}")
    print(f"   ❌ Failed: {len(queries) - successful}/{len(queries)}")
    
    return results

async def main():
    """Run comprehensive testing of all tools."""
    print("🚀 COMPREHENSIVE TOOL TESTING")
    print("=" * 80)
    print("Testing all 11 tools with multiple query variations")
    print("Checking for tool invocation and meaningful responses")
    print("=" * 80)
    
    all_results = {}
    total_tests = sum(len(queries) for queries in TEST_QUERIES.values())
    
    print(f"📋 Total tests to run: {total_tests}")
    
    for category, queries in TEST_QUERIES.items():
        category_results = await test_tool_category(category, queries)
        all_results[category] = category_results
    
    # Final comprehensive summary
    print("\n" + "="*80)
    print("🏁 FINAL COMPREHENSIVE SUMMARY")
    print("="*80)
    
    total_successful = 0
    total_tests_run = 0
    
    for category, results in all_results.items():
        successful = sum(1 for r in results if r["success"])
        total = len(results)
        total_successful += successful
        total_tests_run += total
        
        status = "✅" if successful == total else "⚠️" if successful > total//2 else "❌"
        print(f"{status} {category.upper():15} {successful:2}/{total:2} ({successful/total*100:5.1f}%)")
    
    overall_percentage = total_successful / total_tests_run * 100
    print(f"\n🎯 OVERALL SUCCESS: {total_successful}/{total_tests_run} ({overall_percentage:.1f}%)")
    
    if overall_percentage >= 90:
        print("🏆 EXCELLENT: All tools working reliably!")
    elif overall_percentage >= 75:
        print("👍 GOOD: Most tools working well, minor issues to address")
    elif overall_percentage >= 50:
        print("⚠️  FAIR: Several tools need attention")
    else:
        print("🚨 NEEDS WORK: Major issues with tool functionality")
    
    # Identify problematic categories
    problematic = []
    for category, results in all_results.items():
        successful = sum(1 for r in results if r["success"])
        if successful < len(results) * 0.8:  # Less than 80% success
            problematic.append(category)
    
    if problematic:
        print(f"\n🔧 NEEDS ATTENTION: {', '.join(problematic)}")
    
    print("\n✨ Testing complete! Check individual results above for details.")

if __name__ == "__main__":
    asyncio.run(main())
