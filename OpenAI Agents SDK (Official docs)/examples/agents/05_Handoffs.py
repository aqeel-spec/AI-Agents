from agents import Agent, RunConfig, Runner, handoff
from g_config import create_gemini_config
from pydantic import BaseModel
from dataclasses import dataclass

# Initialize the model and provider using the Gemini configuration
provider, model = create_gemini_config()

# Define Pydantic models for structured responses
class BookingResponse(BaseModel):
    status: str
    booking_id: str
    message: str

class RefundResponse(BaseModel):
    status: str
    refund_id: str
    message: str

# Define a dataclass for user context
@dataclass
class UserContext:
    user_id: str
    is_pro_user: bool
    recent_activity: str
    


# Define the Booking and Refund agents with structured outputs
booking_agent = Agent(
    name="Booking Agent",
    instructions=(
        "Assist the user with booking-related inquiries. "
        "Provide booking information and handle booking requests."
    ),
    output_type=BookingResponse,
)

refund_agent = Agent(
    name="Refund Agent",
    instructions=(
        "Assist the user with refund-related inquiries. "
        "Provide refund information and process refund requests."
    ),
    output_type=RefundResponse,
)

# Define the Triage agent with handoffs
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "Assist the user with their questions. "
        "If the inquiry is about booking, delegate to the Booking Agent. "
        "If the inquiry is about refunds, delegate to the Refund Agent."
    ),
    handoffs=[
        handoff(booking_agent),
        handoff(refund_agent)
    ],
)

# Create the run configuration
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,  # Disable tracing for this example
)

# Function to run the agent with dummy data
async def test_agent_interaction():
    user_context = UserContext(user_id="12345", is_pro_user=True, recent_activity="Booking a flight")
    prompt = input("📝 Enter your prompt (e.g., 'How can I book a flight?'): ")
    print(f"💬 Running agent with prompt: {prompt}")
    result = await Runner.run(triage_agent, prompt, context=user_context, run_config=run_config)
    print(f"✅ Agent response: {result.final_output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_interaction())



# from agents import (
#     Agent,
#     RunConfig,
#     Runner,
#     handoff
# )

# from g_config import create_gemini_config
# from pydantic import BaseModel
# from dataclasses import dataclass

# # Initialize the model and provider using the Gemini configuration
# provider, model = create_gemini_config()


# class BookingResponse(BaseModel):
#     status: str
#     booking_id: str
#     message: str

# class RefundResponse(BaseModel):
#     status: str
#     refund_id: str
#     message: str


# @dataclass
# class UserContext:
#     user_id: str
#     is_pro_user: bool
#     recent_activity: str

# # Define the Booking and Refund agents
# booking_agent = Agent(
#     name="Booking Agent",
#     instructions=(
#         "Assist the user with booking-related inquiries. "
#         "Provide booking information and handle booking requests."
#     ),
#     output_type=BookingResponse,
# )

# refund_agent = Agent(
#     name="Refund Agent",
#     instructions=(
#         "Assist the user with refund-related inquiries. "
#         "Provide refund information and process refund requests."
#     ),
#     output_type=RefundResponse,
# )

# # Define the Triage agent with handoffs
# triage_agent = Agent(
#     name="Triage Agent",
#     instructions=(
#         "Assist the user with their questions. "
#         "If the inquiry is about booking, delegate to the Booking Agent. "
#         "If the inquiry is about refunds, delegate to the Refund Agent."
#     ),
#     handoffs=[
#         handoff(booking_agent),
#         handoff(refund_agent)
#     ],
# )

# # Create the run configuration
# run_config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True,  # Disable tracing for this example
# )

# # Function to run the agent
# async def test_agent_interaction():
#     user_context = UserContext(user_id="12345", is_pro_user=True, recent_activity="Booking a flight")
#     prompt = input("📝 Enter your prompt (e.g., 'How can I book a flight?'): ")
#     print(f"💬 Running agent with prompt: {prompt}")
#     result = await Runner.run(triage_agent, prompt, context=user_context, run_config=run_config)
#     print(f"✅ Agent response: {result.final_output}")


# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_agent_interaction())
