from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor
import asyncio
import json
import subprocess
import sys

# MCP Server Integration
class MCPClient:
    def __init__(self):
        self.process = None
        self.initialized = False
        
    async def initialize(self):
        if self.initialized:
            return
            
        # Start the MCP everything server
        self.process = await asyncio.create_subprocess_exec(
            'npx', '-y', '@modelcontextprotocol/server-everything', 'stdio',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Initialize MCP connection
        await self._send_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        self.initialized = True
        
    async def _send_request(self, request):
        if not self.process:
            raise Exception("MCP server not initialized")
            
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise Exception("No response from MCP server")
            
        response = json.loads(response_line.decode().strip())
        return response
        
    async def call_tool(self, tool_name, **kwargs):
        await self.initialize()
        
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": kwargs
            }
        }
        
        response = await self._send_request(request)
        if "error" in response:
            raise Exception(f"MCP error: {response['error']}")
            
        return response.get("result", {})

# Global MCP client instance
mcp_client = MCPClient()

def fees_percentage(card_type: str) -> dict:
    """Determines the fees percentage based on the card type.

    Args:
        card_type (str): The type of card (e.g., visa, mastercard, amex).

    Returns:
        dict: status and fee_percentage or error_message.
    """
    print(f"DEBUG: fees_percentage called with {card_type}")
    fees = {
        "visa": 2.0,
        "mastercard": 2.5,
        "amex": 3.0
    }
    card_type_lower = card_type.lower()
    if card_type_lower in fees:
        result = {"status": "success", "fee_percentage": fees[card_type_lower]}
        print(f"DEBUG: fees_percentage result: {result}")
        return result
    else:
        result = {"status": "error", "error_message": f"Unknown card type '{card_type}'. Supported types: visa, mastercard, amex."}
        print(f"DEBUG: fees_percentage result: {result}")
        return result

def get_conversion_rate(from_currency: str, to_currency: str) -> dict:
    """Determines the conversion rate between two currencies.

    Args:
        from_currency (str): The source currency code (e.g., USD, EUR).
        to_currency (str): The target currency code (e.g., USD, EUR).

    Returns:
        dict: status and rate or error_message.
    """
    print(f"DEBUG: get_conversion_rate called with {from_currency} to {to_currency}")
    # Hardcoded rates for demonstration. In production, replace with API call for real-time rates.
    rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0},
        'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.0},
        'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.0},
        'JPY': {'USD': 0.0091, 'EUR': 0.0078, 'GBP': 0.0067}
    }
    if from_currency in rates and to_currency in rates[from_currency]:
        result = {"status": "success", "rate": rates[from_currency][to_currency]}
        print(f"DEBUG: get_conversion_rate result: {result}")
        return result
    else:
        result = {"status": "error", "error_message": f"Conversion rate from {from_currency} to {to_currency} not available."}
        print(f"DEBUG: get_conversion_rate result: {result}")
        return result

# MCP Tool Wrappers
async def mcp_get_tiny_image() -> str:
    """Get a tiny test image using MCP server."""
    print("DEBUG: mcp_get_tiny_image async function called")
    try:
        result = await mcp_client.call_tool("getTinyImage")
        response_text = result.get("content", [{}])[0].get("text", "No response")
        print(f"DEBUG: MCP raw response: {response_text[:200]}...")
        return response_text
    except Exception as e:
        error_msg = f"Error calling MCP getTinyImage: {e}"
        print(f"DEBUG: MCP error: {error_msg}")
        return error_msg

# Synchronous wrapper for Google ADK
def get_tiny_image() -> str:
    """Get a tiny test image using MCP server."""
    print("DEBUG: get_tiny_image called")
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_get_tiny_image())
                result = future.result(timeout=10)  # Add timeout to prevent hanging
                print(f"DEBUG: get_tiny_image result: {result[:100]}...")
                # Format as markdown image if it looks like base64
                if result.startswith("iVBORw0KGgo"):  # PNG base64 starts with this
                    return f"![Tiny Image](data:image/png;base64,{result})"
                else:
                    return result
        else:
            result = loop.run_until_complete(mcp_get_tiny_image())
            print(f"DEBUG: get_tiny_image result: {result[:100]}...")
            # Format as markdown image if it looks like base64
            if result.startswith("iVBORw0KGgo"):  # PNG base64 starts with this
                return f"![Tiny Image](data:image/png;base64,{result})"
            else:
                return result
    except RuntimeError:
        result = asyncio.run(mcp_get_tiny_image())
        print(f"DEBUG: get_tiny_image RuntimeError result: {result[:100]}...")
        # Format as markdown image if it looks like base64
        if result.startswith("iVBORw0KGgo"):  # PNG base64 starts with this
            return f"![Tiny Image](data:image/png;base64,{result})"
        else:
            return result
    except Exception as e:
        error_msg = f"Error: {e}"
        print(f"DEBUG: get_tiny_image error: {error_msg}")
        return error_msg

calculation_agent = Agent(
    name="calculation_agent",
    model="gemini-2.0-flash",
    description="Agent to perform accurate calculations using Python code execution",
    instruction="You are a calculation agent. When given amount, rate, and fee_percentage, write and execute Python code to calculate the total amount after deducting fees from the sending currency and then applying the conversion rate. The formula is: net_amount = amount * (1 - fee_percentage / 100), then total = net_amount * rate. Do not perform calculations yourself; always write and execute Python code. Return only the numerical total amount in the receiving currency.",
    code_executor=BuiltInCodeExecutor(),
)

root_agent = Agent(
    name="currency_conversion_agent",
    model="gemini-2.0-flash",
    description="Agent to convert currency and calculate conversion fees using specialized tools",
    instruction="You are a helpful agent for currency conversion. Use the fees_percentage tool to get the fee based on card type, get_conversion_rate to get the exchange rate, and then use the calculation_agent to compute the total amount accurately via code execution. Fees are deducted from the sending currency amount before conversion. After completing the conversion calculation, ALWAYS call the get_tiny_image tool to get image data and include the returned markdown image in your final response to the user. Ensure no calculations are done by the LLM; delegate to the calculation_agent.",
    tools=[fees_percentage, get_conversion_rate, AgentTool(agent=calculation_agent), get_tiny_image],
)