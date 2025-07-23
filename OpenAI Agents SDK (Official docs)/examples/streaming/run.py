import asyncio
from agents import Agent, Runner, RunConfig
from g_config import create_openai_config, create_gemini_config


provider, model = create_openai_config()

if not provider or not model:
    provider, model = create_gemini_config()

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    result = await Runner.run(agent, input="Please tell me 5 jokes.")
    print("_"* 50)
    print("\n🤖 AI Run async...\n")
    print("_"* 50)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())