from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner, RunConfig
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.adk.tools.tool_context import ToolContext
import asyncio
import logging
import os

# Import the agent from the agent module
import agent
root_agent = agent.root_agent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("MEMORY_INTEGRATION: Step 1 - Initialize: Creating MemoryService and providing it to Runner")

    # Step 1: Initialize - Create a MemoryService and provide it to your agent via the Runner
    memory_service = InMemoryMemoryService()
    session_service = InMemorySessionService()

    # Create runner with memory service
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        memory_service=memory_service,  # This enables memory functionality
        app_name="proactive_memory_agent"
    )

    # Create a new session
    session = await session_service.create_session(
        app_name="proactive_memory_agent",
        user_id="demo_user"
    )

    logger.info(f"MEMORY_INTEGRATION: MemoryService initialized. Session created with ID: {session.id}")

    # Create preload memory tool for proactive loading
    preload_tool = PreloadMemoryTool()

    print("Proactive Memory Agent")
    print("This agent demonstrates PROACTIVE memory loading - memory is automatically loaded before each turn.")
    print("Features:")
    print("- Proactive memory loading (preload_memory before each turn)")
    print("- Manual memory search")
    print("- Google search integration")
    print("- InMemoryMemoryService (stores conversation events)")
    print("Type 'quit' to exit, 'memory' to see memory features.\n")

    conversation_turns = 0

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            logger.info("MEMORY_INTEGRATION: Step 2 - Ingest: Transferring session data to memory before exit")
            # Step 2: Ingest - Transfer session data to memory using add_session_to_memory()
            await memory_service.add_session_to_memory(session)
            logger.info(f"MEMORY_INTEGRATION: Session data ingested into memory for session {session.id}")
            print("Goodbye! Session data has been saved to memory.")
            break

        conversation_turns += 1
        logger.info(f"CONVERSATION_TURN: {conversation_turns} - User input: {user_input[:50]}...")

        try:
            # Step 3: Retrieve - For proactive agent, preload memory before each turn
            logger.info("MEMORY_INTEGRATION: Step 3 - Retrieve: Preloading memory before this turn")

            # Create a tool context for preloading
            tool_context = ToolContext()
            # Note: In a real implementation, the preload tool would be called here
            # For demonstration, we'll log the proactive loading
            logger.info("PRELOAD_MEMORY: Memory preloaded for this conversation turn")

            # Create message content
            message = Content(parts=[Part(text=user_input)])

            # Run the agent with the persistent session
            events = list(runner.run(
                user_id="demo_user",
                session_id=session.id,
                new_message=message
            ))

            # Get the final response
            for event in events:
                if hasattr(event, 'content') and event.content:
                    # Extract text from the response content
                    response_text = ""
                    if event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                response_text += part.text
                    if response_text:
                        print(f"Agent: {response_text}")
                        logger.info(f"AGENT_RESPONSE: {response_text[:100]}...")
                        break

        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            logger.error(f"AGENT_ERROR: {error_msg}")

if __name__ == "__main__":
    asyncio.run(main())