# Agent Building Playground

A comprehensive exploration of modern AI agent architectures, demonstrating multi-agent systems, tool integration, and safety workflows using different AI frameworks.

## 🎯 Project Overview

This playground showcases two distinct AI agent implementations that demonstrate key concepts in agent development:

1. **Currency Conversion Agent** (Google ADK) - Financial calculations with multi-agent delegation
2. **Cooking Assistant Agent** (Microsoft Agent Framework) - Recipe generation with safety workflows

Both agents integrate **Model Context Protocol (MCP)** servers for extended tool capabilities and demonstrate production-ready patterns for AI agent development.

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
│   └── currency_agent/            # Alternative agent structure
│       ├── __init__.py
│       └── agent.py
├── MS Agent Framework/            # Microsoft Agent Framework Implementation
│   ├── cooking_agent.py          # Cooking assistant with safety workflows
│   ├── ui.py                     # Web UI for the cooking agent
│   ├── requirements.txt          # Python dependencies
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

### 2. Cooking Assistant Agent (Microsoft Agent Framework)

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

1. **Agent Design Patterns**: Multi-agent delegation, tool integration, safety workflows
2. **Framework Comparison**: Google ADK vs Microsoft Agent Framework approaches
3. **Protocol Integration**: MCP for extending agent capabilities
4. **Safety Implementation**: Mandatory user confirmation for sensitive operations
5. **Code Execution**: Using Python execution for mathematical accuracy
6. **Async Programming**: Bridging async tools with sync frameworks
7. **Model Selection**: Choosing appropriate models for different tasks

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for MCP server)
- GitHub Personal Access Token (for MS Agent Framework)
- Google ADK credentials (for Google ADK agent)

### Running the Agents

#### Cooking Assistant (MS Agent Framework)
```bash
cd "MS Agent Framework"
pip install -r requirements.txt
# Set GITHUB_TOKEN in .env file
python cooking_agent.py
```

#### Currency Agent (Google ADK)
```bash
cd "Google ADK"
# Configure Google ADK credentials
python agent.py
```

## 📚 Further Reading

- [Google ADK Documentation](https://developers.google.com/adk)
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/azure/ai-services/agent/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitHub Models](https://docs.github.com/en/github-models)

## 🤝 Contributing

This is an educational playground for exploring agent architectures. Feel free to experiment with different models, tools, and frameworks!</content>
<parameter name="filePath">/Users/abdulfaras/Agent_Building_Playground/README.md