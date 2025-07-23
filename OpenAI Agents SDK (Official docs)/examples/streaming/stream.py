import asyncio
from agents import Agent, Runner, RunConfig
from g_config import create_openai_config, create_gemini_config
from openai.types.responses import ResponseTextDeltaEvent


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

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    
    print("_"* 50)
    print("\n🤖 AI async streaming...\n")
    print("_"* 50)
    
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())