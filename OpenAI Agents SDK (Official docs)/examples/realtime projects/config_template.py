# Configuration for Future Trading Bot
# Copy this file to config.py and update with your actual values

# OpenAI API Configuration
OPENAI_API_KEY = "your_openai_api_key_here"

# Trading Configuration
TARGET_SYMBOLS = [
    'USD/BRL',
    'USD/CAD', 
    'NZD/CAD',
    'USD/BDT',
    'USD/DZD'
]

# Bot Settings
ANALYSIS_INTERVAL_SECONDS = 300  # 5 minutes
MAX_SIGNALS_PER_SYMBOL = 5
CONFIDENCE_THRESHOLD = 0.6

# Database Configuration
DATABASE_PATH = "trading_bot.db"
LOG_FILE = "trading_bot.log"

# Risk Management
DEFAULT_STOP_LOSS_PERCENT = 2.0  # 2%
DEFAULT_TAKE_PROFIT_PERCENT = 4.0  # 4%

# Market Data Sources (for future implementation)
MARKET_DATA_APIS = {
    'primary': 'https://api.example.com/v1/',
    'backup': 'https://api.backup.com/v1/'
}

# WebSocket Configuration (for real-time data)
WEBSOCKET_ENDPOINTS = {
    'quotex': 'wss://market-qx.pro/ws/',  # Replace with actual endpoint
    'backup': 'wss://backup-feed.com/ws/'
}

# Notification Settings
NOTIFICATIONS = {
    'console': True,
    'file': True,
    'webhook': False,
    'webhook_url': 'https://your-webhook-url.com/notify'
}

# Technical Analysis Settings
TECHNICAL_INDICATORS = {
    'sma_periods': [20, 50, 200],
    'ema_periods': [12, 26],
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9
}
