from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.runners import RunConfig
import asyncio
from typing import Optional

# Tool to demonstrate session concepts
def explain_session_concepts() -> str:
    """Explain the key concepts of session management.

    Returns:
        str: Explanation of session management concepts
    """
    return """
Session Management in Google ADK:

1. **Session (= Notebook 📓)**: 
   - Contains conversation history and state
   - Identified by unique session ID
   - Has events (conversation entries) and state (custom data)

2. **Events (= Individual entries 📝)**: 
   - Each message, response, or action in the conversation
   - Stored chronologically in the session
   - Include metadata like author, timestamp, content

3. **SessionService (= Filing cabinet 🗄️)**: 
   - Storage layer for session data
   - InMemorySessionService: Stores in memory (fast, temporary)
   - DatabaseSessionService: Persistent storage in database
   - Manages creation, retrieval, and updates of sessions

4. **Runner (= Assistant 🤖)**: 
   - Orchestration layer managing conversation flow
   - Automatically maintains conversation history
   - Handles context engineering behind the scenes
   - Manages the interaction between user and agent

The Runner uses the SessionService to persist conversation state,
allowing for resumable conversations and context-aware responses.
"""

def demonstrate_session_state_management(action: str, key: Optional[str] = None, value: Optional[str] = None) -> str:
    """Demonstrate session state management concepts.

    Args:
        action (str): 'explain', 'example_get', 'example_set'
        key (Optional[str]): Key for operations (required for 'example_set')
        value (Optional[str]): Value for set operations (required for 'example_set')

    Returns:
        str: Demonstration of state management
    """
    if action == "explain":
        return """
Session State Management:

- State is a dictionary stored with each session
- Persists custom data across conversation turns
- Can store user preferences, conversation context, etc.
- Automatically managed by the SessionService
- Survives conversation interruptions and resumes

Example: Storing user preferences or conversation context
"""

    elif action == "example_get":
        return "Example: Getting state['user_name'] would return the stored user name from previous interactions"

    elif action == "example_set":
        return f"Example: Setting state['{key}'] = '{value}' would store this data for future use"

    else:
        return "Use: explain, example_get, or example_set <key> <value>"

# Tool to display current session data
def display_session_data() -> str:
    """Display the current session data including events and state.

    Returns:
        str: Formatted session data
    """
    return """
In-Memory Session Data:

Note: This agent uses InMemorySessionService, so session data exists only in memory during the conversation.

Session Concepts:
- Sessions are stored in RAM and lost when the application restarts
- Each conversation has a unique session ID
- Events are stored chronologically in the session
- State can store custom key-value data

To see actual session data, the agent would need to be running with a SessionService instance.
When demonstrating, the agent can show:
- Current session ID (if available)
- Number of events in the conversation
- Current state data
- Event history (last few messages)

Example output when running:
- Session ID: abc-123
- Events: 5 messages
- State: {'user_name': 'John', 'topic': 'session_demo'}
"""

# Session Management Demo Agent
root_agent = Agent(
    name="session_management_demo_agent",
    model="gemini-2.0-flash",
    description="General chatbot that can demonstrate session management concepts",
    instruction="""You are a helpful general chatbot. You can engage in normal conversation about any topic.

When asked to demonstrate session management or how sessions work, use the display_session_data tool to show current session information, and explain the concepts using the other tools.

Always be ready to switch between general chat and demonstrating session concepts.""",
    tools=[explain_session_concepts, demonstrate_session_state_management, display_session_data],
)