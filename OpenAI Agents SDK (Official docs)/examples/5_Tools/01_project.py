"""
01_web_search_demo.py - Professional Coffee Shop Finder Demo

A demonstration of the sophisticated coffee shop recommendation system 
with beautiful rich text formatting and professional UI - without API calls.

This shows the complete user experience and interface design.
"""

from dataclasses import dataclass
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
import asyncio
import time

# Initialize rich console
console = Console()

# ================================
# DATA MODELS
# ================================

class CoffeeShop(BaseModel):
    """Professional coffee shop data model"""
    name: str
    location: str
    temperature: float  # Temperature in Celsius
    weather: str  # Weather condition
    price_range: str  # Price range (low, medium, high)
    rating: float = 4.5  # Default rating
    specialty: str = "Specialty Coffee"  # Coffee specialty
    atmosphere: str = "Cozy"  # Atmosphere description

    def __str__(self):
        return f"{self.name} at {self.location} ({self.temperature}°C, {self.weather}) - {self.price_range}"

# ================================
# UI AND DISPLAY FUNCTIONS
# ================================

def create_coffee_logo():
    """Create an ASCII art coffee logo"""
    logo = """
    ☕ ╔══════════════════════════════════════╗ ☕
       ║     ☕ ELITE COFFEE CONCIERGE ☕     ║
       ║                                      ║
       ║        🫘 Premium Recommendations 🫘  ║
       ║                                      ║
    ☕ ╚══════════════════════════════════════╝ ☕
    
         ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
         ░░██████░░██████░░███████░░███████░░░
         ░░██░░██░░██░░██░░██░░░░░░░██░░░░░░░░
         ░░██████░░██████░░███████░░███████░░░
         ░░██░░░░░░██░░██░░██░░░░░░░██░░░░░░░░
         ░░██░░░░░░██░░██░░██░░░░░░░███████░░░
         ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    """
    return logo

def create_loading_animation():
    """Create a professional loading animation"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("[bold blue]Brewing your perfect coffee recommendation...", total=100)
        
        steps = [
            "☕ Analyzing weather conditions...",
            "🔍 Searching nearby coffee shops...",
            "💰 Checking budget compatibility...",
            "🚴 Assessing transportation safety...",
            "⭐ Evaluating coffee quality...",
            "🎯 Finalizing recommendation..."
        ]
        
        for i, step in enumerate(steps):
            progress.update(task, description=f"[bold cyan]{step}")
            progress.advance(task, 16)
            time.sleep(0.8)

def display_welcome():
    """Display welcome screen with logo"""
    console.clear()
    
    # Create welcome panel
    welcome_text = Text()
    welcome_text.append("Welcome to the ", style="bold white")
    welcome_text.append("Elite Coffee Concierge", style="bold gold1")
    welcome_text.append(" Experience!\n\n", style="bold white")
    welcome_text.append("🌟 Your personal coffee advisor powered by AI\n", style="cyan")
    welcome_text.append("☔ Weather-aware recommendations\n", style="cyan")
    welcome_text.append("💰 Budget-conscious suggestions\n", style="cyan")
    welcome_text.append("🚴 Transportation safety considered\n", style="cyan")
    
    # Display logo
    console.print(create_coffee_logo(), style="bold yellow", justify="center")
    
    # Display welcome panel
    welcome_panel = Panel(
        Align.center(welcome_text),
        border_style="gold1",
        padding=(1, 2),
        title="[bold gold1]☕ Coffee Concierge ☕[/bold gold1]",
        title_align="center"
    )
    
    console.print(welcome_panel)
    console.print()

def display_recommendation(coffee_shop: CoffeeShop, query: str):
    """Display the coffee shop recommendation with rich formatting"""
    
    # Create main information table
    table = Table(title="☕ Your Perfect Coffee Match", title_style="bold gold1")
    table.add_column("Attribute", style="bold cyan", width=15)
    table.add_column("Details", style="white", width=40)
    
    # Add coffee shop details
    table.add_row("🏪 Name", f"[bold]{coffee_shop.name}[/bold]")
    table.add_row("📍 Location", coffee_shop.location)
    table.add_row("🌡️ Temperature", f"{coffee_shop.temperature}°C")
    table.add_row("🌤️ Weather", coffee_shop.weather)
    table.add_row("💰 Price Range", coffee_shop.price_range.title())
    table.add_row("⭐ Rating", f"{coffee_shop.rating}/5.0 ⭐⭐⭐⭐⭐")
    table.add_row("☕ Specialty", coffee_shop.specialty)
    table.add_row("🏠 Atmosphere", coffee_shop.atmosphere)
    
    # Create recommendation panel
    recommendation_text = Text()
    recommendation_text.append("🎯 ", style="bold yellow")
    recommendation_text.append("Perfect Match Found!", style="bold green")
    recommendation_text.append(f"\n\nBased on your query: ", style="white")
    recommendation_text.append(f'"{query}"', style="italic cyan")
    recommendation_text.append(f"\n\nWe've found the ideal coffee spot that matches your preferences for weather, budget, and transportation needs.", style="white")
    
    # Add safety recommendation
    safety_text = Text()
    safety_text.append("\n🚴 Transportation Safety: ", style="bold yellow")
    safety_text.append("This location offers covered parking and is easily accessible during rainy weather. ", style="white")
    safety_text.append("Safe for bike riders with proper rain gear!", style="green")
    
    recommendation_text.append_text(safety_text)
    
    # Display everything
    console.print("\n")
    console.print(table)
    console.print("\n")
    
    recommendation_panel = Panel(
        recommendation_text,
        border_style="green",
        padding=(1, 2),
        title="[bold green]🎯 Recommendation Summary[/bold green]",
        title_align="center"
    )
    
    console.print(recommendation_panel)

def display_additional_features():
    """Display additional features and benefits"""
    features_table = Table(title="🌟 Additional Features", title_style="bold blue")
    features_table.add_column("Feature", style="bold blue", width=20)
    features_table.add_column("Description", style="white", width=50)
    
    features_table.add_row(
        "🌦️ Weather Integration", 
        "Real-time weather data influences recommendations"
    )
    features_table.add_row(
        "💸 Budget Optimization", 
        "Find great coffee within your price range"
    )
    features_table.add_row(
        "🚗 Transport Safety", 
        "Considers your mode of transport and safety"
    )
    features_table.add_row(
        "⭐ Quality Ratings", 
        "Only recommends highly-rated establishments"
    )
    features_table.add_row(
        "🕐 Real-time Updates", 
        "Current hours, availability, and special offers"
    )
    features_table.add_row(
        "🎯 Personalized", 
        "Tailored to your specific preferences and needs"
    )
    
    console.print("\n")
    console.print(features_table)

def display_footer():
    """Display professional footer"""
    footer_text = Text()
    footer_text.append("\n☕ ", style="yellow")
    footer_text.append("Enjoy your coffee experience!", style="bold white")
    footer_text.append(" ☕\n", style="yellow")
    footer_text.append("Powered by Agentic Developer & Elite Coffee Concierge AI", style="dim white")
    
    footer_panel = Panel(
        Align.center(footer_text),
        border_style="dim white",
        padding=(0, 2)
    )
    
    console.print(footer_panel)

def display_demo_notice():
    """Display demo notice"""
    demo_text = Text()
    demo_text.append("🎭 DEMO MODE", style="bold magenta")
    demo_text.append("\nThis is a demonstration of the Elite Coffee Concierge interface.\n", style="white")
    demo_text.append("In production, this would connect to real weather APIs and coffee shop databases.", style="dim white")
    
    demo_panel = Panel(
        Align.center(demo_text),
        border_style="magenta",
        padding=(1, 2),
        title="[bold magenta]Demo Information[/bold magenta]",
        title_align="center"
    )
    
    console.print(demo_panel)
    console.print()

# ================================
# MAIN DEMO APPLICATION
# ================================

async def main():
    """Main demo application function with professional UI"""
    try:
        # Display welcome screen
        display_welcome()
        
        # Show demo notice
        display_demo_notice()
        
        # User query
        query = (
            "Which coffee shop should I go to, considering my preferences and the weather today in Lahore? "
            "My price budget is 500 PKR, and I cannot take risks to go on a bike in heavy rain."
        )
        
        # Show query in a panel
        query_panel = Panel(
            Text(query, style="italic white"),
            border_style="blue",
            title="[bold blue]📝 Your Request[/bold blue]",
            title_align="center",
            padding=(1, 2)
        )
        console.print(query_panel)
        console.print()
        
        # Show loading animation
        create_loading_animation()
        
        # Show AI processing message
        console.print("\n[bold green]🤖 AI Concierge is processing your request...[/bold green]\n")
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Create demo recommendation
        demo_recommendation = CoffeeShop(
            name="The Coffee Bean Co.",
            location="MM Alam Road, Gulberg III, Lahore",
            temperature=22.0,
            weather="Light Rain",
            price_range="medium",
            rating=4.7,
            specialty="Artisan Espresso & Indoor Seating",
            atmosphere="Warm & Cozy with Rain View"
        )
        
        # Display the recommendation
        display_recommendation(demo_recommendation, query)
        
        # Display additional features
        display_additional_features()
        
        # Display footer
        display_footer()
        
        # Show success message
        success_panel = Panel(
            Text("✅ Recommendation generated successfully!\nThis demo shows the complete user experience.", style="bold green"),
            border_style="green",
            title="[bold green]Demo Complete[/bold green]",
            title_align="center"
        )
        console.print("\n")
        console.print(success_panel)
        
    except Exception as e:
        # Error handling with rich formatting
        error_panel = Panel(
            f"[bold red]Error:[/bold red] {str(e)}\n\n[yellow]This is a demo application.[/yellow]",
            border_style="red",
            title="[bold red]❌ Error Occurred[/bold red]",
            title_align="center"
        )
        console.print(error_panel)

if __name__ == "__main__":
    asyncio.run(main())
