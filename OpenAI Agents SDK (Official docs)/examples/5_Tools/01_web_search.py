from agents import Agent, RunConfig, Runner, WebSearchTool, RunConfig, function_tool

from g_config import create_openai_config, create_gemini_config
from dataclasses import dataclass
from pydantic import BaseModel

provider, model = create_gemini_config()
if not provider or not model:
    provider, model = create_openai_config()


run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

class CoffeeShop(BaseModel):
    name: str
    location: str
    temperature: float  # Temperature in Celsius
    weather: str  # Weather condition
    price_range: str  # Price range (low, medium, high)

    def __str__(self):
        return f"{self.name} at {self.location} ({self.temperature}°C, {self.weather}) - {self.price_range}"

@dataclass
class BestLocation:
    temp: float  # Temperature in Celsius
    weather: str  # Weather condition
    location: str  # Location name
    shop: str  # Coffee shop name

    def price_range(self, price: str) -> str:
        """Return price range based on budget."""
        ranges = {
            "low": "100-200 PKR",
            "medium": "200-500 PKR",
            "high": "500+ PKR"
        }
        return ranges.get(price, "Unknown budget range")

    def get_best_location(self) -> str:
        """Generate a recommendation based on attributes."""
        return (
            f"The best coffee shop for you is {self.shop} located at {self.location} "
            f"with a temperature of {self.temp}°C and weather condition as {self.weather}. "
            f"You can expect to spend around {self.price_range('medium')} there."
        )


# agent = Agent(
#     name="Assistant",
#     tools=[
#         WebSearchTool(),
#         FileSearchTool(
#             max_num_results=3,
#             vector_store_ids=["VECTOR_STORE_ID"],
#         ),
#     ],
# )

# Initialize the agent with the WebSearchTool
agent = Agent(
    name="Coffee Shop Finder",
    instructions="You are a helpful assistant that recommends coffee shops based on weather conditions.",
    tools=[WebSearchTool()],
    output_type=CoffeeShop
)

# # Run the agent with a query
# result = Runner.run_sync(
#     agent,
#     "Current weather in Lahore",
# )
from rich.console import Console
from rich.text import Text
async def main():
    query = input("Enter your query for coffee shop recommendation: ")
    
     # Define the context for the agent
    context = {
        "preferences": {
            "budget": "medium",
            "transport": "bike",
            "weather": "rainy"
        },
        "location": "Lahore"
    }

    result = await Runner.run(agent, query,  context=context)
    final_result : CoffeeShop = result.final_output
    # Initialize the console for rich text formatting
    console = Console()

    # Print a separator line
    console.print("=" * 50, style="bold green")
    console.print("[bold magenta]☕ Coffee Shop Recommendation ☕[/bold magenta]")
    console.print("=" * 50, style="bold green")

    # Display the coffee shop details
    console.print(f"[bold]Name:[/bold] {final_result.name}")
    console.print(f"[bold]Location:[/bold] {final_result.location}")
    console.print(f"[bold]Temperature:[/bold] {final_result.temperature}°C")
    console.print(f"[bold]Weather:[/bold] {final_result.weather}")
    console.print(f"[bold]Price Range:[/bold] {final_result.price_range}")
    console.print("=" * 50, style="bold green")
    


# Print the final output
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
