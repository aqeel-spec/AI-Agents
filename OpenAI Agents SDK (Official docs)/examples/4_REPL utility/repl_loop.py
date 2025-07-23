"""
REPL utility

The SDK provides run_demo_loop for quick interactive testing.

run_demo_loop prompts for user input in a loop, 
keeping the conversation history between turns. 
By default it streams model output as it is produced. 
Type quit or exit (or press Ctrl-D) to leave the loop.
"""

import asyncio
from agents import Agent, run_demo_loop, RunConfig
from g_config import create_openai_config, create_gemini_config

provider, model = create_gemini_config()

if not provider or not model:
    provider, model = create_openai_config()
    
run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.")
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())