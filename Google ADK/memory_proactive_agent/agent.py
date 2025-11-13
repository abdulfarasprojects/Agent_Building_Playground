from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner, RunConfig
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def manual_memory_search(query: str) -> str:
    """Manually search memory for specific information.

    Args:
        query (str): The search query to find in memory

    Returns:
        str: Search results from memory
    """
    logger.info(f"MANUAL_MEMORY_SEARCH: Searching memory for query: '{query}'")
    # Note: Memory search will be handled by the runner's memory service
    return f"Manual search initiated for: {query}. Memory search functionality is handled by the InMemoryMemoryService."

def perform_google_search(query: str) -> str:
    """Perform a Google search for real-time information.

    Args:
        query (str): The search query

    Returns:
        str: Search results (simulated for demonstration)
    """
    logger.info(f"GOOGLE_SEARCH: Searching for query: '{query}'")
    # Note: In a real implementation, this would call Google Search API
    # For demonstration, we'll return a simulated response
    return f"Google search results for '{query}': [Simulated search results - in production this would use Google Search API]"

def explain_memory_features() -> str:
    """Explain the memory features of this proactive memory agent.

    Returns:
        str: Explanation of memory capabilities
    """
    return """
Proactive Memory Agent Features:

1. **Proactive Memory Loading**:
   - Memory is automatically loaded before every conversation turn
   - Agent has immediate access to relevant historical context
   - No need for the agent to decide when to search - memory is always available

2. **Manual Memory Search**:
   - Users can explicitly request memory searches using manual_memory_search tool
   - Allows direct querying of stored conversation data

3. **InMemoryMemoryService**:
   - Stores raw conversation events without consolidation
   - Keyword-based search (simple word matching)
   - In-memory storage (resets on restart)
   - Ideal for learning and local development

4. **Three-Step Integration Process**:
   - Initialize: MemoryService created and provided to Runner
   - Ingest: Session data transferred to memory using add_session_to_memory()
   - Retrieve: Memory automatically preloaded before each turn

5. **Google Search Integration**:
   - Access to real-time web search for current information
   - Complements memory with external knowledge

The agent will log all memory operations for demonstration purposes.
"""

# Proactive Memory Agent
root_agent = Agent(
    name="proactive_memory_agent",
    model="gemini-2.0-flash",
    description="A chatbot with proactive memory loading capabilities and Google search",
    instruction="""You are a helpful chatbot with access to memory and Google search tools.

MEMORY FEATURES:
- You have PROACTIVE memory loading - memory is automatically loaded before every conversation turn
- You always have access to relevant historical context without needing to search
- You also have manual memory search capabilities for explicit user requests

TOOL USAGE GUIDELINES:
- manual_memory_search: Use this when users explicitly ask to search memory
- perform_google_search: Use this for real-time information, current events, or when you need external knowledge
- explain_memory_features: Use this to explain your memory capabilities when asked

MEMORY CONTEXT: Your memory has been preloaded for this conversation turn, so you have access to relevant historical information.

LOGGING: Always log your memory operations and decisions for demonstration purposes.

Be conversational and helpful while demonstrating your memory capabilities.""",
    tools=[manual_memory_search, perform_google_search, explain_memory_features],
)