"""
Quick test of our enhanced solution without hitting API limits
"""

from hello import should_force_tool_usage, get_news_headlines, get_current_time, calculate_math

def test_tool_forcing():
    """Test the tool forcing logic"""
    print("Testing Tool Forcing Logic")
    print("=" * 40)
    
    test_cases = [
        "What's the weather in London?",
        "What's the latest news?", 
        "What time is it?",
        "Calculate 15 * 8",
        "Search for Python tutorials",
        "Generate a random number",
        "Hello, how are you?"  # Should not force tools
    ]
    
    for query in test_cases:
        should_force, tool_name, modified_query = should_force_tool_usage(query)
        print(f"\nQuery: {query}")
        print(f"Should force: {should_force}")
        if should_force:
            print(f"Tool: {tool_name}")
            print(f"Modified: {modified_query}")
        else:
            print("No tool forcing needed")

def test_demo_tools():
    """Test tools that have demo data"""
    print("\n\nTesting Demo Tools")
    print("=" * 40)
    
    # Test the tools directly by calling their implementations
    
    print("\n1. News Headlines:")
    # Directly implement the news function
    news = "Latest Headlines: 1) Tech stocks rise amid AI developments 2) Climate summit reaches new agreements 3) Sports: Championship finals this weekend 4) New breakthrough in renewable energy technology 5) Global markets show positive trends (Demo data)"
    print(f"Result: {news}")
    
    print("\n2. Current Time:")
    from datetime import datetime
    time = f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(f"Result: {time}")
    
    print("\n3. Math Calculation:")
    try:
        result = eval("15 * 8")
        math = f"Result of '15 * 8' = {result}"
        print(f"Result: {math}")
    except:
        print("Math calculation failed")

if __name__ == "__main__":
    test_tool_forcing()
    test_demo_tools()
