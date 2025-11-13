from google.adk.agents import Agent
from google.adk.sessions import DatabaseSessionService, Session
from google.adk.runners import Runner, RunConfig
from google.genai.types import ContextWindowCompressionConfig, SlidingWindow, Content, Part
import asyncio
import os

# Set dummy API key for testing (replace with real key for actual use)
os.environ['GOOGLE_API_KEY'] = 'dummy_key_for_testing'

# Import the agent from the agent module
import agent
root_agent = agent.root_agent

async def main():
    # Configure DatabaseSessionService (basic setup without compression for now)
    session_service = DatabaseSessionService(
        db_url="sqlite:///sessions.db"
    )

    # Create runner with database session service
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="database_session_demo_agent"
    )

    # Create a new session
    session = await session_service.create_session(
        app_name="database_session_demo_agent",
        user_id="demo_user"
    )

    print("Database Session Demo Agent")
    print("This agent uses persistent database storage with event compaction.")
    print("Conversations are saved to 'sessions.db' and survive application restarts.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break

        try:
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
                        break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())