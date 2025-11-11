#!/usr/bin/env python3
"""
Test script for the Currency Converter Agent
"""

import asyncio
from currency_agent.agent import root_agent

async def test_agent():
    """Test the currency converter agent instantiation and structure."""
    try:
        print("Testing agent instantiation...")
        print(f"Root agent name: {root_agent.name}")
        print(f"Root agent description: {root_agent.description}")
        print(f"Number of tools: {len(root_agent.tools)}")
        print(f"Tool names: {[tool.__name__ if hasattr(tool, '__name__') else str(tool) for tool in root_agent.tools]}")

        # Check sub-agents
        print(f"Number of sub-agents: {len(root_agent.sub_agents)}")
        for sub_agent in root_agent.sub_agents:
            print(f"Sub-agent: {sub_agent.name} - {sub_agent.description}")

        print("-" * 50)
        print("Testing individual functions...")

        # Test fees_percentage function
        from currency_agent.agent import fees_percentage, get_conversion_rate

        print("Testing fees_percentage:")
        result = fees_percentage("visa")
        print(f"Visa fee: {result}")

        result = fees_percentage("mastercard")
        print(f"Mastercard fee: {result}")

        result = fees_percentage("invalid")
        print(f"Invalid card: {result}")

        print("\nTesting get_conversion_rate:")
        result = get_conversion_rate("USD", "EUR")
        print(f"USD to EUR: {result}")

        result = get_conversion_rate("EUR", "GBP")
        print(f"EUR to GBP: {result}")

        result = get_conversion_rate("USD", "INVALID")
        print(f"USD to INVALID: {result}")

        print("-" * 50)
        print("Agent structure and function validation completed successfully!")
        print("Note: Full agent execution requires GOOGLE_API_KEY environment variable.")

    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())