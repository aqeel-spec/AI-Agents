#!/usr/bin/env python3
"""
Direct Tool Testing Script - Test tools individually without agent
"""

import asyncio
import os
from hello import (
    get_weather, search_internet, get_current_time, 
    calculate_math, get_news_headlines, generate_random_number,
    currency_converter, text_analyzer, unit_converter, password_generator
)

async def test_individual_tools():
    """Test tools directly to confirm they work"""
    print("🔧 DIRECT TOOL TESTING")
    print("=" * 60)
    print("Testing tools individually (no agent required)")
    print("=" * 60)

    tests = [
        ("Weather Tool", lambda: get_weather("London")),
        ("Time Tool", lambda: get_current_time()),
        ("Math Tool", lambda: calculate_math("2 + 2 * 3")),
        ("News Tool", lambda: get_news_headlines()),
        ("Random Tool", lambda: generate_random_number(1, 100)),
        ("Currency Tool", lambda: currency_converter(100, "USD", "EUR")),
        ("Text Analysis Tool", lambda: text_analyzer("This is a test sentence for analysis.")),
        ("Unit Converter Tool", lambda: unit_converter(100, "meters", "feet")),
        ("Password Tool", lambda: password_generator(12, True)),
        ("Search Tool", lambda: search_internet("universities in Italy"))
    ]

    successful = 0
    total = len(tests)

    for name, test_func in tests:
        print(f"\n🔍 Testing {name}")
        print("-" * 50)
        
        try:
            result = test_func()
            if result and len(result) > 10:  # Basic success check
                print(f"✅ Success: {result[:150]}...")
                if len(result) > 150:
                    print(f"    (Full result: {len(result)} characters)")
                successful += 1
            else:
                print(f"⚠️ Short result: {result}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    print(f"\n🏁 DIRECT TOOL SUMMARY: {successful}/{total} tools working ({successful/total*100:.1f}%)")
    
    if successful == total:
        print("🏆 Excellent! All tools working directly!")
    elif successful >= total * 0.8:
        print("👍 Good! Most tools working well.")
    else:
        print("⚠️ Some tools need attention.")

    print("\n📋 ENHANCED TOOL FEATURES:")
    print("✅ Weather: City-specific demo data")
    print("✅ Search: Specialized knowledge for common queries")
    print("✅ News: Realistic demo headlines")
    print("✅ All tools: Improved error handling and fallbacks")

if __name__ == "__main__":
    asyncio.run(test_individual_tools())
