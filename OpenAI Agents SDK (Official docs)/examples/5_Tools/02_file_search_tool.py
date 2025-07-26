from agents import Agent, Runner, RunConfig, FileSearchTool
from g_config import create_openai_config

# Initialize model and provider configurations
provider, model = create_openai_config()



# Define the run configuration
run_config = RunConfig(
    model="gpt-4-1106-preview",
    model_provider=provider,
    tracing_disabled=True
)

# Initialize the agent with the FileSearchTool
agent = Agent(
    name="Document Query Agent",
    instructions="You are an assistant that can retrieve and summarize information from uploaded documents.",
    tools=[
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["vs_6883d3b214d481918c8e4d5442cdcf3b"],  # Use the vector store ID created earlier
        ),
    ]
)


async def main():
    # Example query
    query = input("Enter your query: ")
    result = await Runner.run(agent, query)
    print(f"Result: {result.final_output}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
