# Database Session Demo Agent

This agent acts as a general chatbot while demonstrating persistent session management using DatabaseSessionService with SQLite and event compaction.

## Features

### General Chatbot
- Can engage in conversations about any topic
- Helpful and informative responses

### Database Session Demonstration
When asked to demonstrate database concepts, the agent can:
- **Explain Database Sessions**: Persistent storage in SQLite
- **Show Database Data**: Display current sessions, events, and state from the database
- **Demonstrate Compaction**: How event compression manages memory usage
- **Database Inspection**: Examine stored session data and compaction status

### Persistent Sessions with DatabaseSessionService
- Sessions stored in SQLite database (persistent across restarts)
- Database inspection capabilities
- Session state management

### Event Compaction
- Context window compression to manage memory
- Sliding window compression (target_tokens: 1000)
- Automatic compaction when conversation history grows

## Configuration

- **Database**: SQLite file `sessions.db`
- **Compression**: Sliding window with 1000 token target
- **Persistence**: Sessions survive application restarts

## Usage

### Web UI (Recommended)
Run the agent using the ADK web interface:
```bash
cd "/Users/abdulfaras/Agent_Building_Playground"
source .venv/bin/activate
adk web "Google ADK"
```
Then select `database_session_demo_agent` from the dropdown.

**Note**: Requires Google AI API key. Set `GOOGLE_API_KEY` environment variable.

### Direct Runner (For persistent sessions)
For full database persistence and compaction features, use the custom runner:
```bash
cd "Google ADK/database_session_agent"
python run_agent.py
```

**Note**: Requires Google AI API key. Set `GOOGLE_API_KEY` environment variable with a valid key.

**Status**: ⚠️ Database persistence infrastructure is implemented but not working properly - needs investigation. Sessions are stored in `sessions.db` but the agent may not be functioning correctly.

## Example Interactions

1. **General Chat**: "Tell me about machine learning"
2. **Demonstrate Database**: "Show me the database session data" or "How does compaction work?"
3. **Inspect Database**: "Display current database contents"
4. **Check Compaction**: "Show compaction status"

The agent seamlessly switches between general conversation and demonstrating database session concepts.