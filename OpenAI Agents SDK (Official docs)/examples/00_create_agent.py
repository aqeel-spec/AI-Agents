from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

# result = await Runner.run(agent, "What is the capital of France?")
# print(result.final_output)  # Expected output: "Paris"
async def main():
    result = await Runner.run(agent, "What is the capital of France?")
    print(result.final_output)

    
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())