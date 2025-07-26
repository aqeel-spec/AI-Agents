from g_config import create_gemini_config
from agents import (
    Agent,
    RunConfig,
    RunContextWrapper,
    Runner,
    RunHooks,      # For global lifecycle events
    AgentHooks     # For agent-specific lifecycle events
)
from dataclasses import dataclass
import time
from datetime import datetime

@dataclass
class UserContext:
    user_id: str
    name: str
    session_start: datetime = datetime.now()  # Initialize session start time

provider, model = create_gemini_config()

# ================================
# GLOBAL LIFECYCLE HOOKS (RunHooks)
# ================================

class GlobalLifecycleHooks(RunHooks[UserContext]):
    """Global hooks that apply to the entire agent run"""
    
    async def on_agent_start(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext]):
        """Called before ANY agent starts"""
        print(f"🌍 GLOBAL: Agent starting")
        print(f"   User: {context.context.name}")
        print(f"   Agent: {agent.name}")
        print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
        
        # Initialize session timing
        context.context.session_start = datetime.now()
    
    async def on_agent_end(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], output):
        """Called when ANY agent finishes"""
        if context.context.session_start:
            duration = datetime.now() - context.context.session_start
            print(f"🌍 GLOBAL: Agent completed")
            print(f"   User: {context.context.name}")
            print(f"   Duration: {duration.total_seconds():.2f} seconds")
        
    async def on_handoff(self, context: RunContextWrapper[UserContext], from_agent: Agent[UserContext], to_agent: Agent[UserContext]):
        """Called when one agent hands off to another"""
        print(f"🔄 GLOBAL: Handoff from {from_agent.name} to {to_agent.name}")
    
    async def on_tool_start(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], tool):
        """Called before ANY tool is used"""
        print(f"🔧 GLOBAL: Tool starting")
        print(f"   User: {context.context.name}")
        print(f"   Tool: {tool.name}")
    
    async def on_tool_end(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], tool, result: str):
        """Called after ANY tool completes"""
        print(f"📊 GLOBAL: Tool completed")
        print(f"   User: {context.context.name}")
        print(f"   Tool: {tool.name}")
        print(f"   Result preview: {result[:50]}...")

# ================================
# AGENT-SPECIFIC HOOKS (AgentHooks)
# ================================

class SpecificAgentHooks(AgentHooks[UserContext]):
    """Hooks specific to one particular agent"""
    
    async def on_start(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext]):
        """Called when THIS specific agent starts"""
        print(f"🎯 AGENT-SPECIFIC: {agent.name} is starting")
        print(f"   Handling request for: {context.context.name}")
    
    async def on_end(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], output):
        """Called when THIS specific agent ends"""
        print(f"🎯 AGENT-SPECIFIC: {agent.name} is finishing")
        print(f"   Final output length: {len(str(output))} characters")
    
    async def on_handoff(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], source: Agent[UserContext]):
        """Called when another agent hands off TO this agent"""
        print(f"🎯 AGENT-SPECIFIC: {agent.name} received handoff from {source.name}")
    
    async def on_tool_start(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], tool):
        """Called before THIS agent uses a tool"""
        print(f"🎯 AGENT-SPECIFIC: {agent.name} is about to use {tool.name}")
    
    async def on_tool_end(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], tool, result: str):
        """Called after THIS agent uses a tool"""
        print(f"🎯 AGENT-SPECIFIC: {agent.name} finished using {tool.name}")

# ================================
# AGENT DEFINITION
# ================================

def simple_instructions(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    return f"""
    You are a helpful assistant talking to {context.context.name}.
    Be friendly and provide clear answers.
    Keep responses concise but helpful.
    """

# Create agent with specific hooks
agent = Agent[UserContext](
    name="Lifecycle Demo Agent",
    instructions=simple_instructions,
    hooks=SpecificAgentHooks()  # Agent-specific hooks
)

# ================================
# TESTING FUNCTIONS
# ================================

async def test_with_global_hooks():
    """Test agent with global lifecycle hooks"""
    print("\n" + "="*60)
    print("TESTING WITH GLOBAL HOOKS")
    print("="*60)
    
    # Create global hooks instance
    global_hooks = GlobalLifecycleHooks()
    
    user_context = UserContext(
        user_id="USER001",
        name="Aqeel"
    )
    
    run_config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )
    
    prompt = "Hello! Can you help me understand what 5 + 3 equals?"
    
    result = await Runner.run(
        agent,
        prompt,
        context=user_context,
        run_config=run_config,
        hooks=global_hooks  # Pass global hooks to Runner
    )
    
    print(f"\n💬 Final Response: {result.final_output}")

async def test_with_both_hooks():
    """Test agent with both global and agent-specific hooks"""
    print("\n" + "="*60)
    print("TESTING WITH BOTH GLOBAL AND AGENT-SPECIFIC HOOKS")
    print("="*60)
    
    global_hooks = GlobalLifecycleHooks()
    
    user_context = UserContext(
        user_id="USER002",
        name="Sarah"
    )
    
    run_config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )
    
    prompt = "What's the current time and can you tell me a fun fact?"
    
    result = await Runner.run(
        agent,  # This agent already has agent-specific hooks
        prompt,
        context=user_context,
        run_config=run_config,
        hooks=global_hooks  # Also add global hooks
    )
    
    print(f"\n💬 Final Response: {result.final_output}")

async def test_multiple_users():
    """Test with multiple users to see lifecycle events"""
    print("\n" + "="*60)
    print("TESTING MULTIPLE USERS")
    print("="*60)
    
    global_hooks = GlobalLifecycleHooks()
    
    users = [
        UserContext(user_id="USER003", name="Alice"),
        UserContext(user_id="USER004", name="Bob"),
    ]
    
    run_config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )
    
    for i, user in enumerate(users):
        print(f"\n--- Request {i+1}: {user.name} ---")
        
        result = await Runner.run(
            agent,
            f"Hi, I'm {user.name}. Can you greet me?",
            context=user,
            run_config=run_config,
            hooks=global_hooks
        )
        
        print(f"Response: {result.final_output}")
        
        # Small delay to see timing
        import asyncio
        await asyncio.sleep(0.5)

# ================================
# CUSTOM ANALYTICS HOOKS EXAMPLE
# ================================

class AnalyticsHooks(RunHooks[UserContext]):
    """Example of using hooks for analytics"""
    
    def __init__(self):
        self.sessions = {}
        self.tool_usage = {}
    
    async def on_agent_start(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext]):
        """Track session start"""
        user_id = context.context.user_id
        self.sessions[user_id] = {
            'start_time': datetime.now(),
            'agent_name': agent.name,
            'user_name': context.context.name
        }
        print(f"📊 ANALYTICS: Started tracking session for {context.context.name}")
    
    async def on_agent_end(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], output):
        """Calculate and log session metrics"""
        user_id = context.context.user_id
        if user_id in self.sessions:
            session = self.sessions[user_id]
            duration = datetime.now() - session['start_time']
            
            print(f"📊 ANALYTICS: Session Summary")
            print(f"   User: {session['user_name']}")
            print(f"   Duration: {duration.total_seconds():.2f}s")
            print(f"   Response Length: {len(str(output))} chars")
    
    async def on_tool_start(self, context: RunContextWrapper[UserContext], agent: Agent[UserContext], tool):
        """Track tool usage"""
        tool_name = tool.name
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = 0
        self.tool_usage[tool_name] += 1
        
        print(f"📊 ANALYTICS: Tool {tool_name} used {self.tool_usage[tool_name]} times total")

async def test_analytics_hooks():
    """Test with analytics hooks"""
    print("\n" + "="*60)
    print("TESTING ANALYTICS HOOKS")
    print("="*60)
    
    analytics_hooks = AnalyticsHooks()
    
    user_context = UserContext(
        user_id="ANALYTICS_USER",
        name="Analytics Test User"
    )
    
    run_config = RunConfig(
        model=model,
        model_provider=provider,
        tracing_disabled=True,
    )
    
    result = await Runner.run(
        agent,
        "Can you help me with a simple calculation?",
        context=user_context,
        run_config=run_config,
        hooks=analytics_hooks
    )
    
    print(f"\n💬 Response: {result.final_output}")

# ================================
# MAIN EXECUTION
# ================================

if __name__ == "__main__":
    import asyncio
    
    async def run_all_tests():
        await test_with_global_hooks()
        await test_with_both_hooks()  
        await test_multiple_users()
        await test_analytics_hooks()
    
    asyncio.run(run_all_tests())