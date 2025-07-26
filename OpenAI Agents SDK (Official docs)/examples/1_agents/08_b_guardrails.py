"""
08_guardrails.py - Beginner's Guide to Guardrails

Guardrails are safety checks that run alongside your agents to validate:
1. INPUT GUARDRAILS: User input before the agent processes it
2. OUTPUT GUARDRAILS: Agent output before returning to the user

Think of guardrails like security guards:
- Input guardrails check if the user's request is appropriate
- Output guardrails check if the agent's response is safe to send

This example shows practical guardrails for a customer support chatbot.
"""

from g_config import create_gemini_config
from agents import (
    Agent,
    RunConfig,
    RunContextWrapper,
    Runner,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    input_guardrail,
    output_guardrail,
    TResponseInputItem
)
from pydantic import BaseModel
from dataclasses import dataclass
import asyncio
import re

# Initialize configuration
provider, model = create_gemini_config()

@dataclass
class UserContext:
    user_id: str
    name: str
    is_premium: bool = False

# ================================
# PYDANTIC MODELS FOR STRUCTURED OUTPUT
# ================================

class PolicyViolationCheck(BaseModel):
    """Model for checking if input violates policies"""
    is_violation: bool
    violation_type: str  # e.g., "profanity", "inappropriate_request", "none"
    reasoning: str
    severity: str  # "low", "medium", "high"

class SafetyCheck(BaseModel):
    """Model for checking if output is safe"""
    is_safe: bool
    safety_issues: list[str]  # List of safety concerns if any
    reasoning: str

class CustomerSupportResponse(BaseModel):
    """Model for customer support agent responses"""
    response: str
    helpful: bool
    professional: bool

# ================================
# GUARDRAIL AGENTS
# ================================

# Agent to check input for policy violations
input_checker_agent = Agent(
    name="Input Policy Checker",
    instructions="""
    You are a content moderator for a customer support system.
    
    Check if the user's message violates any policies:
    - Profanity or offensive language
    - Inappropriate requests (asking for homework help, illegal activities)
    - Spam or irrelevant content
    - Requests outside of customer support scope
    
    Be helpful but firm in identifying violations.
    If the message is a normal customer support question, mark it as safe.
    """,
    output_type=PolicyViolationCheck
)

# Agent to check output for safety
output_checker_agent = Agent(
    name="Output Safety Checker", 
    instructions="""
    You are a safety reviewer for customer support responses.
    
    Check if the response:
    - Contains any inappropriate content
    - Provides accurate information (no hallucinations)
    - Is professional and helpful
    - Doesn't include any sensitive information
    
    Mark as unsafe if there are any concerns.
    """,
    output_type=SafetyCheck
)

# ================================
# INPUT GUARDRAILS
# ================================

@input_guardrail
async def policy_violation_guardrail(
    ctx: RunContextWrapper[UserContext], 
    agent: Agent, 
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """
    Check if user input violates our policies.
    This runs BEFORE the main agent processes the request.
    """
    print(f"🛡️  INPUT GUARDRAIL: Checking user input for policy violations...")
    
    # Convert input to string if it's a list
    input_text = input if isinstance(input, str) else str(input)
    
    # Run the policy check
    result = await Runner.run(
        input_checker_agent, 
        f"Please check this customer message: '{input_text}'",
        context=ctx.context
    )
    
    policy_check = result.final_output
    
    print(f"   Policy Check Result: {policy_check.violation_type}")
    print(f"   Reasoning: {policy_check.reasoning}")
    
    # Trigger tripwire if there's a violation
    tripwire_triggered = policy_check.is_violation
    
    if tripwire_triggered:
        print(f"   ⚠️  TRIPWIRE TRIGGERED: {policy_check.violation_type}")
    else:
        print(f"   ✅ Input passed policy check")
    
    return GuardrailFunctionOutput(
        output_info=policy_check,
        tripwire_triggered=tripwire_triggered
    )

@input_guardrail 
async def simple_profanity_guardrail(
    ctx: RunContextWrapper[UserContext],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """
    Simple profanity check using basic pattern matching.
    This is a fast, lightweight guardrail.
    """
    print(f"🛡️  INPUT GUARDRAIL: Quick profanity check...")
    
    input_text = input if isinstance(input, str) else str(input)
    
    # Simple profanity ( بے حرمتی ) detection (you'd use a proper library in production)
    profanity_words = ["badword1", "badword2", "damn", "hell"]  # Add real words as needed
    
    found_profanity = []
    for word in profanity_words:
        if word.lower() in input_text.lower():
            found_profanity.append(word)
    
    has_profanity = len(found_profanity) > 0
    
    if has_profanity:
        print(f"   ⚠️  PROFANITY DETECTED: {found_profanity}")
    else:
        print(f"   ✅ No profanity detected")
    
    return GuardrailFunctionOutput(
        output_info={"profanity_found": found_profanity},
        tripwire_triggered=has_profanity
    )

# ================================
# OUTPUT GUARDRAILS  
# ================================

@output_guardrail
async def safety_review_guardrail(
    ctx: RunContextWrapper[UserContext],
    agent: Agent, 
    output: CustomerSupportResponse
) -> GuardrailFunctionOutput:
    """
    Check if the agent's response is safe to send to the user.
    This runs AFTER the main agent generates a response.
    """
    print(f"🛡️  OUTPUT GUARDRAIL: Safety reviewing agent response...")
    
    # Run safety check on the response
    result = await Runner.run(
        output_checker_agent,
        f"Please review this customer support response: '{output.response}'",
        context=ctx.context
    )
    
    safety_check = result.final_output
    
    print(f"   Safety Check: {'SAFE' if safety_check.is_safe else 'UNSAFE'}")
    print(f"   Reasoning: {safety_check.reasoning}")
    
    if not safety_check.is_safe:
        print(f"   ⚠️  SAFETY ISSUES: {safety_check.safety_issues}")
        print(f"   ⚠️  TRIPWIRE TRIGGERED: Unsafe response blocked")
    else:
        print(f"   ✅ Response passed safety check")
    
    return GuardrailFunctionOutput(
        output_info=safety_check,
        tripwire_triggered=not safety_check.is_safe
    )

@output_guardrail
async def response_quality_guardrail(
    ctx: RunContextWrapper[UserContext],
    agent: Agent,
    output: CustomerSupportResponse  
) -> GuardrailFunctionOutput:
    """
    Check if the response meets quality standards.
    """
    print(f"🛡️  OUTPUT GUARDRAIL: Quality checking response...")
    
    # Simple quality checks
    response_text = output.response.strip()
    
    quality_issues = []
    
    # Check response length
    if len(response_text) < 10:
        quality_issues.append("Response too short")
    
    if len(response_text) > 1000:
        quality_issues.append("Response too long")
        
    # Check if response actually addresses customer needs
    if not output.helpful:
        quality_issues.append("Response marked as not helpful")
        
    if not output.professional:
        quality_issues.append("Response marked as unprofessional")
    
    # Check for placeholder text
    if "lorem ipsum" in response_text.lower() or "[placeholder]" in response_text.lower():
        quality_issues.append("Response contains placeholder text")
    
    has_quality_issues = len(quality_issues) > 0
    
    if has_quality_issues:
        print(f"   ⚠️  QUALITY ISSUES: {quality_issues}")
        print(f"   ⚠️  TRIPWIRE TRIGGERED: Low quality response blocked")
    else:
        print(f"   ✅ Response passed quality check")
    
    return GuardrailFunctionOutput(
        output_info={"quality_issues": quality_issues},
        tripwire_triggered=has_quality_issues
    )

# ================================
# MAIN CUSTOMER SUPPORT AGENT
# ================================

def customer_support_instructions(context: RunContextWrapper[UserContext], agent: Agent) -> str:
    user = context.context
    return f"""
    You are a helpful customer support agent for TechCorp.
    
    Customer Info:
    - Name: {user.name}
    - Account Type: {'Premium' if user.is_premium else 'Standard'}
    
    Guidelines:
    - Be professional, helpful, and friendly
    - Provide accurate information about our products/services
    - If you don't know something, admit it and offer to find out
    - Keep responses concise but thorough
    - Always aim to resolve the customer's issue
    
    Available services to help with:
    - Product information and troubleshooting
    - Account and billing questions  
    - Technical support
    - Return and refund policies
    """

# Create the main agent with both input and output guardrails
customer_support_agent = Agent[UserContext](
    name="Customer Support Agent",
    instructions=customer_support_instructions,
    output_type=CustomerSupportResponse,
    
    # Add input guardrails (run BEFORE agent processes input)
    input_guardrails=[
        policy_violation_guardrail,
        simple_profanity_guardrail
    ],
    
    # Add output guardrails (run AFTER agent generates response)
    output_guardrails=[
        safety_review_guardrail,
        response_quality_guardrail
    ]
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# ================================
# TEST SCENARIOS
# ================================

async def test_normal_interaction():
    """Test a normal customer support interaction"""
    print("\n" + "="*70)
    print("TEST 1: NORMAL CUSTOMER SUPPORT INTERACTION")
    print("="*70)
    
    user_context = UserContext(
        user_id="CUST001",
        name="Alice Johnson",
        is_premium=True
    )
    
    user_message = "Hi! I'm having trouble with my account login. Can you help me reset my password?"
    
    print(f"👤 User: {user_message}")
    
    try:
        result = await Runner.run(
            customer_support_agent,
            user_message,
            context=user_context,
            run_config=run_config
        )
        
        print(f"\n🤖 Agent Response: {result.final_output.response}")
        print(f"✅ SUCCESS: All guardrails passed!")
        
    except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
        print(f"\n❌ GUARDRAIL BLOCKED: {e}")

async def test_inappropriate_input():
    """Test what happens with inappropriate input"""
    print("\n" + "="*70)
    print("TEST 2: INAPPROPRIATE INPUT (Should be blocked)")
    print("="*70)
    
    user_context = UserContext(
        user_id="CUST002", 
        name="Bad Actor"
    )
    
    user_message = "Hey, can you help me with my math homework? What's 2+2?"
    
    print(f"👤 User: {user_message}")
    
    try:
        result = await Runner.run(
            customer_support_agent,
            user_message,
            context=user_context,
            run_config=run_config
        )
        
        print(f"\n🤖 Agent Response: {result.final_output.response}")
        print(f"⚠️  WARNING: Input should have been blocked!")
        
    except InputGuardrailTripwireTriggered as e:
        print(f"\n❌ INPUT BLOCKED BY GUARDRAIL: {e}")
        print("✅ SUCCESS: Inappropriate request was correctly blocked!")
        
    except OutputGuardrailTripwireTriggered as e:
        print(f"\n❌ OUTPUT BLOCKED BY GUARDRAIL: {e}")

async def test_profanity_input():
    """Test profanity detection"""
    print("\n" + "="*70)
    print("TEST 3: PROFANITY INPUT (Should be blocked)")
    print("="*70)
    
    user_context = UserContext(
        user_id="CUST003",
        name="Frustrated User"
    )
    
    user_message = "This damn service never works! Help me now!"
    
    print(f"👤 User: {user_message}")
    
    try:
        result = await Runner.run(
            customer_support_agent,
            user_message,
            context=user_context,
            run_config=run_config
        )
        
        print(f"\n🤖 Agent Response: {result.final_output.response}")
        print(f"⚠️  WARNING: Profanity should have been detected!")
        
    except InputGuardrailTripwireTriggered as e:
        print(f"\n❌ INPUT BLOCKED BY GUARDRAIL: {e}")
        print("✅ SUCCESS: Profanity was correctly detected and blocked!")
        
    except OutputGuardrailTripwireTriggered as e:
        print(f"\n❌ OUTPUT BLOCKED BY GUARDRAIL: {e}")

async def test_good_interaction():
    """Test another normal interaction"""
    print("\n" + "="*70)
    print("TEST 4: PREMIUM CUSTOMER INTERACTION")
    print("="*70)
    
    user_context = UserContext(
        user_id="CUST004",
        name="Premium Customer",
        is_premium=True
    )
    
    user_message = "I'm interested in upgrading my service plan. What options do you have?"
    
    print(f"👤 User: {user_message}")
    
    try:
        result = await Runner.run(
            customer_support_agent,
            user_message,
            context=user_context,
            run_config=run_config
        )
        
        print(f"\n🤖 Agent Response: {result.final_output.response}")
        print(f"✅ SUCCESS: All guardrails passed!")
        
    except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
        print(f"\n❌ GUARDRAIL BLOCKED: {e}")

# ================================
# UTILITY: SHOW GUARDRAIL INFO
# ================================

def show_guardrail_info():
    """Show information about the guardrails being used"""
    print("\n" + "="*70)
    print("GUARDRAILS CONFIGURATION")
    print("="*70)
    
    print("\n📥 INPUT GUARDRAILS (run before agent processes input):")
    print("   1. Policy Violation Check - Uses AI to detect inappropriate requests")
    print("   2. Simple Profanity Filter - Fast keyword-based filtering")
    
    print("\n📤 OUTPUT GUARDRAILS (run after agent generates response):")
    print("   1. Safety Review - Uses AI to check response safety")
    print("   2. Quality Check - Validates response meets quality standards")
    
    print("\n🎯 GUARDRAIL BENEFITS:")
    print("   • Prevent inappropriate usage")
    print("   • Ensure response quality and safety")
    print("   • Save costs by blocking bad requests early")
    print("   • Maintain professional standards")
    print("   • Protect against AI hallucinations")

# ================================
# MAIN EXECUTION
# ================================

if __name__ == "__main__":
    async def run_all_tests():
        show_guardrail_info()
        
        await test_normal_interaction()
        await test_inappropriate_input() 
        await test_profanity_input()
        await test_good_interaction()
        
        print(f"\n" + "="*70)
        print("GUARDRAILS DEMO COMPLETE!")
        print("="*70)
        print("Key Takeaways:")
        print("• Input guardrails filter user requests before processing")
        print("• Output guardrails validate responses before sending")
        print("• Guardrails can use simple rules OR AI-powered checking")
        print("• Multiple guardrails can work together")
        print("• Tripwires stop execution when violations are detected")
    
    asyncio.run(run_all_tests())
