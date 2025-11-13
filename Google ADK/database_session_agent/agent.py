from google.adk.agents import Agent
from google.adk.sessions import DatabaseSessionService, Session
from google.adk.runners import Runner, RunConfig
from google.genai.types import ContextWindowCompressionConfig, SlidingWindow
import sqlite3
import os

# Tool to explain database session concepts
def explain_database_session_concepts() -> str:
    """Explain persistent session management with database storage.

    Returns:
        str: Explanation of database session concepts
    """
    return """
Persistent Sessions with DatabaseSessionService:

1. **Database Storage**: 
   - Sessions stored in SQLite database (persistent)
   - Survives application restarts and crashes
   - Can be inspected and analyzed externally

2. **Event Compaction**: 
   - ContextWindowCompressionConfig manages memory usage
   - SlidingWindow compression (target_tokens: 1000)
   - Automatically compresses old conversation history
   - Preserves conversation continuity while saving memory

3. **Database Inspection**:
   - Can query all sessions in the database
   - Examine individual session events and state
   - Useful for analytics and debugging

4. **Compaction Process**:
   - compaction_interval: Triggers after N conversations
   - overlap_size: Retains recent context for continuity
   - Old events replaced with summaries (not deleted)
   - Maintains conversation flow and understanding

The database file 'sessions.db' contains all session data and can be analyzed separately.
"""

def demonstrate_compaction_behavior() -> str:
    """Demonstrate how event compaction works.

    Returns:
        str: Explanation of compaction behavior
    """
    return """
Event Compaction Behavior:

BEFORE COMPACTION:
Session Events: [msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10]

AFTER COMPACTION (compaction_interval=5, overlap_size=2):
Session Events: [summary_of_1-8, msg9, msg10]

KEY POINTS:
- Old events are NOT deleted
- They are replaced with a single summary event
- Recent events (overlap_size) are preserved for context
- Conversation continuity is maintained
- Memory usage is reduced while preserving understanding

This allows long conversations without unbounded memory growth.
"""

def explain_database_inspection() -> str:
    """Explain how to inspect database contents.

    Returns:
        str: Information about database inspection
    """
    return """
Database Inspection Capabilities:

1. **Session Table**: Contains all sessions with metadata
   - session_id: Unique identifier
   - app_name: Application that created the session
   - user_id: User identifier
   - last_update_time: When session was last modified

2. **Events Table**: Contains all conversation events
   - Linked to sessions by session_id
   - Includes message content, author, timestamp
   - Shows complete conversation history

3. **State Table**: Contains session state data
   - Key-value pairs for each session
   - Persists custom data across conversations

4. **Inspection Tools**:
   - Query session counts and metadata
   - Examine individual session contents
   - Analyze conversation patterns
   - Debug agent behavior

The SQLite database can be opened with any SQLite browser for detailed analysis.
"""

# Tool to display current database session data
def display_database_session_data() -> str:
    """Display current session data from the database including events and state.

    Returns:
        str: Formatted database session data
    """
    try:
        if os.path.exists('sessions.db'):
            conn = sqlite3.connect('sessions.db')
            cursor = conn.cursor()

            # Get session count
            cursor.execute("SELECT COUNT(*) FROM sessions")
            session_count = cursor.fetchone()[0]

            # Get recent sessions
            cursor.execute("""
                SELECT session_id, app_name, user_id, last_update_time
                FROM sessions
                ORDER BY last_update_time DESC
                LIMIT 5
            """)
            sessions = cursor.fetchall()

            # Get event count
            cursor.execute("SELECT COUNT(*) FROM events")
            event_count = cursor.fetchone()[0]

            conn.close()

            result = f"""
Database Session Data:
- Total Sessions: {session_count}
- Total Events: {event_count}

Recent Sessions:
"""
            for session in sessions:
                result += f"- ID: {session[0]}, App: {session[1]}, User: {session[2]}, Last Update: {session[3]}\n"

            return result
        else:
            return "No database file found. Sessions will be created when the agent runs."
    except Exception as e:
        return f"Error accessing database: {str(e)}"

# Tool to show compaction status
def show_compaction_status() -> str:
    """Show the current compaction status and how it affects memory usage.

    Returns:
        str: Compaction status information
    """
    try:
        if os.path.exists('sessions.db'):
            conn = sqlite3.connect('sessions.db')
            cursor = conn.cursor()

            # Get total events
            cursor.execute("SELECT COUNT(*) FROM events")
            total_events = cursor.fetchone()[0]

            # Check for summary events (indicating compaction)
            cursor.execute("SELECT COUNT(*) FROM events WHERE content LIKE '%summary%' OR content LIKE '%compressed%'")
            summary_events = cursor.fetchone()[0]

            conn.close()

            compaction_info = f"""
Compaction Status:
- Total Events in Database: {total_events}
- Summary/Compressed Events: {summary_events}

Compaction Configuration:
- compaction_interval: 5 (triggers after 5 conversations)
- overlap_size: 2 (retains recent context)
- target_tokens: 1000 (memory limit for sliding window)

How Compaction Works:
1. When conversation reaches compaction_interval, old events are compressed
2. Events before the overlap_size are replaced with a summary
3. Recent events are preserved for context continuity
4. Memory usage is controlled while maintaining conversation understanding

Status: {'Compaction has occurred' if summary_events > 0 else 'No compaction yet - conversation still within limits'}
"""

            return compaction_info
        else:
            return """
Compaction Status: No database yet

This agent uses DatabaseSessionService with ContextWindowCompressionConfig:
- Compression Type: SlidingWindow
- Target Tokens: 1000
- Compaction Interval: 5 conversations
- Overlap Size: 2 recent events preserved

Compaction will begin automatically once conversations exceed the interval.
"""
    except Exception as e:
        return f"Error checking compaction status: {str(e)}"

# Database Session Demo Agent
root_agent = Agent(
    name="database_session_demo_agent",
    model="gemini-2.0-flash",
    description="General chatbot that can demonstrate persistent database sessions and compaction",
    instruction="""You are a helpful general chatbot. You can engage in normal conversation about any topic.

When asked to demonstrate database sessions, compaction, or how persistent memory works, use the display_database_session_data and show_compaction_status tools to show current session information and explain the concepts using the other tools.

Always be ready to switch between general chat and demonstrating database session concepts.""",
    tools=[explain_database_session_concepts, demonstrate_compaction_behavior, explain_database_inspection, display_database_session_data, show_compaction_status],
)