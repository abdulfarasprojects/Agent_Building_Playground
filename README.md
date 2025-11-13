# Agent Building Playground

A comprehensive exploration of modern AI agent architectures, demonstrating multi-agent systems, tool integration, and safety workflows using different AI frameworks.

## 🎯 Project Overview

This playground showcases seven distinct AI agent implementations that demonstrate key concepts in agent development:

1. **Currency Conversion Agent** (Google ADK) - Financial calculations with multi-agent delegation
2. **Shipping Coordinator Agent** (Google ADK) - Long-running operations with human approval workflows
3. **Session Management Demo Agent** (Google ADK) - General chatbot with session management demonstration capabilities
4. **Database Session Demo Agent** (Google ADK) - General chatbot with persistent database sessions and compaction ⚠️ **NEEDS INVESTIGATION**
5. **Reactive Memory Agent** (Google ADK) - Chatbot with reactive memory loading using load_memory tool
6. **Proactive Memory Agent** (Google ADK) - Chatbot with proactive memory loading (preload before each turn)
7. **Cooking Assistant Agent** (Microsoft Agent Framework) - Recipe generation with safety workflows

All agents integrate **Model Context Protocol (MCP)** servers for extended tool capabilities and demonstrate production-ready patterns for AI agent development.

## 🏗️ Core Concepts Demonstrated

### Multi-Agent Architecture
Agents delegate specialized tasks to sub-agents for better accuracy and separation of concerns.

```python
# Google ADK: Currency agent delegates calculations to specialized calculation agent
calculation_agent = Agent(
    name="calculation_agent",
    model="gemini-2.0-flash",
    instruction="You are a calculation agent. When given amount, rate, and fee_percentage, write and execute Python code to calculate the total amount...",
    code_executor=BuiltInCodeExecutor(),
)

root_agent = Agent(
    name="currency_conversion_agent",
    model="gemini-2.0-flash",
    tools=[fees_percentage, get_conversion_rate, AgentTool(agent=calculation_agent)],
)
```

### Tool Integration & MCP Protocol
Both agents integrate external tools via synchronous wrappers around async MCP clients.

```python
# MCP Client for external tool integration
class MCPClient:
    async def call_tool(self, tool_name, **kwargs):
        await self.initialize()
        request = {
            "jsonrpc": "2.0", "id": 2,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": kwargs}
        }
        response = await self._send_request(request)
        return response.get("result", {})

# Synchronous wrapper for framework compatibility
def get_tiny_image() -> str:
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_get_tiny_image())
                return future.result(timeout=10)
        else:
            return loop.run_until_complete(mcp_get_tiny_image())
    except RuntimeError:
        return asyncio.run(mcp_get_tiny_image())
```

### Safety Workflows & User Confirmation
Cooking agent implements mandatory allergen checking before recipe generation.

```python
# Safety workflow in agent instructions
instructions="""
IMPORTANT WORKFLOW FOR RECIPE REQUESTS:
1. When a user asks for a recipe, FIRST use the check_allergens tool to analyze the dish name/ingredients for gluten and nuts
2. If allergens are detected (gluten or nuts found), ask the user: "This recipe contains [list allergens]. Do you want me to proceed?"
3. Only proceed with recipe generation if the user explicitly agrees
4. If user declines, stop and offer alternatives or end the conversation
"""
```

### Code Execution for Accuracy
Currency agent uses Python code execution to ensure mathematical precision.

```python
# Agent delegates all calculations to code execution
instruction="You are a calculation agent. When given amount, rate, and fee_percentage, write and execute Python code to calculate the total amount after deducting fees... Do not perform calculations yourself; always write and execute Python code."
```

### Framework Comparison

| Aspect | Google ADK | Microsoft Agent Framework |
|--------|------------|---------------------------|
| **Model Support** | Gemini models | GitHub Models (Grok-3) |
| **Agent Creation** | Class-based with tools | ChatAgent with instructions |
| **Tool Integration** | Direct tool functions | Function-based tools |
| **Execution Model** | Built-in code executor | External tool calls |
| **Threading** | Async-first | Async with sync wrappers |

## 📁 Project Structure

```
Agent_Building_Playground/
├── Google ADK/                    # Google ADK Implementation
│   ├── agent.py                   # Currency conversion agent with MCP integration
│   ├── currency_agent/            # Alternative agent structure
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── shipping_agent/            # Shipping coordinator agent
│   │   ├── __init__.py
│   │   ├── agent.py               # Shipping agent with approval workflow
│   │   ├── config.yaml            # Agent configuration
│   │   └── README.md              # Shipping agent documentation
│   ├── session_demo_agent/        # Session management demo
│   │   ├── __init__.py
│   │   ├── agent.py               # InMemorySessionService demonstration
│   │   └── README.md              # Session management documentation
│   ├── database_session_agent/    # Database session demo
│   │   ├── __init__.py
│   │   ├── agent.py               # DatabaseSessionService with compaction
│   │   ├── run_agent.py           # Custom runner for database persistence
│   │   ├── sessions.db            # SQLite database (created at runtime)
│   │   └── README.md              # Database session documentation
│   ├── memory_reactive_agent/     # Reactive memory loading demo
│   │   ├── __init__.py
│   │   ├── agent.py               # Reactive memory agent with load_memory tool
│   │   ├── run_agent.py           # Runner demonstrating three-step memory process
│   │   └── README.md              # Reactive memory documentation
│   └── memory_proactive_agent/    # Proactive memory loading demo
│       ├── __init__.py
│       ├── agent.py               # Proactive memory agent with preload_memory
│       ├── run_agent.py           # Runner with automatic memory preloading
│       └── README.md              # Proactive memory documentation
├── MS Agent Framework/            # Microsoft Agent Framework Implementation
│   ├── cooking_agent.py          # Cooking assistant with safety workflows
│   ├── ui.py                     # Web UI for the cooking agent
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Environment variables
│   ├── .gitignore               # Git ignore rules
│   └── README.md                 # Agent-specific documentation
└── README.md                     # This project-level README
```

## 🚀 Agent Implementations

### 1. Currency Conversion Agent (Google ADK)

**Purpose**: Accurate currency conversion with fee calculation and multi-agent delegation.

**Key Features**:
- Fee calculation based on card type (Visa: 2%, Mastercard: 2.5%, Amex: 3%)
- Real-time currency conversion rates
- Code execution for mathematical accuracy
- MCP integration for image generation
- Multi-agent architecture (root agent + calculation agent)

**Usage Example**:
```python
# Agent handles complex conversion logic
result = await agent.run(
    "Convert 1000 USD to EUR using a Visa card",
    thread=thread
)
# Returns: Total amount after fees and conversion
```

### 2. Shipping Coordinator Agent (Google ADK)

**Purpose**: Long-running shipping coordination with human approval workflows.

**Key Features**:
- Auto-approval for small orders (≤5 containers)
- Human approval required for large orders (>5 containers)
- ToolContext integration for confirmation requests
- Clear status updates and approval handling
- Demonstrates pause → wait → resume pattern

**Usage Example**:
```bash
cd "Google ADK"
adk run shipping_agent
```

**Example Interaction**:
```
User: Please coordinate shipping for 8 containers
Agent: [Requests confirmation: "Large shipping order detected: 8 containers. Do you approve this shipment?"]
User: approve
Agent: ✅ Approved shipping order for 8 containers. Order will be processed.
```

### 3. Session Management Demo Agent (Google ADK)

**Purpose**: General chatbot that demonstrates session management concepts with InMemorySessionService.

**Key Features**:
- General conversation capabilities on any topic
- Session management demonstration when requested
- Session as conversation notebook 📓 with events as entries 📝
- SessionService as storage layer 🗄️ and Runner as orchestration layer 🤖
- In-memory session storage (data lost on restart)
- Tools to display current session information and explain concepts

**Usage Example**:
```bash
cd "Google ADK"
adk web "Google ADK"  # Access via web UI
# or
adk run session_demo_agent
```

**Example Interactions**:
```
User: What's the weather like today?
Agent: I don't have access to real-time weather data, but I can help you with general information...

User: Show me how sessions work
Agent: Sessions in Google ADK are like conversation notebooks 📓 that store your chat history...
```

### 4. Database Session Demo Agent (Google ADK)

**Purpose**: General chatbot that demonstrates persistent sessions with DatabaseSessionService and event compaction.

**Key Features**:
- General conversation capabilities on any topic
- Database session demonstration with compaction when requested
- SQLite database persistence (survives restarts) ⚠️ **NEEDS INVESTIGATION**
- Event compaction with sliding window compression
- Database inspection capabilities
- Tools to display session data, compaction status, and explain concepts

**Usage Example**:
```bash
cd "Google ADK"
adk web "Google ADK"  # Access via web UI
# or
adk run database_session_agent
```

**Database Note**: The `sessions.db` file is automatically created when running the database agent. It persists all conversation sessions and can be inspected with SQLite tools.

**Status**: ⚠️ **Database persistence infrastructure is implemented but not working properly - needs investigation**

**Known Issues**: The database agent creates the SQLite database file and session tables correctly, but the agent may fail to respond properly when interacting through the web interface or direct runner. The underlying DatabaseSessionService and compaction features are implemented, but the agent execution may encounter errors during LLM API calls or message processing.

**Example Interactions**:
```
User: Tell me about machine learning
Agent: Machine learning is a subset of AI that enables systems to learn from data...

User: How does compaction work?
Agent: Event compaction manages memory by compressing old conversation events...
```

### 5. Reactive Memory Agent (Google ADK)

**Purpose**: General chatbot demonstrating reactive memory loading where the agent decides when to search memory.

**Current Status**: ⚠️ Demonstrates memory integration setup but actual reactive memory functionality is broken due to function calling issues. Agent gets stuck in loops calling manual_memory_search repeatedly.

**Key Features**:
- Reactive memory loading using `load_memory` tool (intended but not working)
- Agent decides when memory search is needed based on context (not implemented)
- Manual memory search capabilities (simulated, doesn't actually search memory)
- Google search integration for real-time information (working)
- InMemoryMemoryService with keyword-based search (integrated but not used)
- Comprehensive logging of memory operations (working)
- Three-step memory integration process (Initialize → Ingest → Retrieve) (partially working)

**Memory Process**:
1. **Initialize**: Create InMemoryMemoryService and provide to Runner
2. **Ingest**: Transfer session data to memory using `add_session_to_memory()`
3. **Retrieve**: Agent uses `load_memory` tool when it determines search is helpful

**Usage Example**:
```bash
cd "Google ADK/memory_reactive_agent"
python run_agent.py
```

**Example Interactions** (intended behavior - currently not working):
```
User: What did we talk about earlier?
Agent: [Intended: Uses load_memory tool to search conversation history]
Agent: [Currently: Gets stuck in function calling loop]

User: Search memory for "Python"
Agent: [Intended: Uses manual_memory_search tool]
Agent: [Currently: Calls manual_memory_search repeatedly without actual search]
```

### 6. Proactive Memory Agent (Google ADK)

**Purpose**: General chatbot demonstrating proactive memory loading where memory is preloaded before each turn.

**Current Status**: ⚠️ Demonstrates memory integration setup but actual proactive memory functionality is broken due to function calling issues. Agent gets stuck in loops calling manual_memory_search repeatedly.

**Key Features**:
- Proactive memory loading (memory preloaded before each conversation turn) (intended but not working)
- Agent has immediate access to relevant historical context (not implemented)
- Manual memory search capabilities (simulated, doesn't actually search memory)
- Google search integration for real-time information (working)
- InMemoryMemoryService with keyword-based search (integrated but not used)
- Comprehensive logging of memory operations (working)
- Automatic memory preloading before each agent response (not implemented)

**Memory Process**:
1. **Initialize**: Create InMemoryMemoryService and provide to Runner
2. **Ingest**: Transfer session data to memory using `add_session_to_memory()`
3. **Retrieve**: Memory automatically preloaded before each conversation turn

**Usage Example**:
```bash
cd "Google ADK/memory_proactive_agent"
python run_agent.py
```

**Example Interactions** (intended behavior - currently not working):
```
User: What did we talk about earlier?
Agent: [Intended: Memory already preloaded] Based on our conversation history...
Agent: [Currently: Gets stuck in function calling loop]

User: Search memory for "JavaScript"
Agent: [Intended: Uses manual_memory_search tool]
Agent: [Currently: Calls manual_memory_search repeatedly without actual search]
```

**Key Difference** (intended vs current): Reactive agent should search memory when it decides it's needed, while proactive agent should always have memory loaded before responding. Currently both agents exhibit the same broken behavior.

### 7. Cooking Assistant Agent (Microsoft Agent Framework)

**Purpose**: Safe recipe generation with allergen awareness and nutritional information.

**Key Features**:
- Mandatory allergen checking (gluten, nuts) before recipe generation
- Calorie calculation per serving
- Ingredient price lookup
- MCP tools integration (echo, math, LLM sampling, etc.)
- Safety confirmation workflow
- Interactive console and web UI

**Safety Workflow**:
1. User requests recipe → Agent checks for allergens
2. If allergens found → Ask user confirmation
3. User approves → Generate recipe
4. Include nutritional info and pricing

## 🛠️ Technical Implementation Details

### MCP (Model Context Protocol) Integration

Both agents demonstrate MCP server integration for extended capabilities:

```python
# Starting MCP everything server
self.process = await asyncio.create_subprocess_exec(
    'npx', '-y', '@modelcontextprotocol/server-everything',
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
```

**Available MCP Tools**:
- `echo` - Message echoing
- `add` - Mathematical addition
- `longRunningOperation` - Progress tracking
- `printEnv` - Environment inspection
- `sampleLLM` - LLM response generation
- `getTinyImage` - Test image generation
- `listRoots` - MCP server roots

### Async/Sync Bridge Pattern

Since MCP is async but frameworks may expect sync tools, both implementations use the bridge pattern:

```python
def sync_wrapper(async_func):
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Use ThreadPoolExecutor for running loop
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                    return future.result()
            else:
                return loop.run_until_complete(async_func(*args, **kwargs))
        except RuntimeError:
            # No loop, create new one
            return asyncio.run(async_func(*args, **kwargs))
    return wrapper
```

## 🎯 Learning Outcomes

This playground demonstrates:

1. **Agent Design Patterns**: Multi-agent delegation, tool integration, safety workflows, approval workflows
2. **Session Management**: In-memory and persistent session storage, event compaction, context management, real-time session inspection
3. **Memory Integration**: Reactive vs proactive memory loading (partially implemented ⚠️), InMemoryMemoryService, three-step memory process (Initialize → Ingest → Retrieve), keyword-based search
4. **Database Persistence**: SQLite-based session storage with automatic compaction and inspection capabilities ⚠️ **NEEDS INVESTIGATION**
5. **General Chatbot Development**: Building versatile agents that handle multiple conversation types
6. **Framework Comparison**: Google ADK vs Microsoft Agent Framework approaches
7. **Protocol Integration**: MCP for extending agent capabilities
8. **Safety Implementation**: Mandatory user confirmation for sensitive operations
9. **Long-running Operations**: Pause and resume patterns with human input
10. **Code Execution**: Using Python execution for mathematical accuracy
11. **Async Programming**: Bridging async tools with sync frameworks
12. **Model Selection**: Choosing appropriate models for different tasks
13. **Dynamic Agent Behavior**: Switching between general chat and specialized demonstrations

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Agent_Building_Playground
   python -m venv .venv
   source .venv/bin/activate
   pip install google-adk
   ```

2. **Set API keys**:
   ```bash
   export GOOGLE_API_KEY=your_google_ai_key
   export GITHUB_TOKEN=your_github_token
   ```

3. **Run all Google ADK agents**:
   ```bash
   adk web "Google ADK"
   ```
   Access at http://127.0.0.1:8000 - All agents including memory agents are now available in the web interface
   **⚠️ Note**: Memory agents have function calling issues and do not work as expected

   **Note**: Database Session Demo Agent is currently not working properly and needs investigation.

## 🏃 Running Individual Agents

##### Shipping Coordinator (Google ADK)
```bash
cd "Google ADK"
adk run shipping_agent
```

##### Currency Agent (Google ADK)
```bash
cd "Google ADK"
# Configure Google ADK credentials
python agent.py
```

##### Session Management Demo (Google ADK)
```bash
cd "Google ADK"
adk web "Google ADK"  # Select from web UI dropdown
# OR
adk run session_demo_agent
```

##### Database Session Demo (Google ADK)
```bash
cd "Google ADK"
adk web "Google ADK"  # Select from web UI dropdown
# OR for full persistence features:
cd "Google ADK/database_session_agent"
python run_agent.py
```
   **Note**: ⚠️ Currently not working properly - needs investigation. Requires Google AI API key. Set `GOOGLE_API_KEY` environment variable.

   **Note**: ⚠️ Memory agents have function calling issues and do not demonstrate proper memory functionality. They show the integration setup but get stuck in loops and don't actually retrieve or use memory.##### Reactive Memory Agent (Google ADK)
```bash
cd "Google ADK/memory_reactive_agent"
python run_agent.py
# OR via ADK Web UI at http://127.0.0.1:8000
```
**⚠️ CURRENT STATUS: NOT WORKING AS EXPECTED**
- **Issues**: Function calling loops, no actual memory retrieval, agent gets stuck repeatedly calling manual_memory_search
- **Features**: Reactive memory loading (intended), manual search, simulated Google search integration, comprehensive logging
- **Requirements**: Set `GOOGLE_API_KEY` environment variable
- **Note**: Agent demonstrates memory integration setup but actual memory functionality is broken due to function calling issues

##### Proactive Memory Agent (Google ADK)
```bash
cd "Google ADK/memory_proactive_agent"
python run_agent.py
# OR via ADK Web UI at http://127.0.0.1:8000
```
**⚠️ CURRENT STATUS: NOT WORKING AS EXPECTED**
- **Issues**: Function calling loops, no actual memory retrieval, agent gets stuck repeatedly calling manual_memory_search
- **Features**: Proactive memory loading (intended), manual search, simulated Google search integration, automatic preloading
- **Requirements**: Set `GOOGLE_API_KEY` environment variable
- **Note**: Agent demonstrates memory integration setup but actual memory functionality is broken due to function calling issues

##### Cooking Assistant (MS Agent Framework)
```bash
cd "MS Agent Framework"
# Install dependencies
pip install -r requirements.txt
# Set up GitHub token
export GITHUB_TOKEN=your_github_token
# Run the agent
python cooking_agent.py
# Or run with web UI
python ui.py
```

## � Known Issues & Future Improvements

### Memory Agents Issues
The memory agents currently demonstrate the integration setup but have several critical issues:

1. **Function Calling Loops**: Agents get stuck repeatedly calling the same tools due to Google ADK function calling compatibility issues
2. **No Actual Memory Retrieval**: The `manual_memory_search` function returns static messages instead of actually querying the InMemoryMemoryService
3. **Missing Reactive/Proactive Logic**: Both agents behave identically - neither implements the intended reactive vs proactive memory loading patterns
4. **Memory Service Not Used**: The integrated InMemoryMemoryService is not actually utilized for memory operations

### Required Fixes
To make these agents work properly:

1. **Implement Actual Memory Search**: Replace simulated memory functions with real calls to `memory_service.search_memory()`
2. **Fix Function Calling**: Resolve Google ADK function calling issues or implement alternative tool integration
3. **Reactive Agent**: Implement logic for agent to decide when memory search is needed
4. **Proactive Agent**: Implement memory preloading before each conversation turn
5. **Memory Context Integration**: Properly pass memory results to the agent for context-aware responses

### Database Session Agent
⚠️ Currently not working properly - needs investigation.

## �📚 Further Reading

- [Google ADK Documentation](https://developers.google.com/adk)
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/azure/ai-services/agent/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitHub Models](https://docs.github.com/en/github-models)

## 🤝 Contributing

This is an educational playground for exploring agent architectures. Feel free to experiment with different models, tools, and frameworks!</content>
<parameter name="filePath">/Users/abdulfaras/Agent_Building_Playground/README.md