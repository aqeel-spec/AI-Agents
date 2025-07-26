"""
09_cloning_or_copying_agents.py - Agent Cloning Example

Agent cloning allows you to create variations of existing agents by copying
their configuration and modifying specific properties. This is useful for:

1. Creating different versions of the same agent with slight modifications
2. A/B testing different prompts or configurations
3. Creating specialized agents from a base template
4. Maintaining consistency while allowing customization

This example shows a real-world customer service scenario where we create
different agent variations from a base customer support agent.
"""

from agents import Agent, RunConfig, Runner, RunContextWrapper
from g_config import create_gemini_config
from pydantic import BaseModel
from dataclasses import dataclass
import asyncio

# Initialize configuration
provider, model = create_gemini_config()

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

@dataclass
class UserContext:
    user_id: str
    name: str
    tier: str  # "basic", "premium", "enterprise"

class CustomerResponse(BaseModel):
    message: str
    helpful: bool
    professional: bool

# ================================
# BASE CUSTOMER SUPPORT AGENT
# ================================

def base_customer_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    user = context.context
    return f"""
    You are a customer support representative for TechCorp.
    
    Customer Information:
    - Name: {user.name}
    - User ID: {user.user_id}
    - Service Tier: {user.tier.upper()}
    
    Your role:
    - Provide helpful and accurate information
    - Be professional and courteous
    - Solve customer problems efficiently
    - Follow company policies and procedures
    
    Keep responses clear, concise, and actionable.
    """

# Create the base customer support agent
base_agent = Agent[UserContext](
    name="Customer Support Agent",
    instructions=base_customer_instructions,
    output_type=CustomerResponse
)

# ================================
# CLONED AGENT VARIATIONS
# ================================

# 1. TECHNICAL SUPPORT SPECIALIST (cloned from base agent)
def technical_support_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    user = context.context
    return f"""
    You are a TECHNICAL SUPPORT SPECIALIST for TechCorp.
    
    Customer Information:
    - Name: {user.name}
    - User ID: {user.user_id}
    - Service Tier: {user.tier.upper()}
    
    Your expertise:
    - Deep technical knowledge of our products
    - Troubleshooting complex technical issues
    - Providing step-by-step technical solutions
    - Understanding system architectures and integrations
    
    Use technical terminology when appropriate, but explain complex concepts clearly.
    Always provide specific, actionable technical steps.
    """

technical_agent = base_agent.clone(
    name="Technical Support Specialist",
    instructions=technical_support_instructions
)

# 2. BILLING SUPPORT AGENT (cloned from base agent)
def billing_support_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    user = context.context
    return f"""
    You are a BILLING SUPPORT SPECIALIST for TechCorp.
    
    Customer Information:
    - Name: {user.name}
    - User ID: {user.user_id}
    - Service Tier: {user.tier.upper()}
    
    Your expertise:
    - Payment processing and billing cycles
    - Account upgrades and downgrades
    - Refund and credit policies
    - Subscription management
    - Invoice and receipt assistance
    
    Be empathetic about billing concerns and provide clear explanations of charges.
    Always verify customer identity before discussing account details.
    """

billing_agent = base_agent.clone(
    name="Billing Support Specialist", 
    instructions=billing_support_instructions
)

# 3. VIP CUSTOMER AGENT (cloned from base agent with enhanced service)
def vip_customer_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    user = context.context
    return f"""
    You are a VIP CUSTOMER SUCCESS MANAGER for TechCorp.
    
    VIP Customer Information:
    - Name: {user.name}
    - User ID: {user.user_id}
    - Service Tier: {user.tier.upper()} (VIP Treatment)
    
    Your premium service approach:
    - Provide white-glove, personalized service
    - Anticipate needs and offer proactive solutions
    - Escalate issues immediately if needed
    - Offer premium features and early access to new products
    - Maintain a warm, relationship-focused tone
    
    Go above and beyond to ensure complete satisfaction.
    Treat this customer as our most valued partner.
    """

vip_agent = base_agent.clone(
    name="VIP Customer Success Manager",
    instructions=vip_customer_instructions
)

# 4. SIMPLE CHAT AGENT (cloned with simplified responses)
def simple_chat_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    user = context.context
    return f"""
    You are a FRIENDLY CHAT ASSISTANT for TechCorp.
    
    Customer: {user.name} ({user.tier} tier)
    
    Your style:
    - Keep responses short and simple
    - Use friendly, casual language
    - Focus on quick, easy-to-understand answers
    - Ask clarifying questions if needed
    - Be warm and approachable
    
    Perfect for basic inquiries and general questions.
    """

simple_agent = base_agent.clone(
    name="Friendly Chat Assistant",
    instructions=simple_chat_instructions
)

# ================================
# TEST SCENARIOS
# ================================

async def test_base_agent():
    """Test the original base agent"""
    print("\n" + "="*60)
    print("🏢 TESTING BASE CUSTOMER SUPPORT AGENT")
    print("="*60)
    
    context = UserContext(
        user_id="USER001",
        name="John Smith", 
        tier="basic"
    )
    
    prompt = "I'm having trouble accessing my account dashboard."
    print(f"👤 Customer: {prompt}")
    
    result = await Runner.run(
        base_agent,
        prompt,
        context=context,
        run_config=run_config
    )
    
    print(f"🤖 {base_agent.name}: {result.final_output.message}")

async def test_technical_agent():
    """Test the technical support specialist (cloned agent)"""
    print("\n" + "="*60)
    print("🔧 TESTING TECHNICAL SUPPORT SPECIALIST (CLONED)")
    print("="*60)
    
    context = UserContext(
        user_id="USER002",
        name="Sarah Johnson",
        tier="premium"
    )
    
    prompt = "My API integration is returning 500 errors. How do I debug this?"
    print(f"👤 Customer: {prompt}")
    
    result = await Runner.run(
        technical_agent,
        prompt,
        context=context,
        run_config=run_config
    )
    
    print(f"🤖 {technical_agent.name}: {result.final_output.message}")

async def test_billing_agent():
    """Test the billing support specialist (cloned agent)"""
    print("\n" + "="*60)
    print("💳 TESTING BILLING SUPPORT SPECIALIST (CLONED)")
    print("="*60)
    
    context = UserContext(
        user_id="USER003",
        name="Mike Wilson",
        tier="basic"
    )
    
    prompt = "I was charged twice this month. Can you help me understand my bill?"
    print(f"👤 Customer: {prompt}")
    
    result = await Runner.run(
        billing_agent,
        prompt,
        context=context,
        run_config=run_config
    )
    
    print(f"🤖 {billing_agent.name}: {result.final_output.message}")

async def test_vip_agent():
    """Test the VIP customer success manager (cloned agent)"""
    print("\n" + "="*60)
    print("⭐ TESTING VIP CUSTOMER SUCCESS MANAGER (CLONED)")
    print("="*60)
    
    context = UserContext(
        user_id="USER004",
        name="Dr. Emily Chen",
        tier="enterprise"
    )
    
    prompt = "I'd like to discuss expanding our enterprise package."
    print(f"� VIP Customer: {prompt}")
    
    result = await Runner.run(
        vip_agent,
        prompt,
        context=context,
        run_config=run_config
    )
    
    print(f"🤖 {vip_agent.name}: {result.final_output.message}")

async def test_simple_agent():
    """Test the simple chat assistant (cloned agent)"""
    print("\n" + "="*60)
    print("💬 TESTING FRIENDLY CHAT ASSISTANT (CLONED)")
    print("="*60)
    
    context = UserContext(
        user_id="USER005",
        name="Alex",
        tier="basic"
    )
    
    prompt = "What are your support hours?"
    print(f"👤 Customer: {prompt}")
    
    result = await Runner.run(
        simple_agent,
        prompt,
        context=context,
        run_config=run_config
    )
    
    print(f"🤖 {simple_agent.name}: {result.final_output.message}")

async def demonstrate_agent_properties():
    """Show how cloned agents maintain and change properties"""
    print("\n" + "="*60)
    print("🔍 AGENT CLONING PROPERTIES COMPARISON")
    print("="*60)
    
    print(f"📋 Base Agent:")
    print(f"   Name: {base_agent.name}")
    print(f"   Instructions: Custom function")
    print(f"   Output Type: {base_agent.output_type}")
    
    print(f"\n📋 Technical Agent (Cloned):")
    print(f"   Name: {technical_agent.name}")
    print(f"   Instructions: Modified from base")
    print(f"   Output Type: {technical_agent.output_type} (inherited)")
    print(f"   Same base structure: ✅")
    
    print(f"\n📋 VIP Agent (Cloned):")
    print(f"   Name: {vip_agent.name}")
    print(f"   Instructions: Enhanced for VIP service")
    print(f"   Output Type: {vip_agent.output_type} (inherited)")
    print(f"   Same base structure: ✅")
    
    print(f"\n💡 Cloning Benefits:")
    print(f"   • Maintains all base agent properties")
    print(f"   • Allows selective customization")
    print(f"   • Ensures consistency across agent variations")
    print(f"   • Reduces code duplication")
    print(f"   • Easy to maintain and update")

# ================================
# MAIN EXECUTION
# ================================

async def main():
    """Run all agent cloning demonstrations"""
    print("🚀 AGENT CLONING DEMONSTRATION")
    print("This example shows how to create specialized agents from a base template")
    
    await demonstrate_agent_properties()
    await test_base_agent()
    await test_technical_agent()
    await test_billing_agent()
    await test_vip_agent()
    await test_simple_agent()
    
    print("\n" + "="*60)
    print("✅ AGENT CLONING DEMO COMPLETE!")
    print("="*60)
    print("Key Takeaways:")
    print("• Cloning creates new agents with shared base properties")
    print("• You can modify any property during cloning (name, instructions, etc.)")
    print("• Cloned agents inherit output types, guardrails, and other configurations")
    print("• Perfect for creating specialized variations of the same agent")
    print("• Helps maintain consistency while allowing customization")

if __name__ == "__main__":
    asyncio.run(main())