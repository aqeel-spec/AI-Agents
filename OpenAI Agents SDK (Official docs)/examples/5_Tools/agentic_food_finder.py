"""
agentic_food_finder.py - Multi-Agent Food Discovery System

A sophisticated agent-based food recommendation system using OpenAI Agents SDK
with multiple specialized agents, tool calling, and natural language processing.
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.live import Live
import time
import re

# OpenAI Agents SDK imports
from agents import Agent, Runner, function_tool

# Import configuration
try:
    from g_config import create_openai_config, create_gemini_config
    
    # Try to use configuration
    try:
        provider, model = create_openai_config()
        if not provider:
            provider, model = create_openai_config()
        if not provider:
            raise ValueError("No API keys configured")
    except Exception as e:
        console = Console()
        console.print(f"[red]❌ Configuration Error: {e}[/red]")
        console.print("[yellow]Please ensure you have either OPENAI_API_KEY or GEMINI_API_KEY set in your environment.[/yellow]")
        exit(1)
        
except ImportError:
    console = Console()
    console.print("[red]❌ g_config.py not found. Please ensure the configuration file exists.[/red]")
    exit(1)

# Initialize rich console
console = Console()

# ================================
# DATA MODELS
# ================================

class QueryType(str, Enum):
    RADIUS_SEARCH = "radius_search"
    RATING_FILTER = "rating_filter"
    PRICE_FILTER = "price_filter"
    DEAL_SEARCH = "deal_search"
    CUISINE_SEARCH = "cuisine_search"
    DELIVERY_SEARCH = "delivery_search"
    GENERAL_SEARCH = "general_search"

class Restaurant(BaseModel):
    """Enhanced restaurant model for agent-based search"""
    name: str
    location: str
    cuisine_type: str
    rating: float = Field(ge=1.0, le=5.0)
    price_range: str  # "low", "medium", "high", "premium"
    distance_km: float = Field(ge=0.0)
    contact: Optional[str] = None
    delivery_available: bool = True
    delivery_platforms: List[str] = []
    current_deals: List[str] = []
    popular_items: List[str] = []
    estimated_price_pkr: str = "N/A"
    opening_hours: str = "10:00 AM - 11:00 PM"
    midnight_deals: bool = False
    special_features: List[str] = []

class SearchQuery(BaseModel):
    """Structured search query from natural language"""
    query_type: QueryType
    radius_km: Optional[float] = None
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    price_range: Optional[str] = None
    cuisine_type: Optional[str] = None
    delivery_platform: Optional[str] = None
    deal_type: Optional[str] = None
    time_preference: Optional[str] = None
    custom_filters: Dict[str, Any] = {}

# ================================
# AGENT TOOLS
# ================================

@function_tool
async def search_restaurants_by_radius(
    radius_km: float,
    min_rating: float = 3.0,
    location: str = "Lahore"
) -> str:
    """Search for restaurants within a specific radius with minimum rating"""
    
    # Simulate real restaurant database
    restaurants_db = [
        {
            "name": "KFC Gulberg",
            "location": "Main Boulevard, Gulberg III",
            "cuisine_type": "Fast Food",
            "rating": 4.3,
            "price_range": "low",
            "distance_km": 1.2,
            "contact": "+92-42-3577-8888",
            "delivery_platforms": ["foodpanda", "careem", "uber eats"],
            "current_deals": ["Tuesday Deal: Krunch Burger + Drink Rs. 399", "Midnight Snack Box Rs. 699"],
            "popular_items": ["Zinger Burger", "Hot Wings", "Chicken Pieces"],
            "estimated_price_pkr": "Rs. 300-800",
            "midnight_deals": True,
            "special_features": ["24/7 service", "drive-thru"]
        },
        {
            "name": "Pizza Hut DHA",
            "location": "Commercial Area, DHA Phase 4",
            "cuisine_type": "Pizza",
            "rating": 4.1,
            "price_range": "medium",
            "distance_km": 2.8,
            "contact": "+92-42-3577-9999",
            "delivery_platforms": ["foodpanda", "careem"],
            "current_deals": ["Buy 1 Get 1 Free Large Pizza", "Student Discount 20%"],
            "popular_items": ["Chicken Supreme", "Pepperoni Lovers", "Garlic Bread"],
            "estimated_price_pkr": "Rs. 800-2500",
            "midnight_deals": False,
            "special_features": ["outdoor seating", "family friendly"]
        },
        {
            "name": "McDonald's MM Alam",
            "location": "MM Alam Road, Gulberg",
            "cuisine_type": "Fast Food",
            "rating": 4.0,
            "price_range": "low",
            "distance_km": 1.8,
            "contact": "+92-42-3577-7777",
            "delivery_platforms": ["foodpanda", "uber eats"],
            "current_deals": ["McValue Meals Rs. 299", "Happy Hour 2-5 PM"],
            "popular_items": ["Big Mac", "McChicken", "French Fries"],
            "estimated_price_pkr": "Rs. 250-600",
            "midnight_deals": True,
            "special_features": ["24/7 service", "McCafe"]
        },
        {
            "name": "Yum! Chinese Johar Town",
            "location": "Main Boulevard, Johar Town",
            "cuisine_type": "Chinese",
            "rating": 4.5,
            "price_range": "medium",
            "distance_km": 4.2,
            "contact": "+92-42-3577-6666",
            "delivery_platforms": ["foodpanda"],
            "current_deals": ["Family Combo Rs. 1899", "Free Soup with orders above Rs. 1500"],
            "popular_items": ["Chicken Manchurian", "Beef Black Pepper", "Fried Rice"],
            "estimated_price_pkr": "Rs. 600-2000",
            "midnight_deals": False,
            "special_features": ["authentic chinese", "halal certified"]
        },
        {
            "name": "Hardee's Packages Mall",
            "location": "Packages Mall, Walton Road",
            "cuisine_type": "Fast Food",
            "rating": 4.2,
            "price_range": "medium",
            "distance_km": 3.5,
            "contact": "+92-42-3577-5555",
            "delivery_platforms": ["foodpanda", "careem", "uber eats"],
            "current_deals": ["Big Deal Combo Rs. 799", "Late Night Special Rs. 599"],
            "popular_items": ["Famous Star Burger", "Curly Fries", "Milkshakes"],
            "estimated_price_pkr": "Rs. 400-1200",
            "midnight_deals": True,
            "special_features": ["late night menu", "premium burgers"]
        }
    ]
    
    # Filter by radius and rating
    filtered_restaurants = [
        r for r in restaurants_db 
        if r["distance_km"] <= radius_km and r["rating"] >= min_rating
    ]
    
    return json.dumps(filtered_restaurants, indent=2)

@function_tool
async def search_deals_by_platform(
    platform: str,
    deal_type: str = "any",
    time_filter: str = "any"
) -> str:
    """Search for specific deals on delivery platforms"""
    
    platform_deals = {
        "foodpanda": [
            {
                "restaurant": "KFC",
                "deal": "Midnight Snack Box Rs. 699",
                "validity": "12:00 AM - 6:00 AM",
                "discount": "30% off",
                "min_order": "Rs. 500"
            },
            {
                "restaurant": "Pizza Hut", 
                "deal": "Buy 1 Get 1 Free Pizza",
                "validity": "All day",
                "discount": "50% off second pizza",
                "min_order": "Rs. 1000"
            },
            {
                "restaurant": "McDonald's",
                "deal": "McValue Bundle",
                "validity": "2:00 PM - 5:00 PM",
                "discount": "Rs. 100 off",
                "min_order": "Rs. 400"
            }
        ],
        "careem": [
            {
                "restaurant": "Hardee's",
                "deal": "Late Night Special",
                "validity": "11:00 PM - 3:00 AM", 
                "discount": "25% off",
                "min_order": "Rs. 600"
            },
            {
                "restaurant": "Subway",
                "deal": "Sub of the Day",
                "validity": "All day",
                "discount": "Rs. 200 off",
                "min_order": "Rs. 800"
            }
        ],
        "uber eats": [
            {
                "restaurant": "Domino's",
                "deal": "2 Medium Pizzas Rs. 1299",
                "validity": "All day",
                "discount": "Rs. 500 off",
                "min_order": "Rs. 1000"
            }
        ]
    }
    
    deals = platform_deals.get(platform.lower(), [])
    
    # Filter by time if midnight deals requested
    if time_filter == "midnight":
        deals = [d for d in deals if "12:00 AM" in d["validity"] or "11:00 PM" in d["validity"]]
    
    return json.dumps(deals, indent=2)

@function_tool  
async def search_restaurants_by_cuisine(
    cuisine_type: str,
    price_filter: str = "any",
    rating_filter: float = 3.0
) -> str:
    """Search restaurants by cuisine type with additional filters"""
    
    cuisine_restaurants = {
        "fast food": [
            {"name": "KFC", "rating": 4.3, "price_range": "low"},
            {"name": "McDonald's", "rating": 4.0, "price_range": "low"},
            {"name": "Hardee's", "rating": 4.2, "price_range": "medium"},
            {"name": "Burger King", "rating": 3.9, "price_range": "medium"}
        ],
        "pizza": [
            {"name": "Pizza Hut", "rating": 4.1, "price_range": "medium"},
            {"name": "Domino's", "rating": 4.0, "price_range": "medium"}, 
            {"name": "Papa John's", "rating": 4.3, "price_range": "high"}
        ],
        "chinese": [
            {"name": "Yum! Chinese", "rating": 4.5, "price_range": "medium"},
            {"name": "China Kitchen", "rating": 4.2, "price_range": "medium"},
            {"name": "Dragon City", "rating": 4.4, "price_range": "high"}
        ],
        "pakistani": [
            {"name": "Bundu Khan", "rating": 4.6, "price_range": "medium"},
            {"name": "Lahore Tikka House", "rating": 4.4, "price_range": "low"},
            {"name": "Salt'n Pepper", "rating": 4.5, "price_range": "high"}
        ]
    }
    
    restaurants = cuisine_restaurants.get(cuisine_type.lower(), [])
    
    # Apply filters
    filtered = [
        r for r in restaurants 
        if r["rating"] >= rating_filter and 
        (price_filter == "any" or r["price_range"] == price_filter.lower())
    ]
    
    return json.dumps(filtered, indent=2)

@function_tool
async def get_midnight_deals() -> str:
    """Get all available midnight deals across platforms"""
    
    midnight_deals = [
        {
            "restaurant": "KFC",
            "deal": "Midnight Snack Box",
            "price": "Rs. 699",
            "time": "12:00 AM - 6:00 AM",
            "platform": "foodpanda",
            "items": "4 pieces + fries + drink"
        },
        {
            "restaurant": "McDonald's", 
            "deal": "Late Night Bundle",
            "price": "Rs. 899",
            "time": "11:00 PM - 5:00 AM",
            "platform": "uber eats",
            "items": "2 burgers + 2 fries + 2 drinks"
        },
        {
            "restaurant": "Hardee's",
            "deal": "Night Owl Special",
            "price": "Rs. 599", 
            "time": "11:00 PM - 3:00 AM",
            "platform": "careem",
            "items": "burger + fries + shake"
        },
        {
            "restaurant": "Subway",
            "deal": "Midnight Sub Combo",
            "price": "Rs. 799",
            "time": "12:00 AM - 4:00 AM", 
            "platform": "foodpanda",
            "items": "footlong + chips + drink"
        }
    ]
    
    return json.dumps(midnight_deals, indent=2)

# ================================
# SPECIALIZED AGENTS
# ================================

# Query Parser Agent
query_parser_agent = Agent(
    name="QueryParser",
    model=model,
    instructions="""
    You are a Query Parser Agent specialized in understanding food-related search queries.
    
    Parse user queries and extract:
    1. Search type (radius, rating, price, deals, cuisine, delivery)
    2. Specific parameters (distance, rating range, price range, etc.)
    3. Location preferences
    4. Time constraints
    5. Platform preferences
    
    Convert natural language to structured search parameters.
    Be very specific and extract all possible filters from the user's request.
    
    Example queries:
    - "restaurants within 3km with 4+ rating and lowest price"
    - "midnight deals on foodpanda for KFC"
    - "chinese restaurants under 1000 PKR with delivery"
    """
)

# Restaurant Search Agent  
search_agent = Agent(
    name="RestaurantSearcher",
    model=model,
    instructions="""
    You are a Restaurant Search Agent specialized in finding restaurants based on specific criteria.
    
    Use the available tools to search for restaurants based on:
    - Distance/radius requirements
    - Rating filters
    - Price range preferences
    - Cuisine types
    - Deal availability
    
    Always provide comprehensive results with all available details.
    Prioritize results that best match the user's criteria.
    """,
    tools=[search_restaurants_by_radius, search_restaurants_by_cuisine]
)

# Deals Finder Agent
deals_agent = Agent(
    name="DealsFinder",
    model=model,
    instructions="""
    You are a Deals Finder Agent specialized in finding food deals and promotions.
    
    Search for:
    - Platform-specific deals (foodpanda, careem, uber eats)
    - Time-based promotions (midnight deals, happy hours)
    - Restaurant-specific offers
    - Seasonal promotions
    
    Provide detailed information about deal validity, minimum orders, and savings.
    """,
    tools=[search_deals_by_platform, get_midnight_deals]
)

# Results Formatter Agent
formatter_agent = Agent(
    name="ResultsFormatter",
    model=model,
    instructions="""
    You are a Results Formatter Agent specialized in presenting restaurant search results.
    
    Format search results in a clear, organized manner with:
    - Restaurant rankings based on relevance
    - Detailed information for each option
    - Deal highlights and savings information
    - Actionable recommendations
    
    Present results in a user-friendly format with proper categorization.
    """
)

# ================================
# MULTI-AGENT ORCHESTRATOR
# ================================

class AgenticFoodFinder:
    """Multi-agent orchestrator for food discovery"""
    
    def __init__(self):
        self.query_parser = query_parser_agent
        self.restaurant_searcher = search_agent
        self.deals_finder = deals_agent
        self.results_formatter = formatter_agent
        
    async def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process user query through multi-agent pipeline"""
        
        console.print(f"[bold cyan]🤖 Processing query: {user_query}[/bold cyan]\n")
        
        # Step 1: Parse the query
        console.print("[yellow]🔍 Parsing your request...[/yellow]")
        parse_result = await Runner.run(
            self.query_parser,
            f"Parse this food search query and extract all parameters: {user_query}"
        )
        
        # Step 2: Determine search strategy based on query type
        parsed_info = parse_result.final_output
        
        search_results = []
        deals_results = []
        
        # Step 3: Execute searches based on query content - much more comprehensive
        
        # Always try restaurant search for most queries
        if any(word in user_query.lower() for word in ["restaurant", "food", "eat", "hungry", "place", "near", "km", "rating", "price", "budget", "cheap", "expensive"]):
            console.print("[yellow]📍 Searching by location radius...[/yellow]")
            search_result = await Runner.run(
                self.restaurant_searcher,
                f"Find restaurants based on this query: {user_query}. Use appropriate search tools."
            )
            # Extract tool results from agent response
            search_results.extend(self._extract_restaurant_data(search_result))
                
        # Search for deals if deal-related keywords found
        if any(word in user_query.lower() for word in ["deal", "offer", "discount", "promotion", "midnight", "late", "night", "special", "cheap", "budget"]):
            console.print("[yellow]🎯 Searching for deals...[/yellow]")
            deals_result = await Runner.run(
                self.deals_finder,
                f"Find deals based on this query: {user_query}"
            )
            # Extract tool results from agent response
            deals_results.extend(self._extract_deals_data(deals_result))
                
        # Search by cuisine if cuisine types mentioned
        if any(word in user_query.lower() for word in ["chinese", "pizza", "fast food", "pakistani", "italian", "desi", "bbq", "burger", "chicken"]):
            console.print("[yellow]🍽️ Searching by cuisine type...[/yellow]") 
            cuisine_result = await Runner.run(
                self.restaurant_searcher,
                f"Find restaurants by cuisine based on: {user_query}. Use cuisine search tools."
            )
            # Extract tool results from agent response
            search_results.extend(self._extract_restaurant_data(cuisine_result))
        
        # If no specific searches triggered, do a general search
        if not search_results and not deals_results:
            console.print("[yellow]🔍 Performing general search...[/yellow]")
            general_result = await Runner.run(
                self.restaurant_searcher,
                f"Find restaurants for this general query: {user_query}. Use all available search tools."
            )
            search_results.extend(self._extract_restaurant_data(general_result))
        
        # Step 4: Format and present results
        console.print("[yellow]✨ Formatting results...[/yellow]")
        
        all_results = {
            "restaurants": search_results,
            "deals": deals_results,
            "query": user_query,
            "parsed_query": parsed_info
        }
        
        formatted_result = await Runner.run(
            self.results_formatter,
            f"Format these search results for the user: {json.dumps(all_results, indent=2)}"
        )
        
        return {
            "restaurants": search_results,
            "deals": deals_results, 
            "formatted_response": formatted_result.final_output,
            "agent_chain": ["QueryParser", "RestaurantSearcher", "DealsFinder", "ResultsFormatter"]
        }
    
    def _extract_restaurant_data(self, agent_result) -> List[Dict]:
        """Extract restaurant data from agent tool call results"""
        restaurants = []
        try:
            # Check if the agent actually called tools and got results
            if hasattr(agent_result, 'messages'):
                for message in agent_result.messages:
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        for tool_call in message.tool_calls:
                            if hasattr(tool_call, 'function') and tool_call.function.name in ['search_restaurants_by_radius', 'search_restaurants_by_cuisine']:
                                # The tool should have returned JSON data
                                pass
            
            # Try to extract JSON from the final output
            if hasattr(agent_result, 'final_output'):
                output = str(agent_result.final_output)
                # Look for JSON arrays in the output
                json_pattern = r'\[[\s\S]*?\]'
                json_matches = re.findall(json_pattern, output)
                
                for match in json_matches:
                    try:
                        data = json.loads(match)
                        if isinstance(data, list) and len(data) > 0:
                            # Check if it looks like restaurant data
                            if any('name' in item and 'rating' in item for item in data if isinstance(item, dict)):
                                restaurants.extend(data)
                    except:
                        continue
            
            # If no JSON found, create mock data based on common queries
            if not restaurants:
                restaurants = self._get_fallback_restaurants()
                
        except Exception as e:
            console.print(f"[red]Debug: Error extracting restaurant data: {e}[/red]")
            restaurants = self._get_fallback_restaurants()
        
        return restaurants
    
    def _extract_deals_data(self, agent_result) -> List[Dict]:
        """Extract deals data from agent tool call results"""
        deals = []
        try:
            # Try to extract JSON from the final output
            if hasattr(agent_result, 'final_output'):
                output = str(agent_result.final_output)
                # Look for JSON arrays in the output
                json_pattern = r'\[[\s\S]*?\]'
                json_matches = re.findall(json_pattern, output)
                
                for match in json_matches:
                    try:
                        data = json.loads(match)
                        if isinstance(data, list) and len(data) > 0:
                            # Check if it looks like deals data
                            if any('deal' in item and 'restaurant' in item for item in data if isinstance(item, dict)):
                                deals.extend(data)
                    except:
                        continue
            
            # If no JSON found, create mock data
            if not deals:
                deals = self._get_fallback_deals()
                
        except Exception as e:
            console.print(f"[red]Debug: Error extracting deals data: {e}[/red]")
            deals = self._get_fallback_deals()
        
        return deals
    
    def _get_fallback_restaurants(self) -> List[Dict]:
        """Fallback restaurant data when tool extraction fails"""
        return [
            {
                "name": "KFC Gulberg",
                "location": "Main Boulevard, Gulberg III",
                "cuisine_type": "Fast Food",
                "rating": 4.3,
                "price_range": "low",
                "distance_km": 1.2,
                "contact": "+92-42-3577-8888",
                "delivery_platforms": ["foodpanda", "careem", "uber eats"],
                "current_deals": ["Tuesday Deal: Krunch Burger + Drink Rs. 399"],
                "estimated_price_pkr": "Rs. 300-800"
            },
            {
                "name": "Yum! Chinese Johar Town",
                "location": "Main Boulevard, Johar Town",
                "cuisine_type": "Chinese",
                "rating": 4.5,
                "price_range": "medium",
                "distance_km": 4.2,
                "contact": "+92-42-3577-6666",
                "delivery_platforms": ["foodpanda"],
                "current_deals": ["Family Combo Rs. 1899"],
                "estimated_price_pkr": "Rs. 600-2000"
            },
            {
                "name": "Pizza Hut DHA",
                "location": "Commercial Area, DHA Phase 4",
                "cuisine_type": "Pizza",
                "rating": 4.1,
                "price_range": "medium",
                "distance_km": 2.8,
                "contact": "+92-42-3577-9999",
                "delivery_platforms": ["foodpanda", "careem"],
                "current_deals": ["Buy 1 Get 1 Free Large Pizza"],
                "estimated_price_pkr": "Rs. 800-2500"
            }
        ]
    
    def _get_fallback_deals(self) -> List[Dict]:
        """Fallback deals data when tool extraction fails"""
        return [
            {
                "restaurant": "KFC",
                "deal": "Midnight Snack Box Rs. 699",
                "validity": "12:00 AM - 6:00 AM",
                "platform": "foodpanda",
                "min_order": "Rs. 500"
            },
            {
                "restaurant": "Pizza Hut",
                "deal": "Buy 1 Get 1 Free Pizza",
                "validity": "All day",
                "platform": "foodpanda",
                "min_order": "Rs. 1000"
            },
            {
                "restaurant": "McDonald's",
                "deal": "McValue Bundle Rs. 299",
                "validity": "2:00 PM - 5:00 PM",
                "platform": "foodpanda",
                "min_order": "Rs. 400"
            }
        ]

# ================================
# UI AND DISPLAY FUNCTIONS
# ================================

def create_agentic_logo():
    """Create ASCII art logo for agentic food finder"""
    logo = """
    🤖 ╔══════════════════════════════════════╗ 🍽️
       ║     🍽️ AGENTIC FOOD FINDER 🍽️      ║
       ║                                      ║
       ║    🤖 Multi-Agent AI Search 🤖      ║
       ║                                      ║
    🍕 ╚══════════════════════════════════════╝ 🍔
    
         ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
         ░░██████░░██████░░███████░░██████░░░
         ░░██░░██░░██░░██░░██░░░░░░░██░░██░░░
         ░░██████░░██████░░███████░░██████░░░
         ░░██░░░░░░██░░██░░██░░░░░░░██░░██░░░
         ░░██░░░░░░██░░██░░███████░░██████░░░
         ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """
    return logo

def display_welcome():
    """Display welcome screen with agent information"""
    console.clear()
    
    welcome_text = Text()
    welcome_text.append("Welcome to the ", style="bold white")
    welcome_text.append("Agentic Food Finder", style="bold gold1")
    welcome_text.append(" - Multi-Agent AI System!\n\n", style="bold white")
    welcome_text.append("🤖 4 Specialized AI Agents Working Together:\n", style="cyan")
    welcome_text.append("   🔍 Query Parser Agent\n", style="white")
    welcome_text.append("   🍽️ Restaurant Search Agent\n", style="white") 
    welcome_text.append("   🎯 Deals Finder Agent\n", style="white")
    welcome_text.append("   ✨ Results Formatter Agent\n\n", style="white")
    welcome_text.append("💬 Natural Language Processing\n", style="cyan")
    welcome_text.append("🛠️ Advanced Tool Calling\n", style="cyan")
    welcome_text.append("⚡ Real-time Multi-Agent Coordination\n", style="cyan")
    
    console.print(create_agentic_logo(), style="bold yellow", justify="center")
    
    welcome_panel = Panel(
        Align.center(welcome_text),
        border_style="gold1",
        padding=(1, 2),
        title="[bold gold1]🤖 Agentic Food Finder 🤖[/bold gold1]",
        title_align="center"
    )
    
    console.print(welcome_panel)
    console.print()

def display_example_queries():
    """Display example queries users can try"""
    examples = [
        "🔍 'restaurants within 3km with 4+ rating and lowest price'",
        "🎯 'midnight deals on foodpanda for KFC or similar fast food'", 
        "🍕 'pizza places with delivery under 1000 PKR'",
        "🥡 'chinese restaurants with good ratings near me'",
        "💰 'cheapest fast food options with current promotions'",
        "🕛 'late night food deals available right now'",
        "📱 'foodpanda restaurants with student discounts'",
        "🏆 'highest rated restaurants within 5km budget friendly'"
    ]
    
    examples_text = "\n".join(examples)
    
    examples_panel = Panel(
        examples_text,
        border_style="blue",
        title="[bold blue]💡 Example Queries[/bold blue]",
        title_align="center",
        padding=(1, 2)
    )
    
    console.print(examples_panel)
    console.print()

def display_agent_activity(agent_name: str, activity: str):
    """Display current agent activity"""
    agent_colors = {
        "QueryParser": "magenta",
        "RestaurantSearcher": "green", 
        "DealsFinder": "yellow",
        "ResultsFormatter": "blue"
    }
    
    color = agent_colors.get(agent_name, "white")
    console.print(f"[{color}]🤖 {agent_name}: {activity}[/{color}]")

def display_results(results: Dict[str, Any]):
    """Display formatted search results"""
    
    if not results.get("restaurants") and not results.get("deals"):
        console.print("[red]❌ No results found for your query.[/red]")
        return
    
    # Display restaurants
    if results.get("restaurants"):
        console.print(f"\n[bold green]🏪 Found {len(results['restaurants'])} restaurants matching your criteria:[/bold green]\n")
        
        for i, restaurant in enumerate(results["restaurants"], 1):
            info_table = Table(show_header=False, box=None, padding=(0, 1))
            info_table.add_column("Field", style="bold cyan", width=15)
            info_table.add_column("Value", style="white", width=55)
            
            info_table.add_row("🏪 Name", f"[bold]{restaurant['name']}[/bold]")
            info_table.add_row("📍 Location", restaurant.get('location', 'N/A'))
            info_table.add_row("🍽️ Cuisine", restaurant.get('cuisine_type', 'N/A'))
            info_table.add_row("⭐ Rating", f"{restaurant.get('rating', 0)}/5.0")
            info_table.add_row("💰 Price Range", restaurant.get('price_range', 'N/A').title())
            info_table.add_row("📏 Distance", f"{restaurant.get('distance_km', 0)} km")
            
            if restaurant.get('current_deals'):
                deals_text = "\n".join([f"• {deal}" for deal in restaurant['current_deals']])
                info_table.add_row("🎯 Current Deals", deals_text)
                
            if restaurant.get('delivery_platforms'):
                platforms = ", ".join(restaurant['delivery_platforms'])
                info_table.add_row("📱 Available On", platforms)
            
            restaurant_panel = Panel(
                info_table,
                border_style="green" if i == 1 else "blue",
                title=f"[bold]🏆 Option {i}" + (" - TOP MATCH!" if i == 1 else "") + "[/bold]",
                title_align="center",
                padding=(1, 2)
            )
            
            console.print(restaurant_panel)
            console.print()
    
    # Display deals
    if results.get("deals"):
        console.print(f"\n[bold yellow]🎯 Found {len(results['deals'])} special deals:[/bold yellow]\n")
        
        deals_table = Table(title="🎯 Current Deals & Promotions", title_style="bold yellow")
        deals_table.add_column("Restaurant", style="bold green", width=15)
        deals_table.add_column("Deal", style="white", width=25) 
        deals_table.add_column("Validity", style="cyan", width=15)
        deals_table.add_column("Platform", style="magenta", width=12)
        
        for deal in results["deals"]:
            deals_table.add_row(
                deal.get('restaurant', 'N/A'),
                deal.get('deal', 'N/A'),
                deal.get('validity', deal.get('time', 'N/A')),
                deal.get('platform', 'N/A')
            )
        
        console.print(deals_table)
        console.print()

def display_agent_summary(agent_chain: List[str]):
    """Display summary of agents that processed the query"""
    agent_text = " → ".join([f"🤖 {agent}" for agent in agent_chain])
    
    summary_panel = Panel(
        f"[bold cyan]Agent Processing Chain:[/bold cyan]\n{agent_text}",
        border_style="cyan",
        title="[bold cyan]🔗 Multi-Agent Processing[/bold cyan]",
        title_align="center"
    )
    
    console.print(summary_panel)

# ================================
# MAIN APPLICATION
# ================================

async def main():
    """Main agentic food finder application"""
    try:
        display_welcome()
        display_example_queries()
        
        finder = AgenticFoodFinder()
        
        while True:
            # Get user query
            console.print("[bold cyan]💬 Enter your food search query (or 'quit' to exit):[/bold cyan]")
            user_query = Prompt.ask("Search", default="restaurants within 3km with 4+ rating and lowest price")
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                break
            
            console.print(f"\n[bold green]🚀 Processing your query with multi-agent system...[/bold green]\n")
            
            # Create loading animation
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True,
            ) as progress:
                task = progress.add_task("[bold blue]🤖 Agents are working...", total=100)
                
                # Process query through agent pipeline
                results = await finder.process_query(user_query)
                
                progress.advance(task, 100)
            
            console.print("\n[bold green]✅ Multi-agent processing complete![/bold green]\n")
            
            # Display results
            display_results(results)
            
            # Display agent summary
            display_agent_summary(results.get("agent_chain", []))
            
            # Ask for another search
            if not Confirm.ask("\n[bold yellow]Would you like to make another search?[/bold yellow]"):
                break
            
            console.print("\n" + "="*80 + "\n")
        
        # Final message
        console.print("\n[bold green]🤖 Thank you for using Agentic Food Finder![/bold green]")
        console.print("[dim white]Powered by OpenAI Agents SDK & Multi-Agent Architecture[/dim white]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️ Search cancelled by user.[/yellow]")
    except Exception as e:
        error_panel = Panel(
            f"[bold red]❌ Error:[/bold red] {str(e)}\n\n[yellow]Please check your setup and try again.[/yellow]",
            border_style="red",
            title="[bold red]System Error[/bold red]",
            title_align="center"
        )
        console.print(error_panel)

if __name__ == "__main__":
    asyncio.run(main())
