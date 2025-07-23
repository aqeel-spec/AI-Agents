from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    RunConfig
)

from g_config import create_gemini_config

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,
    )


provider, model = create_gemini_config()

# Create the run configuration
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,  # Disable tracing for this example
)

agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    # This should trip the guardrail
    try:
        prompt = "Hello, can you help me solve for x: 2x + 3 = 11?"
        result = await Runner.run(agent, prompt, run_config=run_config)
        print("Guardrail didn't trip - this is unexpected")
        print(f"✅ Agent response: {result.final_output}")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
        
#     result = await Runner.run(triage_agent, prompt, context=user_context, run_config=run_config)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
