# Future Trading Bot - Live Signal Generator

A sophisticated trading bot that provides live trading signals using OpenAI Agents SDK and web search capabilities for the https://market-qx.pro/en/trade/ platform.

## Features

🤖 **AI-Powered Analysis**: Uses OpenAI GPT-4 for market sentiment analysis and signal generation
📊 **Technical Analysis**: Implements multiple technical indicators (SMA, EMA, RSI, MACD)
🔍 **Web Search Integration**: Real-time market news and sentiment analysis
💾 **Data Storage**: SQLite database for storing signals and market data
📈 **Live Monitoring**: Real-time monitoring of multiple currency pairs
🎯 **Risk Management**: Automatic stop-loss and take-profit calculations

## Supported Trading Pairs

- USD/BRL (US Dollar / Brazilian Real)
- USD/CAD (US Dollar / Canadian Dollar)
- NZD/CAD (New Zealand Dollar / Canadian Dollar)
- USD/BDT (US Dollar / Bangladeshi Taka)
- USD/DZD (US Dollar / Algerian Dinar)

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection for web search capabilities

### Quick Setup

1. **Clone or download the project files**

2. **Run the setup script**:
   ```bash
   python setup.py
   ```

3. **Set your OpenAI API key**:
   
   **Option 1: Environment Variable (Recommended)**
   ```bash
   set OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **Option 2: Configuration File**
   - Edit `config.py` and update the `OPENAI_API_KEY` value

4. **Run the bot**:
   ```bash
   python bot.py
   ```

### Manual Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create configuration file**:
   ```bash
   copy config_template.py config.py
   ```

3. **Update configuration** with your API key and settings

## Configuration

Edit `config.py` to customize the bot behavior:

```python
# OpenAI API Configuration
OPENAI_API_KEY = "your_openai_api_key_here"

# Trading Configuration
TARGET_SYMBOLS = ['USD/BRL', 'USD/CAD', 'NZD/CAD', 'USD/BDT', 'USD/DZD']
ANALYSIS_INTERVAL_SECONDS = 300  # 5 minutes
CONFIDENCE_THRESHOLD = 0.6

# Risk Management
DEFAULT_STOP_LOSS_PERCENT = 2.0  # 2%
DEFAULT_TAKE_PROFIT_PERCENT = 4.0  # 4%
```

## Usage

### Basic Usage

```bash
python bot.py
```

The bot will:
1. Start monitoring the configured trading pairs
2. Generate signals every 5 minutes (configurable)
3. Display live signals in the console
4. Store all signals and market data in the database

### Understanding Signals

Each signal includes:
- **Symbol**: Trading pair (e.g., USD/BRL)
- **Signal Type**: BUY, SELL, or HOLD
- **Confidence**: Percentage confidence (0-100%)
- **Entry Price**: Recommended entry price
- **Stop Loss**: Risk management stop-loss level
- **Take Profit**: Target profit level
- **Reasoning**: AI explanation for the signal

### Example Output

```
================================================================================
LIVE TRADING SIGNALS
================================================================================

Symbol: USD/BRL
Signal: BUY
Confidence: 75.00%
Entry Price: 0.169000
Stop Loss: 0.165620
Take Profit: 0.175760
Time: 2025-07-24 10:30:00
Reasoning: Bullish technical indicators and positive sentiment. Technical score: 2, Sentiment: 0.3
--------------------------------------------------------------------
```

## Components

### 1. WebSearchAgent
- Searches for market news and analysis
- Uses OpenAI for sentiment analysis
- Provides fundamental analysis input

### 2. TechnicalAnalyzer
- Calculates technical indicators:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - MACD (Moving Average Convergence Divergence)

### 3. DatabaseManager
- Stores trading signals
- Manages market data history
- SQLite database for persistence

### 4. FutureTradingBot
- Main bot orchestrator
- Combines technical and fundamental analysis
- Generates and displays signals

## Database Schema

### Signals Table
- `id`: Unique identifier
- `symbol`: Trading pair
- `signal_type`: BUY/SELL/HOLD
- `confidence`: Signal confidence (0-1)
- `entry_price`: Entry price
- `stop_loss`: Stop loss level
- `take_profit`: Take profit level
- `timestamp`: Signal generation time
- `reasoning`: AI explanation
- `timeframe`: Analysis timeframe

### Market Data Table
- `id`: Unique identifier
- `symbol`: Trading pair
- `price`: Current price
- `volume`: Trading volume
- `change_24h`: 24-hour change percentage
- `high_24h`: 24-hour high
- `low_24h`: 24-hour low
- `timestamp`: Data timestamp

## Customization

### Adding New Trading Pairs

Edit `config.py`:
```python
TARGET_SYMBOLS = [
    'USD/BRL',
    'USD/CAD',
    'EUR/USD',  # Add new pairs here
    'GBP/USD'
]
```

### Adjusting Analysis Frequency

```python
ANALYSIS_INTERVAL_SECONDS = 180  # 3 minutes instead of 5
```

### Risk Management Settings

```python
DEFAULT_STOP_LOSS_PERCENT = 1.5   # Tighter stop loss
DEFAULT_TAKE_PROFIT_PERCENT = 3.0  # Conservative take profit
```

## API Integration

Currently uses simulated market data. To integrate with real APIs:

1. **Replace the `fetch_real_time_data` method** in `FutureTradingBot`
2. **Add authentication** for your chosen data provider
3. **Update WebSocket connections** for real-time feeds

### Supported Data Sources (Future)
- Quotex API (when available)
- Alpha Vantage
- Yahoo Finance
- IEX Cloud
- Twelve Data

## Logging

The bot creates two log files:
- `trading_bot.log`: Detailed bot operations
- Console output: Real-time signal display

Log levels:
- INFO: General operations
- WARNING: Minor issues
- ERROR: Serious problems

## Risk Disclaimer

⚠️ **IMPORTANT**: This bot is for educational purposes only. 

- **Past performance does not guarantee future results**
- **Trading involves significant risk of loss**
- **Only trade with money you can afford to lose**
- **Always verify signals with your own analysis**
- **Consider consulting with a financial advisor**

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set
   - Check your OpenAI account has sufficient credits

2. **Module Import Errors**
   - Run `pip install -r requirements.txt`
   - Ensure you're using Python 3.8+

3. **Database Errors**
   - Delete `trading_bot.db` to reset the database
   - Check file permissions

4. **No Signals Generated**
   - Check internet connection for web search
   - Verify API key is working
   - Check log files for errors

### Support

For issues and questions:
1. Check the log files for error details
2. Verify all dependencies are installed
3. Ensure configuration is correct
4. Review the troubleshooting section

## Future Enhancements

- [ ] Real-time WebSocket data feeds
- [ ] Advanced portfolio management
- [ ] Multiple timeframe analysis
- [ ] Backtesting capabilities
- [ ] Email/SMS notifications
- [ ] Web dashboard interface
- [ ] Machine learning model integration
- [ ] Risk-adjusted position sizing

## License

This project is for educational purposes. Please comply with all applicable trading regulations and platform terms of service.

---

*Happy Trading! 📈*
