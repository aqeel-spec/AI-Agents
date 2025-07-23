from g_config import create_gemini_config, weather_api_key
from agents import Agent, RunConfig, RunContextWrapper, Runner
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserContext:
    user_id: str
    name: str
    is_pro_user: bool
    recent_activity: str
    preferred_language: str = "English"
    time_zone: str = "UTC"

provider, model = create_gemini_config()

def dynamic_instructions(
    context: RunContextWrapper[UserContext],
    agent: Agent[UserContext]
) -> str:
    user = context.context
    current_time = datetime.now().strftime("%H:%M")
    
    # Base instruction
    base_instruction = f"""
    You are assisting {user.name} (User ID: {user.user_id}).
    Current time: {current_time}
    
    User Profile:
    - Name: {user.name}
    - Account Type: {'Pro User' if user.is_pro_user else 'Free User'}
    - Recent Activity: {user.recent_activity}
    - Preferred Language: {user.preferred_language}
    """
    
    # Add personalized behavior based on user type
    if user.is_pro_user:
        base_instruction += """
        
        🌟 PRO USER INSTRUCTIONS:
        - Provide detailed, comprehensive answers
        - Offer advanced features and suggestions
        - Prioritize their requests
        - Mention pro-exclusive features when relevant
        """
    else:
        base_instruction += """
        
        📝 FREE USER INSTRUCTIONS:
        - Provide helpful but concise answers
        - Occasionally mention pro features that could help
        - Be encouraging about upgrading when appropriate
        """
    
    # Add context-specific instructions based on recent activity
    if "flight" in user.recent_activity.lower():
        base_instruction += """
        
        ✈️ TRAVEL CONTEXT:
        - Focus on travel-related assistance
        - Ask about destinations, dates, preferences
        - Suggest travel tips and requirements
        """
    elif "booking" in user.recent_activity.lower():
        base_instruction += """
        
        📅 BOOKING CONTEXT:
        - Help with reservation processes
        - Ask for specific requirements
        - Provide confirmation and next steps
        """
    
    base_instruction += f"""
    
    Always address the user as {user.name} and be helpful, friendly, and professional.
    """
    
    return base_instruction.strip()

# Create agent with dynamic instructions
agent = Agent[UserContext](
    name="Personalized Triage Agent",
    instructions=dynamic_instructions,
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

async def test_different_users():
    # Test with Pro User
    pro_user = UserContext(
        user_id="PRO001", 
        name="Aqeel Shahzad", 
        is_pro_user=True, 
        recent_activity="Booking a flight to Dubai",
        preferred_language="English"
    )
    
    # Test with Free User
    free_user = UserContext(
        user_id="FREE001", 
        name="Sarah Johnson", 
        is_pro_user=False, 
        recent_activity="Looking at hotel prices",
        preferred_language="English"
    )
    
    users = [pro_user, free_user]
    
    for user in users:
        print(f"\n{'='*50}")
        print(f"Testing with: {user.name} ({'Pro' if user.is_pro_user else 'Free'} User)")
        print(f"{'='*50}")
        
        prompt = input(f"📝 Enter prompt for {user.name}: ")
        
        result = await Runner.run(
            agent, 
            prompt, 
            context=user, 
            run_config=run_config
        )
        
        print(f"✅ Response for {user.name}: {result.final_output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_different_users())


# ==================================================================
#                SIMPLE EXAMPLE FOR DYNAMIC INSTRUCTIONS 👇👇👇
# ==================================================================

# from g_config import create_gemini_config, weather_api_key

# from agents import (
#     Agent,
#     RunConfig,
#     RunContextWrapper,
#     Runner
# )
# from dataclasses import dataclass


# # create user context from existing example
# @dataclass
# class UserContext:
#     user_id: str
#     name : str
#     is_pro_user: bool
#     recent_activity: str

# provider, model = create_gemini_config()

# def dynamic_instructions(
#     context : RunContextWrapper[UserContext],
#     agent : Agent[UserContext]
# ) -> str :
#     return f"The user's name is {context.context.name}. Help them with their questions"


# agent = Agent[UserContext](
#     name="Triage Agent",
#     instructions=dynamic_instructions,
# )

# # Create the run configuration
# run_config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True,  # Disable tracing for this example
# )


# # Function to run the agent with dummy data
# async def test_agent_interaction():
#     user_context = UserContext(user_id="12345", name="Aqeel Shahzad", is_pro_user=True, recent_activity="Booking a flight")
#     prompt = input("📝 Enter your prompt (e.g., 'How can I book a flight?'): ")
#     print(f"💬 Running agent with prompt: {prompt}")
#     result = await Runner.run(agent, prompt, context=user_context, run_config=run_config)
#     print(f"✅ Agent response: {result.final_output}")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_agent_interaction())
