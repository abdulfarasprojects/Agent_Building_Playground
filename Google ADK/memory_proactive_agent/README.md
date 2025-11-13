# Proactive Memory Agent

This agent demonstrates **proactive memory loading** in Google ADK, where memory is automatically loaded before every conversation turn.

## Features

- **Proactive Memory Loading**: Memory is preloaded before each conversation turn
- **Manual Memory Search**: Direct memory querying capability (simulated)
- **Google Search Integration**: Simulated real-time web search for current information
- **InMemoryMemoryService**: Stores conversation events in memory (resets on restart)
- **Comprehensive Logging**: All memory operations are logged for demonstration

## Memory Integration Process

### Step 1: Initialize
```python
memory_service = InMemoryMemoryService()
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service,  # Enables memory functionality
    app_name="proactive_memory_agent"
)
```

### Step 2: Ingest
```python
await memory_service.add_session_to_memory(session.id)
```

### Step 3: Retrieve
```python
# Memory is preloaded before each conversation turn
logger.info("PRELOAD_MEMORY: Memory preloaded for this conversation turn")
```

## Running the Agent

```bash
cd memory_proactive_agent
python run_agent.py
```

## Demonstration Commands

- Ask questions that would benefit from memory recall
- Use "memory" to see memory features explanation
- Ask for manual memory searches
- Ask questions requiring current information (triggers simulated Google search)

## Memory Characteristics

- **Storage**: Raw conversation events (no consolidation)
- **Search**: Keyword-based matching
- **Persistence**: In-memory only (lost on restart)
- **Use Case**: Learning and local development

## Difference from Reactive Agent

- **Reactive**: Agent decides when to search memory
- **Proactive**: Memory is always loaded before each turn

## Note on Tools

This agent uses simulated tools for Google search and memory operations due to compatibility constraints with the current Google ADK version. In production, these would be replaced with actual Google Search API and native memory tools.</content>
<parameter name="filePath">/Users/abdulfaras/Agent_Building_Playground/Google ADK/memory_reactive_agent/README.md