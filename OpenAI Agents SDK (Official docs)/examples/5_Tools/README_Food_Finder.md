# Elite Food Finder - AI-Powered Restaurant Search

## 🍽️ Overview

The Elite Food Finder is a sophisticated restaurant recommendation system that uses AI to find the best food options based on your preferences, budget, and location. It features a beautiful command-line interface with rich text formatting and real-time search capabilities.

## ✨ Features

### 🤖 AI-Powered Search
- **OpenAI GPT-4 Integration**: Uses advanced AI to search for real restaurant data
- **Intelligent Parsing**: Processes natural language restaurant information
- **Fallback System**: Comprehensive local database when API is unavailable

### 🎯 Smart Filtering
- **Food Categories**: 8 different food types including:
  - 🍕 Pizza
  - 🍔 Burgers & Fast Food
  - 🥡 Chinese Food
  - 🍝 Italian Food
  - 🥘 Pakistani/Desi Food
  - 🍰 Desserts & Sweets
  - ☕ Cafe & Coffee
  - 🍽️ Fine Dining

- **Price Ranges**: 3 budget categories:
  - 💸 **Lowest**: Budget-friendly options (Under Rs. 500)
  - 💰 **Highest**: Mid-range to expensive (Rs. 500-2000)
  - 👑 **Premium**: Luxury & fine dining (Above Rs. 2000)

### 🖥️ Professional UI
- **Rich Text Formatting**: Beautiful colored output with panels and tables
- **ASCII Art Logo**: Custom food finder branding
- **Loading Animations**: Professional spinning progress indicators
- **Interactive Prompts**: User-friendly input system
- **Responsive Design**: Adapts to different terminal sizes

### 📊 Comprehensive Restaurant Data
Each restaurant result includes:
- 🏪 **Name & Location**: Full restaurant details
- ⭐ **Ratings**: 5-star rating system
- 💰 **Price Estimates**: Accurate PKR pricing
- 📞 **Contact Info**: Phone numbers and websites
- 🕐 **Operating Hours**: Current business hours
- 🚚 **Delivery Options**: Availability information
- 🎯 **Current Deals**: Live promotions and discounts
- 🔥 **Popular Items**: Recommended menu items
- 📏 **Distance**: Approximate travel distance

## 🚀 Installation & Setup

### Prerequisites
```bash
# Python 3.8+ required
# Install dependencies
pip install openai rich pydantic asyncio
```

### Environment Setup
1. Create a `.env` file with your OpenAI API key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

2. Ensure the `g_config.py` file is properly configured

## 📱 Usage

### Basic Usage
```bash
python food_finder_agent_real.py
```

### Available Files
1. **`food_finder_agent_real.py`** - Full AI-powered version with OpenAI integration
2. **`food_finder_agent.py`** - Demo version with pre-loaded restaurant data
3. **`01_web_search_demo.py`** - Original coffee shop finder demo

### Interactive Flow
1. **Welcome Screen**: Displays the Elite Food Finder logo and features
2. **Food Selection**: Choose from 8 food categories
3. **Budget Selection**: Pick your price range preference
4. **AI Search**: Watch the AI search for restaurants in real-time
5. **Results Display**: View detailed restaurant recommendations
6. **Repeat Option**: Search for additional food types

## 🏆 Restaurant Database

### Major Chains Included
- **Fast Food**: KFC, McDonald's, Hardee's, Burger King
- **Pizza**: Pizza Hut, Domino's Pizza
- **Chinese**: Yum! Chinese & Thai, China Kitchen
- **Fine Dining**: Cosa Nostra, Premium establishments
- **Local Favorites**: Popular Pakistani restaurants

### Real-Time Features
- ✅ Current promotional deals
- ✅ Live pricing information
- ✅ Operating hours
- ✅ Delivery availability
- ✅ Contact information
- ✅ Distance calculations

## 🎨 UI Components

### Visual Elements
- **🍕 ASCII Art Logo**: Custom food finder branding
- **📊 Rich Tables**: Structured data presentation
- **🎯 Color Coding**: Different colors for different information types
- **⚡ Progress Bars**: Real-time search progress
- **📱 Panels**: Elegant information containers

### Color Scheme
- **Gold**: Branding and titles
- **Cyan**: Interactive prompts and labels
- **Green**: Success messages and top picks
- **Blue**: Information panels
- **Red**: Error messages
- **Yellow**: Warnings and highlights

## 🔧 Technical Architecture

### Core Components
1. **RealWebSearchTool**: AI-powered restaurant search engine
2. **Restaurant Model**: Pydantic data validation
3. **UI Functions**: Rich text display components
4. **Interactive System**: User input handling

### Error Handling
- **API Fallback**: Graceful degradation when APIs are unavailable
- **JSON Parsing**: Robust data processing with error recovery
- **User Interruption**: Clean exit on Ctrl+C
- **Network Issues**: Informative error messages

### Performance
- **Async Operations**: Non-blocking API calls
- **Response Caching**: Efficient data handling
- **Memory Optimization**: Lightweight data structures

## 🌟 Example Output

```
🎉 AI found 3 excellent options for burger!

╭───────────────── 🏆 TOP PICK! Option 1: KFC ──────────────────╮
│ 🏪 Name         KFC                                           │
│ 📍 Location     Multiple outlets across Lahore                │
│ ⭐ Rating       4.3/5.0 ⭐⭐⭐⭐                                 │
│ 💵 Est. Price   Rs. 300-1500                                  │
│ 🎯 Current Deals • Tuesday Deal: Krunch Burger + Drink Rs. 399│
│ 🔥 Popular Items Zinger Burger, Hot Wings, Chicken Pieces     │
╰───────────────────────────────────────────────────────────────╯
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Test thoroughly
5. Submit a pull request

### Areas for Enhancement
- **Additional Cuisines**: More food categories
- **Location Expansion**: Other Pakistani cities
- **Real-time Integration**: Live menu APIs
- **User Preferences**: Saved favorites
- **Review System**: User ratings integration

## 📄 License

This project is developed for educational and demonstration purposes as part of the OpenAI Agents SDK examples.

## 🙏 Acknowledgments

- **OpenAI**: For GPT-4 API and AI capabilities
- **Rich Library**: For beautiful terminal formatting
- **Pydantic**: For data validation
- **Agentic Developer**: For system architecture and design

---

**Enjoy finding your perfect meal with AI! 🍽️✨**
