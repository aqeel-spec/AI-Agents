
## Tools

Tools let agents take actions—such as fetching data, executing code, calling external APIs, and even controlling a computer. In the Agent SDK, there are three categories of tools:

1. **Hosted tools**: These tools run on LLM servers alongside the AI models. OpenAI provides several built-in options.
2. **Function tools**: Any Python function can be exposed as a tool, complete with automatic schema validation.
3. **Agents as tools**: Allows one agent to call another agent as if it were a tool.


### Hosted tools 🛠

OpenAI offers several pre-built tools when using the `OpenAIResponsesModel` ([openai.github.io][1]):

* **WebSearchTool** – lets agents search the web.
* **FileSearchTool** – enables agents to retrieve information from your OpenAI Vector Stores.
* **ComputerTool** – allows agents to automate tasks on your computer.
* **CodeInterpreterTool** – runs sandboxed code execution.
* **HostedMCPTool** – interacts with tools available via a remote MCP server.
* **ImageGenerationTool** – generates images from a textual prompt.
* **LocalShellTool** – runs shell commands on your local machine.

```python
from agents import Agent, Runner, WebSearchTool, FileSearchTool

agent = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)

async def main():
    result = await Runner.run(agent, "Find me the top-rated coffee shops in SF and check their latest reviews.")
    print(result.final_output)
```


### Function tools

You can turn any Python function into a tool using the `@function_tool` decorator. The SDK automatically:

* Infers the function’s name and arguments.
* Generates a JSON schema from its signature.
* Extracts descriptions from docstrings.

```python
from agents import Agent, Runner, function_tool

@function_tool
async def fetch_weather(city: str) -> str:
    """Returns current weather for a specified city."""
    # Replace with a real API call
    return "Sunny and 24°C"

agent = Agent(
    name="WeatherBot",
    tools=[fetch_weather],
)

# Usage remains the same via Runner.run(...)
```


### Agents as tools

You can treat agents themselves as tools, enabling multi-agent workflows where one agent leverages another’s capabilities without performing a full handoff. This allows for hierarchical or modular agent architectures ([openai.github.io][1], [datacamp.com][2]).


Let me know if you’d like examples or help integrating specific tools into your workflow!

[1]: https://openai.github.io/openai-agents-python/tools/?utm_source=chatgpt.com "Tools - OpenAI Agents SDK"
[2]: https://www.datacamp.com/tutorial/openai-agents-sdk-tutorial?utm_source=chatgpt.com "OpenAI Agents SDK Tutorial: Building AI Systems That Take Action"
