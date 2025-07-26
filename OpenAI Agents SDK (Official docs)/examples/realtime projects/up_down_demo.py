"""
UP/DOWN Prediction Demo
Shows live trading predictions with system time and duration
"""

import asyncio
from datetime import datetime, timedelta
import random

class UpDownDemo:
    def __init__(self):
        self.symbols = ['USD/BRL', 'USD/CAD', 'NZD/CAD', 'USD/BDT', 'USD/DZD']
        self.prices = {
            'USD/BRL': 0.16900,
            'USD/CAD': 1.35420,
            'NZD/CAD': 0.89200,
            'USD/BDT': 0.00850,
            'USD/DZD': 0.00745
        }
    
    def generate_prediction(self, symbol):
        """Generate UP/DOWN prediction with duration"""
        current_time = datetime.now()
        current_price = self.prices[symbol]
        
        # Simulate price changes
        price_change = random.uniform(-0.002, 0.002)
        new_price = current_price * (1 + price_change)
        self.prices[symbol] = new_price
        
        # Generate prediction
        directions = ['UP', 'DOWN']
        weights = [0.6, 0.4] if price_change > 0 else [0.4, 0.6]
        direction = random.choices(directions, weights=weights)[0]
        
        # Duration between 1-10 minutes
        duration = random.randint(1, 10)
        
        # Confidence based on price momentum
        confidence = min(0.95, 0.6 + abs(price_change) * 100)
        
        # Target price
        if direction == 'UP':
            target_price = new_price * (1 + random.uniform(0.001, 0.005))
        else:
            target_price = new_price * (1 - random.uniform(0.001, 0.005))
        
        return {
            'symbol': symbol,
            'current_price': new_price,
            'direction': direction,
            'duration': duration,
            'confidence': confidence,
            'target_price': target_price,
            'timestamp': current_time,
            'expiry_time': current_time + timedelta(minutes=duration)
        }
    
    def display_predictions(self, predictions):
        """Display UP/DOWN predictions with live time"""
        current_time = datetime.now()
        
        print("\n" + "🔴"*25 + " LIVE UP/DOWN PREDICTIONS " + "🔴"*25)
        print(f"⏰ System Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Platform: https://market-qx.pro/en/trade/")
        print("="*80)
        
        for i, pred in enumerate(predictions, 1):
            # Time calculations
            time_remaining = pred['expiry_time'] - current_time
            minutes_left = time_remaining.total_seconds() / 60
            
            # Direction styling
            if pred['direction'] == 'UP':
                direction_display = "📈 UP"
                color = "🟢"
            else:
                direction_display = "📉 DOWN" 
                color = "🔴"
            
            # Profit calculation
            profit_pct = abs((pred['target_price'] - pred['current_price']) / pred['current_price']) * 100
            
            print(f"\n{color} PREDICTION #{i} - {pred['symbol']}")
            print(f"📊 Direction: {direction_display}")
            print(f"⏱️  Duration: {pred['duration']} minutes")
            print(f"⏰ Expires: {pred['expiry_time'].strftime('%H:%M:%S')}")
            
            if minutes_left > 0:
                print(f"⌛ Time Left: {minutes_left:.1f} minutes")
            else:
                print(f"⌛ EXPIRED ({abs(minutes_left):.1f} min ago)")
            
            print(f"🎯 Confidence: {pred['confidence']:.1%}")
            print(f"💰 Current: {pred['current_price']:.6f}")
            print(f"🎯 Target: {pred['target_price']:.6f}")
            print(f"💹 Potential: +{profit_pct:.2f}%")
            print("-" * 60)
        
        print(f"\n⚡ Next Update: {(current_time + timedelta(seconds=30)).strftime('%H:%M:%S')}")
        print("="*80)
    
    async def run_demo(self, cycles=10):
        """Run the UP/DOWN prediction demo"""
        print("🚀 UP/DOWN Trading Predictions Demo")
        print("📈📉 Live system time integration with duration forecasts")
        print("🎯 Simulating market-qx.pro platform predictions")
        print("\nPress Ctrl+C to stop...\n")
        
        try:
            for cycle in range(cycles):
                # Generate predictions for all symbols
                predictions = []
                for symbol in self.symbols:
                    prediction = self.generate_prediction(symbol)
                    predictions.append(prediction)
                
                # Display predictions
                self.display_predictions(predictions)
                
                # Countdown to next update
                for remaining in range(30, 0, -1):
                    print(f"\r⏳ Next prediction in: {remaining} seconds...", end="", flush=True)
                    await asyncio.sleep(1)
                
                print()  # New line
                
        except KeyboardInterrupt:
            print("\n\n✅ Demo stopped by user")
        
        print("\n🎉 Demo completed!")
        print("\n🚀 To run the full bot:")
        print("1. Set OpenAI API key: set OPENAI_API_KEY=your_key_here")
        print("2. Run: python bot.py")

async def main():
    demo = UpDownDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
