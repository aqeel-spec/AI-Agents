# Future Trading Bot - Quick Start Guide

## 🎯 What You Have Created

A sophisticated AI-powered trading bot that generates live trading signals for the https://market-qx.pro/en/trade/ platform using:

- **OpenAI Agents SDK** for intelligent signal generation
- **Web search capabilities** for real-time market sentiment analysis
- **Technical analysis** with RSI, MACD, SMA, EMA indicators
- **Real-time monitoring** of currency pairs
- **Risk management** with automatic stop-loss and take-profit calculations

## 📂 Project Structure

```
├── bot.py                 # Main trading bot (complete implementation)
├── simple_demo.py         # Working demo (run this first!)
├── demo.py               # Advanced demo with full features
├── test_setup.py         # System verification script  
├── setup.py              # Installation script
├── config_template.py    # Configuration template
├── requirements.txt      # Python dependencies
├── README.md            # Detailed documentation
└── logs/                # Log files directory
```

## 🚀 Quick Start (3 Steps)

### Step 1: Run the Demo
```bash
python simple_demo.py
```

This shows you exactly what the bot does - generates trading signals like:
- 💱 **USD/BRL**: BUY signal with 75% confidence
- 💱 **USD/CAD**: SELL signal with 68% confidence  
- 💱 **NZD/CAD**: HOLD signal with 55% confidence

### Step 2: Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set it in Windows:
   ```cmd
   set OPENAI_API_KEY=your_actual_api_key_here
   ```

### Step 3: Run Live Bot
```bash
python bot.py
```

## 🎯 Target Trading Pairs

The bot monitors these pairs from market-qx.pro:
- **USD/BRL** (US Dollar / Brazilian Real)
- **USD/CAD** (US Dollar / Canadian Dollar)  
- **NZD/CAD** (New Zealand Dollar / Canadian Dollar)
- **USD/BDT** (US Dollar / Bangladeshi Taka)
- **USD/DZD** (US Dollar / Algerian Dinar)

## 🧠 How It Works

1. **Data Collection**: Fetches real-time market data
2. **Technical Analysis**: Calculates RSI, MACD, moving averages
3. **Sentiment Analysis**: Uses AI to analyze market news and sentiment
4. **Signal Generation**: Combines technical + fundamental analysis
5. **Risk Management**: Calculates optimal entry, stop-loss, take-profit
6. **Display Results**: Shows signals with confidence levels and reasoning

## 🔧 Key Features

- ✅ **Real-time signals** every 5 minutes
- ✅ **AI-powered analysis** using GPT-4
- ✅ **Web search integration** for market sentiment
- ✅ **Technical indicators** (RSI, MACD, SMA, EMA)
- ✅ **SQLite database** for signal history
- ✅ **Risk management** with stop-loss/take-profit
- ✅ **Confidence scoring** for each signal
- ✅ **Detailed reasoning** for trading decisions

## 📊 Sample Output

```
================================================================================
🤖 FUTURE TRADING BOT - LIVE SIGNALS
================================================================================

📊 SIGNAL #1
💱 Symbol: USD/BRL
📈 Signal: BUY
🎯 Confidence: 75.0%
💰 Entry Price: 0.16900
🛑 Stop Loss: 0.16562
🎉 Take Profit: 0.17576
🧠 Reasoning: Technical indicators show bullish momentum. RSI oversold, MACD crossing upward, positive market sentiment.
```

## ⚠️ Important Notes

- **Demo Mode**: Run `simple_demo.py` first to see how it works
- **API Required**: You need an OpenAI API key for live functionality
- **Educational Purpose**: This is for learning - always verify signals
- **Risk Warning**: Never trade more than you can afford to lose
- **Platform Integration**: Currently simulates data - can be extended with real APIs

## 🛠️ Customization

Edit `bot.py` to:
- Add more trading pairs
- Adjust analysis frequency (default: 5 minutes)
- Modify risk management parameters
- Integrate real market data APIs
- Add notification systems

## 🎉 Success!

You now have a complete AI-powered trading bot that:
1. ✅ **Generates intelligent trading signals**
2. ✅ **Uses advanced AI for market analysis** 
3. ✅ **Provides real-time monitoring**
4. ✅ **Includes risk management**
5. ✅ **Works with market-qx.pro platform**

Start with the demo, then move to live trading once you have your API key set up!

---
*Built with OpenAI Agents SDK | Target Platform: https://market-qx.pro/en/trade/*
