from agents import (
    Agent, RunConfig,
    Runner,
    function_tool,
    RunContextWrapper
)

from dataclasses import dataclass
from g_config import create_gemini_config, weather_api_key
from pydantic import BaseModel

provider, model = create_gemini_config()

class Purchase(BaseModel):
    item: str
    price: float

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> list[Purchase]:
        # Simulate fetching user purchases
        return [
            Purchase(item="Laptop", price=1200.00),
            Purchase(item="Smartphone", price=800.00)
        ]

@function_tool
def get_user_id(context: RunContextWrapper[UserContext]) -> str:
    """Get the current user's unique identifier."""
    return context.context.uid

@function_tool
def get_pro_status(context: RunContextWrapper[UserContext]) -> str:
    """Check if the current user has pro subscription status."""
    return "Yes" if context.context.is_pro_user else "No"

@function_tool
async def get_user_purchases(context: RunContextWrapper[UserContext]) -> str:
    """Get the current user's recent purchases with item names and prices."""
    purchases = await context.context.fetch_purchases()
    purchase_list = []
    for purchase in purchases:
        purchase_list.append(f"{purchase.item}: ${purchase.price:.2f}")
    return "Recent purchases: " + ", ".join(purchase_list)

# Create the agent
agent = Agent[UserContext](
    name="Assistant",
    instructions="""You are a helpful assistant with access to user-specific data through function tools.
    
    When asked about user information, you should:
    1. Use get_user_id() to retrieve the user's ID
    2. Use get_pro_status() to check if the user is a pro user
    3. Use get_user_purchases() to get the user's recent purchases
    
    Always use these tools to provide accurate, up-to-date information.""",
    model=model,
    tools=[get_user_id, get_pro_status, get_user_purchases]
)

# Create the run configuration
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,  # Disable tracing for this example
)

# Function to run the agent
async def main():
    user_context = UserContext(uid="12345", is_pro_user=True)
    # prompt = """
    # Please retrieve and display the current user's information by using the available tools:
    
    # 1. Get the user ID
    # 2. Check the pro user status  
    # 3. Get the list of recent purchases with item names and prices
    
    # Format the response as a clear list.
    # """
    prompt = input("📝 Enter your prompt (e.g., 'Get user information'): ")
    print(f"💬 Running agent with prompt: {prompt}")
    result = await Runner.run(agent, prompt, context=user_context, run_config=run_config)
    print(f"✅ Agent response: {result.final_output}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
