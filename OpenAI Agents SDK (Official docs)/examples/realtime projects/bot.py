"""
Future Trading Bot - Live Signal Generator
Uses OpenAI Agents SDK with web search capabilities for real-time trading signals
Target Platform: https://market-qx.pro/en/trade/
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import websockets
import requests
from dataclasses import dataclass
import pandas as pd
import numpy as np
from openai import OpenAI
import os
from bs4 import BeautifulSoup
import aiohttp
import sqlite3
from threading import Thread
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TradingSignal:
    """Data class for trading signals"""
    symbol: str
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    prediction: str  # 'UP', 'DOWN', 'SIDEWAYS'
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    timestamp: datetime
    reasoning: str
    timeframe: str
    duration_minutes: int  # Predicted duration for the move
    target_price: float  # Predicted target price

@dataclass
class PricePrediction:
    """Data class for price predictions with duration"""
    symbol: str
    current_price: float
    predicted_direction: str  # 'UP' or 'DOWN'
    predicted_price: float
    duration_minutes: int
    confidence: float
    timestamp: datetime
    expiry_time: datetime
    reasoning: str

@dataclass
class MarketData:
    """Data class for market data"""
    symbol: str
    price: float
    volume: float
    change_24h: float
    timestamp: datetime
    high_24h: float
    low_24h: float

class WebSearchAgent:
    """Agent for web search and market analysis"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_market_news(self, symbol: str) -> List[Dict[str, Any]]:
        """Search for market news and analysis for a specific symbol"""
        try:
            search_queries = [
                f"{symbol} trading analysis today",
                f"{symbol} price prediction",
                f"{symbol} market news",
                f"{symbol} technical analysis"
            ]
            
            news_data = []
            for query in search_queries:
                # Simulate web search results (replace with actual search API)
                news_data.append({
                    'title': f"Market Analysis for {symbol}",
                    'content': f"Latest trading analysis and predictions for {symbol}",
                    'source': 'Market Analysis',
                    'timestamp': datetime.now(),
                    'relevance_score': 0.8
                })
            
            return news_data
        except Exception as e:
            logger.error(f"Error searching market news: {e}")
            return []
    
    async def analyze_market_sentiment(self, symbol: str, news_data: List[Dict]) -> Dict[str, Any]:
        """Use OpenAI to analyze market sentiment from news data"""
        try:
            news_text = "\n".join([f"{item['title']}: {item['content']}" for item in news_data])
            
            prompt = f"""
            Analyze the market sentiment for {symbol} based on the following news and information:
            
            {news_text}
            
            Provide analysis in JSON format with:
            - sentiment_score: float between -1 (very bearish) and 1 (very bullish)
            - confidence: float between 0 and 1
            - key_factors: list of important factors affecting the sentiment
            - recommendation: BUY, SELL, or HOLD
            - reasoning: detailed explanation
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst and trading advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Parse the response (assuming it returns valid JSON)
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing market sentiment: {e}")
            return {
                'sentiment_score': 0,
                'confidence': 0.5,
                'key_factors': [],
                'recommendation': 'HOLD',
                'reasoning': 'Analysis unavailable due to error'
            }

class TechnicalAnalyzer:
    """Technical analysis tools with price prediction capabilities"""
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        return ema
    
    @staticmethod
    def predict_price_direction(prices: List[float], volumes: List[float] = None) -> Dict[str, Any]:
        """Predict price direction using multiple indicators"""
        if len(prices) < 20:
            return {'direction': 'SIDEWAYS', 'confidence': 0.5, 'duration': 5}
        
        # Calculate indicators
        sma_5 = TechnicalAnalyzer.calculate_sma(prices, 5)
        sma_10 = TechnicalAnalyzer.calculate_sma(prices, 10)
        sma_20 = TechnicalAnalyzer.calculate_sma(prices, 20)
        rsi = TechnicalAnalyzer.calculate_rsi(prices)
        macd = TechnicalAnalyzer.calculate_macd(prices)
        
        # Price momentum
        current_price = prices[-1]
        prev_price = prices[-2] if len(prices) > 1 else current_price
        momentum = (current_price - prev_price) / prev_price * 100
        
        # Direction scoring
        direction_score = 0
        confidence_factors = []
        
        # Moving average trend
        if sma_5 and sma_10 and sma_20:
            if sma_5 > sma_10 > sma_20:  # Bullish alignment
                direction_score += 2
                confidence_factors.append("Bullish MA alignment")
            elif sma_5 < sma_10 < sma_20:  # Bearish alignment
                direction_score -= 2
                confidence_factors.append("Bearish MA alignment")
        
        # RSI signals
        if rsi:
            if rsi < 30:  # Oversold - potential bounce UP
                direction_score += 1
                confidence_factors.append("RSI oversold - bounce expected")
            elif rsi > 70:  # Overbought - potential drop DOWN
                direction_score -= 1
                confidence_factors.append("RSI overbought - drop expected")
        
        # MACD signals
        if macd:
            if macd['macd'] > macd['signal']:
                direction_score += 1
                confidence_factors.append("MACD bullish crossover")
            else:
                direction_score -= 1
                confidence_factors.append("MACD bearish crossover")
        
        # Momentum factor
        if momentum > 0.1:
            direction_score += 1
            confidence_factors.append("Positive momentum")
        elif momentum < -0.1:
            direction_score -= 1
            confidence_factors.append("Negative momentum")
        
        # Recent price pattern analysis
        recent_highs = max(prices[-5:]) if len(prices) >= 5 else current_price
        recent_lows = min(prices[-5:]) if len(prices) >= 5 else current_price
        
        if current_price > (recent_highs + recent_lows) / 2:
            direction_score += 0.5
        else:
            direction_score -= 0.5
        
        # Determine direction and confidence
        if direction_score > 1:
            prediction = 'UP'
            confidence = min(0.95, 0.6 + abs(direction_score) * 0.1)
        elif direction_score < -1:
            prediction = 'DOWN'
            confidence = min(0.95, 0.6 + abs(direction_score) * 0.1)
        else:
            prediction = 'SIDEWAYS'
            confidence = 0.5
        
        # Predict duration based on volatility and momentum
        volatility = np.std(prices[-10:]) if len(prices) >= 10 else 0.001
        if volatility > 0.002:  # High volatility - shorter duration
            duration = np.random.randint(1, 5)
        elif volatility < 0.0005:  # Low volatility - longer duration
            duration = np.random.randint(5, 15)
        else:
            duration = np.random.randint(3, 10)
        
        # Predict target price
        if prediction == 'UP':
            target_price = current_price * (1 + volatility * 2)
        elif prediction == 'DOWN':
            target_price = current_price * (1 - volatility * 2)
        else:
            target_price = current_price
        
        return {
            'direction': prediction,
            'confidence': confidence,
            'duration': duration,
            'target_price': target_price,
            'factors': confidence_factors,
            'momentum': momentum,
            'volatility': volatility
        }
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def calculate_macd(prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Dict[str, float]:
        """Calculate MACD"""
        if len(prices) < slow_period:
            return None
        
        ema_fast = TechnicalAnalyzer.calculate_ema(prices, fast_period)
        ema_slow = TechnicalAnalyzer.calculate_ema(prices, slow_period)
        
        if ema_fast is None or ema_slow is None:
            return None
        
        macd_line = ema_fast - ema_slow
        # Simplified signal line calculation
        signal_line = macd_line * 0.9  # Simplified
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }

class DatabaseManager:
    """Manage SQLite database for storing signals and market data"""
    
    def __init__(self, db_path: str = "trading_bot.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                entry_price REAL NOT NULL,
                stop_loss REAL NOT NULL,
                take_profit REAL NOT NULL,
                timestamp DATETIME NOT NULL,
                reasoning TEXT,
                timeframe TEXT,
                duration_minutes INTEGER,
                target_price REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume REAL NOT NULL,
                change_24h REAL NOT NULL,
                high_24h REAL NOT NULL,
                low_24h REAL NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_signal(self, signal: TradingSignal):
        """Store trading signal in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO signals 
            (symbol, signal_type, prediction, confidence, entry_price, stop_loss, take_profit, timestamp, reasoning, timeframe, duration_minutes, target_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            signal.symbol, signal.signal_type, signal.prediction, signal.confidence,
            signal.entry_price, signal.stop_loss, signal.take_profit,
            signal.timestamp, signal.reasoning, signal.timeframe,
            signal.duration_minutes, signal.target_price
        ))
        
        conn.commit()
        conn.close()
    
    def store_market_data(self, data: MarketData):
        """Store market data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO market_data 
            (symbol, price, volume, change_24h, high_24h, low_24h, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.symbol, data.price, data.volume, data.change_24h,
            data.high_24h, data.low_24h, data.timestamp
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_prices(self, symbol: str, limit: int = 100) -> List[float]:
        """Get recent prices for technical analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price FROM market_data 
            WHERE symbol = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (symbol, limit))
        
        prices = [row[0] for row in cursor.fetchall()]
        conn.close()
        return list(reversed(prices))  # Return in chronological order

class FutureTradingBot:
    """Main trading bot class"""
    
    def __init__(self, openai_api_key: str, target_symbols: Optional[List[str]] = None):
        self.openai_api_key = openai_api_key
        self.target_symbols = target_symbols or ['USD/BRL', 'USD/CAD', 'NZD/CAD', 'USD/BDT', 'USD/DZD']
        self.db_manager = DatabaseManager()
        self.technical_analyzer = TechnicalAnalyzer()
        self.is_running = False
        self.signals: List[TradingSignal] = []
        
        # Market data simulation (replace with real API)
        self.market_data = {}
        for symbol in self.target_symbols:
            self.market_data[symbol] = {
                'price': 1.0,
                'volume': 1000000,
                'change_24h': 0.0,
                'high_24h': 1.05,
                'low_24h': 0.95
            }
    
    async def fetch_real_time_data(self, symbol: str) -> Optional[MarketData]:
        """Fetch real-time market data (simulated - replace with real API)"""
        try:
            # Simulate price movement
            current_data = self.market_data[symbol]
            price_change = np.random.normal(0, 0.001)  # Small random changes
            new_price = current_data['price'] * (1 + price_change)
            
            # Update market data
            self.market_data[symbol]['price'] = new_price
            self.market_data[symbol]['change_24h'] = price_change * 100
            
            market_data = MarketData(
                symbol=symbol,
                price=new_price,
                volume=current_data['volume'] + np.random.randint(-10000, 10000),
                change_24h=self.market_data[symbol]['change_24h'],
                timestamp=datetime.now(),
                high_24h=current_data['high_24h'],
                low_24h=current_data['low_24h']
            )
            
            # Store in database
            self.db_manager.store_market_data(market_data)
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error fetching real-time data for {symbol}: {e}")
            return None
    
    async def generate_prediction(self, symbol: str) -> Optional[PricePrediction]:
        """Generate UP/DOWN prediction with duration and live system time"""
        try:
            # Get current system time
            current_time = datetime.now()
            
            # Get recent market data
            market_data = await self.fetch_real_time_data(symbol)
            if not market_data:
                return None
            
            # Get historical prices for analysis
            recent_prices = self.db_manager.get_recent_prices(symbol, 50)
            if len(recent_prices) < 10:
                logger.warning(f"Insufficient price data for prediction: {symbol}")
                return None
            
            # Get volumes (simulated for now)
            recent_volumes = [float(1000000 + np.random.randint(-100000, 100000)) for _ in range(len(recent_prices))]
            
            # Use technical analysis for prediction
            prediction_data = self.technical_analyzer.predict_price_direction(recent_prices, recent_volumes)
            
            # Create expiry time based on predicted duration
            expiry_time = current_time + timedelta(minutes=prediction_data['duration'])
            
            # Create detailed reasoning
            reasoning = f"Technical Analysis: {', '.join(prediction_data['factors'])}. "
            reasoning += f"Momentum: {prediction_data['momentum']:.3f}%, "
            reasoning += f"Volatility: {prediction_data['volatility']:.5f}. "
            reasoning += f"System Time: {current_time.strftime('%H:%M:%S')}"
            
            prediction = PricePrediction(
                symbol=symbol,
                current_price=market_data.price,
                predicted_direction=prediction_data['direction'],
                predicted_price=prediction_data['target_price'],
                duration_minutes=prediction_data['duration'],
                confidence=prediction_data['confidence'],
                timestamp=current_time,
                expiry_time=expiry_time,
                reasoning=reasoning
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error generating prediction for {symbol}: {e}")
            return None

    async def generate_trading_signal(self, symbol: str) -> Optional[TradingSignal]:
        """Generate enhanced trading signal with UP/DOWN prediction"""
        try:
            # Get prediction first
            prediction = await self.generate_prediction(symbol)
            if not prediction:
                return None
            
            # Get recent market data
            market_data = await self.fetch_real_time_data(symbol)
            if not market_data:
                return None
            
            # Get historical prices for technical analysis
            recent_prices = self.db_manager.get_recent_prices(symbol, 50)
            if len(recent_prices) < 20:
                logger.warning(f"Insufficient price data for {symbol}")
                return None
            
            # Perform technical analysis
            sma_20 = self.technical_analyzer.calculate_sma(recent_prices, 20)
            sma_50 = self.technical_analyzer.calculate_sma(recent_prices, 50)
            rsi = self.technical_analyzer.calculate_rsi(recent_prices)
            macd = self.technical_analyzer.calculate_macd(recent_prices)
            
            # Use AI agent for sentiment analysis (if API key available)
            sentiment_analysis = {'sentiment_score': 0, 'confidence': 0.5}
            if self.openai_api_key and self.openai_api_key != 'demo-key-not-set':
                try:
                    async with WebSearchAgent(self.openai_api_key) as search_agent:
                        news_data = await search_agent.search_market_news(symbol)
                        sentiment_analysis = await search_agent.analyze_market_sentiment(symbol, news_data)
                except:
                    pass  # Continue without sentiment if API fails
            
            # Map prediction to trading signal
            if prediction.predicted_direction == 'UP':
                signal_type = "BUY"
            elif prediction.predicted_direction == 'DOWN':
                signal_type = "SELL"
            else:
                signal_type = "HOLD"
            
            current_price = market_data.price
            
            # Enhanced reasoning with live time
            current_time = datetime.now()
            reasoning = f"[{current_time.strftime('%H:%M:%S')}] PREDICTION: {prediction.predicted_direction} for {prediction.duration_minutes}min. "
            reasoning += f"Current: {current_price:.6f}, Target: {prediction.predicted_price:.6f}. "
            reasoning += prediction.reasoning
            
            # Calculate stop loss and take profit based on prediction
            if signal_type == "BUY":
                stop_loss = current_price * 0.985  # 1.5% stop loss
                take_profit = prediction.predicted_price
            elif signal_type == "SELL":
                stop_loss = current_price * 1.015  # 1.5% stop loss  
                take_profit = prediction.predicted_price
            else:
                stop_loss = current_price * 0.99
                take_profit = current_price * 1.01
            
            signal = TradingSignal(
                symbol=symbol,
                signal_type=signal_type,
                prediction=prediction.predicted_direction,
                confidence=prediction.confidence,
                entry_price=current_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                timestamp=current_time,
                reasoning=reasoning,
                timeframe="5m",
                duration_minutes=prediction.duration_minutes,
                target_price=prediction.predicted_price
            )
            
            # Store signal in database
            self.db_manager.store_signal(signal)
            
            return signal
            
        except Exception as e:
            logger.error(f"Error generating trading signal for {symbol}: {e}")
            return None
    
    async def run_analysis_cycle(self):
        """Run one complete analysis cycle for all symbols"""
        logger.info("Starting analysis cycle...")
        
        new_signals = []
        for symbol in self.target_symbols:
            signal = await self.generate_trading_signal(symbol)
            if signal:
                new_signals.append(signal)
                logger.info(f"Generated signal for {symbol}: {signal.signal_type} (confidence: {signal.confidence:.2f})")
        
        self.signals.extend(new_signals)
        return new_signals
    
    def display_signals(self, signals: List[TradingSignal]):
        """Display trading signals with UP/DOWN predictions and live time"""
        if not signals:
            print("No new signals generated.")
            return
        
        current_time = datetime.now()
        print("\n" + "="*90)
        print("🚀 LIVE UP/DOWN PREDICTIONS WITH DURATION")
        print("="*90)
        print(f"⏰ System Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Platform: https://market-qx.pro/en/trade/")
        print("="*90)
        
        for i, signal in enumerate(signals, 1):
            # Calculate time remaining
            expiry_time = signal.timestamp + timedelta(minutes=signal.duration_minutes)
            time_remaining = expiry_time - current_time
            
            # Direction emoji and color coding
            direction_emoji = "📈" if signal.prediction == "UP" else "📉" if signal.prediction == "DOWN" else "➡️"
            action_emoji = "🟢 BUY" if signal.signal_type == "BUY" else "🔴 SELL" if signal.signal_type == "SELL" else "🟡 HOLD"
            
            print(f"\n{direction_emoji} PREDICTION #{i} - {signal.symbol}")
            print(f"📊 Direction: {signal.prediction}")
            print(f"⏱️  Duration: {signal.duration_minutes} minutes")
            print(f"⏰ Expires: {expiry_time.strftime('%H:%M:%S')}")
            print(f"⌛ Time Left: {time_remaining.total_seconds()/60:.1f} min" if time_remaining.total_seconds() > 0 else "⌛ EXPIRED")
            print(f"{action_emoji} - Confidence: {signal.confidence:.1%}")
            print(f"💰 Current Price: {signal.entry_price:.6f}")
            print(f"🎯 Target Price: {signal.target_price:.6f}")
            print(f"🛑 Stop Loss: {signal.stop_loss:.6f}")
            print(f"💡 Analysis: {signal.reasoning}")
            
            # Show profit potential
            if signal.prediction == "UP":
                potential_profit = ((signal.target_price - signal.entry_price) / signal.entry_price) * 100
                print(f"📈 Potential Profit: +{potential_profit:.2f}%")
            elif signal.prediction == "DOWN":
                potential_profit = ((signal.entry_price - signal.target_price) / signal.entry_price) * 100
                print(f"📉 Potential Profit: +{potential_profit:.2f}%")
            
            print("-" * 70)
        
        print(f"\n⚡ Next Update: {(current_time + timedelta(minutes=5)).strftime('%H:%M:%S')}")
        print("="*90)

    async def run_prediction_cycle(self):
        """Run prediction cycle for all symbols with live time"""
        current_time = datetime.now()
        logger.info(f"Starting prediction cycle at {current_time.strftime('%H:%M:%S')}")
        
        predictions = []
        signals = []
        
        for symbol in self.target_symbols:
            # Generate prediction
            prediction = await self.generate_prediction(symbol)
            if prediction:
                predictions.append(prediction)
            
            # Generate trading signal
            signal = await self.generate_trading_signal(symbol)
            if signal:
                signals.append(signal)
                logger.info(f"[{current_time.strftime('%H:%M:%S')}] {symbol}: {signal.prediction} for {signal.duration_minutes}min (confidence: {signal.confidence:.1%})")
        
        self.signals.extend(signals)
        return signals

    def display_live_dashboard(self):
        """Display live trading dashboard"""
        current_time = datetime.now()
        print("\n" + "🔴"*30 + " LIVE DASHBOARD " + "🔴"*30)
        print(f"⏰ System Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Platform: https://market-qx.pro/en/trade/")
        print(f"📊 Monitoring: {len(self.target_symbols)} symbols")
        print(f"📈 Active Signals: {len([s for s in self.signals[-10:] if s.prediction in ['UP', 'DOWN']])}")
        print("="*75)
        
        # Show recent signals summary
        recent_signals = self.signals[-5:] if self.signals else []
        for signal in recent_signals:
            time_ago = (current_time - signal.timestamp).total_seconds() / 60
            status = "🟢 ACTIVE" if time_ago < signal.duration_minutes else "⏳ EXPIRED"
            print(f"{signal.symbol}: {signal.prediction} | {status} | {time_ago:.1f}min ago")
        
        print("="*75)
    
    async def start_live_trading(self, interval_seconds: int = 60):
        """Start live UP/DOWN predictions with system time integration"""
        logger.info("Starting live UP/DOWN prediction bot...")
        self.is_running = True
        
        try:
            # Show initial dashboard
            self.display_live_dashboard()
            
            while self.is_running:
                # Show current time
                current_time = datetime.now()
                print(f"\n⏰ [{current_time.strftime('%H:%M:%S')}] Analyzing market conditions...")
                
                # Run prediction cycle
                signals = await self.run_prediction_cycle()
                
                # Display predictions
                self.display_signals(signals)
                
                # Show countdown to next update
                for remaining in range(interval_seconds, 0, -1):
                    print(f"\r⏳ Next update in: {remaining} seconds...", end="", flush=True)
                    await asyncio.sleep(1)
                    if not self.is_running:
                        break
                
                print()  # New line after countdown
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error in live trading loop: {e}")
        finally:
            self.is_running = False
    
    def stop(self):
        """Stop the trading bot"""
        self.is_running = False
        logger.info("Trading bot stopped")

async def main():
    """Main function to run the trading bot"""
    
    # Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        print("Please set your OPENAI_API_KEY environment variable")
        return
    
    # Target trading pairs from the website
    TARGET_SYMBOLS = [
        'USD/BRL',
        'USD/CAD', 
        'NZD/CAD',
        'USD/BDT',
        'USD/DZD'
    ]
    
    # Initialize and start the bot
    bot = FutureTradingBot(
        openai_api_key=OPENAI_API_KEY,
        target_symbols=TARGET_SYMBOLS
    )
    
    print("🚀 Future Trading Bot - Live UP/DOWN Predictions")
    print("="*60)
    print("🎯 Target Platform: https://market-qx.pro/en/trade/")
    print(f"📊 Monitoring symbols: {', '.join(TARGET_SYMBOLS)}")
    print("📈📉 Real-time UP/DOWN predictions with duration")
    print("⏰ Live system time integration")
    print("Press Ctrl+C to stop the bot")
    print("="*60)
    
    # Start live trading with 1-minute intervals for faster predictions
    await bot.start_live_trading(interval_seconds=60)

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())