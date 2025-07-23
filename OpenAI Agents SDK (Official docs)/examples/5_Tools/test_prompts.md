# 🧪 Comprehensive Test Prompts for Agentic Food Finder

## 🎯 **How to Test:**
Run the command: `python agentic_food_finder.py`

## 📝 **Test Categories**

### 🔍 **1. Location & Distance Based Searches**
```
restaurants within 2km with good ratings
find food places within 5km radius and budget friendly
show me restaurants within 3km with 4+ rating and lowest price
restaurants near me within 1.5km with delivery available
```

### 💰 **2. Price & Budget Focused Searches**
```
cheapest fast food options with current promotions
restaurants under 500 PKR budget with good ratings
find expensive restaurants with premium quality
low price range restaurants with delivery deals
budget friendly options within 3km radius
```

### ⭐ **3. Rating & Quality Based Searches**
```
highest rated restaurants within 5km budget friendly
restaurants with 4+ rating and good deals
find 4.5+ rated restaurants near me with delivery
best rated chinese restaurants with affordable prices
```

### 🍽️ **4. Cuisine Specific Searches**
```
chinese restaurants with good ratings near me
pizza places with delivery under 1000 PKR
best fast food restaurants with current deals
find pakistani restaurants with family deals
show me italian restaurants with home delivery
```

### 🎯 **5. Deals & Promotions Searches**
```
midnight deals on foodpanda for KFC or similar fast food
late night food deals available right now
foodpanda restaurants with student discounts
find current deals on careem food delivery
search for buy 1 get 1 offers on pizza
midnight deals available on any fast food app
```

### 🕛 **6. Time-Based Searches**
```
restaurants open late night with delivery
midnight food options with deals
24/7 restaurants with good ratings near me
late night delivery options under 800 PKR
```

### 📱 **7. Platform Specific Searches**
```
foodpanda deals for chinese restaurants
careem delivery options with current promotions
uber eats restaurants with good ratings near me
find deals on all delivery platforms
```

### 🏆 **8. Complex Multi-Filter Searches**
```
restaurants within 3km with 4+ rating lowest price and current deals
fast food chains with midnight deals on foodpanda under 600 PKR
pizza places within 2km with family deals and good ratings
chinese restaurants with delivery under 1000 PKR and student discounts
```

### 🎪 **9. Natural Language Conversational Tests**
```
I'm hungry and want something cheap and nearby
looking for good food deals for a student budget
need late night food delivery with best offers
want pizza for family with current promotions
searching for authentic chinese food with delivery
```

### 🔧 **10. Edge Cases & Specific Requests**
```
KFC deals with specific items and prices
list all midnight deals with contact numbers
premium restaurants with outdoor seating options
halal certified restaurants with family packages
restaurants with drive-thru and 24/7 service
```

---

## 🎯 **Quick Test Sequence (Copy & Paste):**

### **Test 1:** Location Search
```
restaurants within 3km with 4+ rating and lowest price
```

### **Test 2:** Deals Search
```
midnight deals on foodpanda for KFC
```

### **Test 3:** Cuisine Search
```
chinese restaurants with good ratings near me
```

### **Test 4:** Complex Search
```
fast food restaurants within 2km with deals under 500 PKR
```

### **Test 5:** Platform Specific
```
careem delivery restaurants with current promotions
```

---

## 🏆 **Expected Agent Behavior:**

1. **Query Parser Agent** should extract parameters like:
   - Distance: 3km, 2km, 5km
   - Rating: 4+, 4.5+, good ratings
   - Price: under 500 PKR, budget friendly, lowest price
   - Cuisine: chinese, pizza, fast food, pakistani
   - Platform: foodpanda, careem, uber eats
   - Time: midnight, late night, 24/7

2. **Restaurant Searcher Agent** should call appropriate tools:
   - `search_restaurants_by_radius()` for distance-based searches
   - `search_restaurants_by_cuisine()` for cuisine-specific searches

3. **Deals Finder Agent** should call:
   - `search_deals_by_platform()` for platform-specific deals
   - `get_midnight_deals()` for time-based promotions

4. **Results Formatter Agent** should present:
   - Clear restaurant information with ratings, prices, distance
   - Deal details with validity, platforms, minimum orders
   - Recommendations based on user criteria

---

## 🚀 **Success Indicators:**

✅ **Multi-Agent Coordination**: All 4 agents work together seamlessly
✅ **Tool Calling**: Agents call appropriate function tools based on query
✅ **Natural Language Processing**: System understands complex conversational queries
✅ **Result Quality**: Relevant restaurants and deals are returned
✅ **UI Experience**: Professional rich console interface with animations
✅ **Error Handling**: System gracefully handles edge cases and missing data

---

## 📊 **Performance Metrics:**

- **Response Time**: Should complete within 10-15 seconds
- **Accuracy**: Results should match query criteria
- **Agent Chain**: All 4 agents should appear in processing chain
- **Tool Usage**: Appropriate tools should be called based on query type
- **Data Quality**: Restaurant and deal information should be comprehensive
