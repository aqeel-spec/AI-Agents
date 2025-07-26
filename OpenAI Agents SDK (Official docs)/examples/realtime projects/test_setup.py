"""
Test script for Future Trading Bot
Run this to verify your setup before running the main bot
"""

import os
import sys
import asyncio
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import openai
        print("✓ OpenAI imported successfully")
    except ImportError as e:
        print(f"✗ OpenAI import failed: {e}")
        return False
    
    try:
        import pandas as pd
        import numpy as np
        print("✓ Data analysis libraries imported successfully")
    except ImportError as e:
        print(f"✗ Data analysis libraries import failed: {e}")
        return False
    
    try:
        import aiohttp
        import websockets
        print("✓ Async HTTP libraries imported successfully")
    except ImportError as e:
        print(f"✗ Async HTTP libraries import failed: {e}")
        return False
    
    try:
        import sqlite3
        print("✓ SQLite imported successfully")
    except ImportError as e:
        print(f"✗ SQLite import failed: {e}")
        return False
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\nTesting OpenAI connection...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ OpenAI API key not found in environment variables")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API connection successful'"}
            ],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("✓ OpenAI API connection successful")
            return True
        else:
            print("✗ OpenAI API returned empty response")
            return False
            
    except Exception as e:
        print(f"✗ OpenAI API connection failed: {e}")
        return False

def test_database():
    """Test database operations"""
    print("\nTesting database operations...")
    
    try:
        import sqlite3
        
        # Test database creation
        conn = sqlite3.connect(':memory:')  # Use in-memory database for testing
        cursor = conn.cursor()
        
        # Create test table
        cursor.execute('''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value REAL
            )
        ''')
        
        # Insert test data
        cursor.execute('INSERT INTO test_table (name, value) VALUES (?, ?)', ('test', 1.23))
        
        # Query test data
        cursor.execute('SELECT * FROM test_table')
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            print("✓ Database operations successful")
            return True
        else:
            print("✗ Database operations failed")
            return False
            
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_bot_components():
    """Test bot components"""
    print("\nTesting bot components...")
    
    try:
        # Import bot components
        sys.path.append('.')
        from bot import TechnicalAnalyzer, DatabaseManager, MarketData
        
        # Test technical analyzer
        analyzer = TechnicalAnalyzer()
        test_prices = [1.0, 1.1, 1.05, 1.15, 1.2, 1.18, 1.25, 1.22, 1.3, 1.28]
        
        sma = analyzer.calculate_sma(test_prices, 5)
        rsi = analyzer.calculate_rsi(test_prices)
        
        if sma and rsi:
            print("✓ Technical analysis components working")
        else:
            print("✗ Technical analysis components failed")
            return False
        
        # Test database manager
        db_manager = DatabaseManager(':memory:')  # Use in-memory database
        
        # Test market data storage
        test_data = MarketData(
            symbol='USD/BRL',
            price=1.234,
            volume=1000000,
            change_24h=0.5,
            timestamp=datetime.now(),
            high_24h=1.25,
            low_24h=1.22
        )
        
        db_manager.store_market_data(test_data)
        recent_prices = db_manager.get_recent_prices('USD/BRL', 10)
        
        if recent_prices:
            print("✓ Database manager working")
            return True
        else:
            print("✗ Database manager failed")
            return False
            
    except Exception as e:
        print(f"✗ Bot components test failed: {e}")
        return False

async def test_async_operations():
    """Test async operations"""
    print("\nTesting async operations...")
    
    try:
        # Test basic async operation
        await asyncio.sleep(0.1)
        
        # Test aiohttp session
        import aiohttp
        async with aiohttp.ClientSession() as session:
            # Just test session creation, don't make actual request
            pass
        
        print("✓ Async operations working")
        return True
        
    except Exception as e:
        print(f"✗ Async operations test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("Future Trading Bot - System Test")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Run synchronous tests
    if not test_imports():
        all_tests_passed = False
    
    if not test_openai_connection():
        all_tests_passed = False
    
    if not test_database():
        all_tests_passed = False
    
    if not test_bot_components():
        all_tests_passed = False
    
    # Run asynchronous tests
    if not await test_async_operations():
        all_tests_passed = False
    
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✓ All tests passed! Your setup is ready.")
        print("You can now run the bot with: python bot.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("Make sure to install requirements and set up your API key.")
    
    print("=" * 40)

if __name__ == "__main__":
    asyncio.run(main())
