# Session Management Demo Agent

This agent acts as a general chatbot while demonstrating Google ADK's session management capabilities using InMemorySessionService.

## Features

### General Chatbot
- Can engage in conversations about any topic
- Helpful and informative responses

### Session Management Demonstration
When asked to demonstrate session concepts, the agent can:
- **Explain Session Concepts**: Session as notebook 📓, events as entries 📝, SessionService as filing cabinet 🗄️
- **Show Session Data**: Display current session information (ID, events, state)
- **Demonstrate State Management**: How to store and retrieve custom data

### SessionService (Storage Layer)
- Manages creation, storage, and retrieval of session data
- Uses InMemorySessionService (data stored in memory, lost on restart)
- Different implementations available: InMemory, Database, Cloud

## Usage

### Web UI (Recommended)
Run the agent using the ADK web interface:
```bash
cd "/Users/abdulfaras/Agent_Building_Playground"
source .venv/bin/activate
adk web "Google ADK"
```
Then select `session_management_demo_agent` from the dropdown.

### Direct CLI
Run the agent directly:
```bash
cd "Google ADK"
adk run session_demo_agent
```

**Note**: Session data is stored in memory only and will be lost when the application restarts.

## Example Interactions

1. **General Chat**: "What's the weather like today?"
2. **Demonstrate Sessions**: "Show me how sessions work" or "Demonstrate session management"
3. **Inspect Session**: "Display current session data"
4. **State Management**: "Explain how session state works"

The agent seamlessly switches between general conversation and demonstrating session concepts.