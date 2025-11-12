import asyncio
import os
import json
import subprocess
import sys
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

# Mock data for allergens (gluten and nuts)
ALLERGEN_DATA = {
    "wheat": ["gluten"],
    "flour": ["gluten"],
    "bread": ["gluten"],
    "pasta": ["gluten"],
    "barley": ["gluten"],
    "rye": ["gluten"],
    "oats": ["gluten"],  # cross-contamination possible
    "almonds": ["nuts"],
    "peanuts": ["nuts"],
    "walnuts": ["nuts"],
    "cashews": ["nuts"],
    "pecans": ["nuts"],
    "hazelnuts": ["nuts"],
    "pistachios": ["nuts"],
    "macadamia": ["nuts"],
    "brazil nuts": ["nuts"],
    "pine nuts": ["nuts"],
    "chestnuts": ["nuts"],
}

# Mock data for calories per 100g
CALORIE_DATA = {
    "chicken": 165,
    "beef": 250,
    "pork": 242,
    "fish": 120,
    "rice": 130,
    "pasta": 157,
    "potatoes": 77,
    "bread": 265,
    "flour": 364,
    "butter": 717,
    "oil": 884,
    "milk": 61,
    "cheese": 402,
    "eggs": 155,
    "tomatoes": 18,
    "onions": 40,
    "garlic": 149,
    "carrots": 41,
    "lettuce": 15,
    "spinach": 23,
    "broccoli": 34,
    "mushrooms": 22,
    "apples": 52,
    "bananas": 89,
    "oranges": 47,
    "strawberries": 32,
    "blueberries": 57,
    "sugar": 387,
    "salt": 0,
    "pepper": 251,
    "olive oil": 884,
    "soy sauce": 53,
    "vinegar": 18,
    "honey": 304,
    "almonds": 579,
    "peanuts": 567,
    "walnuts": 654,
}

# Mock data for ingredient prices per unit
PRICE_DATA = {
    "chicken": {"price": 5.99, "unit": "lb"},
    "beef": {"price": 8.99, "unit": "lb"},
    "pork": {"price": 6.49, "unit": "lb"},
    "fish": {"price": 12.99, "unit": "lb"},
    "rice": {"price": 2.49, "unit": "lb"},
    "pasta": {"price": 1.99, "unit": "lb"},
    "potatoes": {"price": 0.79, "unit": "lb"},
    "bread": {"price": 3.49, "unit": "loaf"},
    "flour": {"price": 2.99, "unit": "lb"},
    "butter": {"price": 4.99, "unit": "lb"},
    "oil": {"price": 6.99, "unit": "bottle"},
    "milk": {"price": 3.49, "unit": "gallon"},
    "cheese": {"price": 5.99, "unit": "lb"},
    "eggs": {"price": 4.99, "unit": "dozen"},
    "tomatoes": {"price": 2.99, "unit": "lb"},
    "onions": {"price": 1.49, "unit": "lb"},
    "garlic": {"price": 0.99, "unit": "head"},
    "carrots": {"price": 1.29, "unit": "lb"},
    "lettuce": {"price": 1.99, "unit": "head"},
    "spinach": {"price": 3.99, "unit": "bag"},
    "broccoli": {"price": 2.49, "unit": "head"},
    "mushrooms": {"price": 4.99, "unit": "lb"},
    "apples": {"price": 2.99, "unit": "lb"},
    "bananas": {"price": 0.59, "unit": "lb"},
    "oranges": {"price": 1.99, "unit": "lb"},
    "strawberries": {"price": 4.99, "unit": "pint"},
    "blueberries": {"price": 5.99, "unit": "pint"},
    "sugar": {"price": 2.49, "unit": "lb"},
    "salt": {"price": 1.99, "unit": "container"},
    "pepper": {"price": 3.99, "unit": "container"},
    "olive oil": {"price": 8.99, "unit": "bottle"},
    "soy sauce": {"price": 3.49, "unit": "bottle"},
    "vinegar": {"price": 2.99, "unit": "bottle"},
    "honey": {"price": 6.99, "unit": "jar"},
    "almonds": {"price": 9.99, "unit": "lb"},
    "peanuts": {"price": 3.99, "unit": "lb"},
    "walnuts": {"price": 11.99, "unit": "lb"},
}

def check_allergens(recipe_text: str) -> dict:
    """
    Tool to identify if there is gluten or nuts in the recipe.
    
    Args:
        recipe_text: The dish name, ingredients, or full recipe text to analyze
        
    Returns:
        dict: Contains 'gluten' and 'nuts' boolean flags and lists of detected ingredients
    """
    print("LOG: check_allergens tool called")
    recipe_lower = recipe_text.lower()
    detected_gluten = []
    detected_nuts = []
    
    for ingredient, allergens in ALLERGEN_DATA.items():
        if ingredient in recipe_lower:
            if "gluten" in allergens:
                detected_gluten.append(ingredient)
            if "nuts" in allergens:
                detected_nuts.append(ingredient)
    
    return {
        "gluten": len(detected_gluten) > 0,
        "nuts": len(detected_nuts) > 0,
        "gluten_ingredients": detected_gluten,
        "nut_ingredients": detected_nuts,
        "allergens_found": detected_gluten + detected_nuts
    }

def calculate_calories(recipe_text: str, servings: int = 4) -> dict:
    """
    Tool to identify total calories in 1 portion of the dish.
    
    Args:
        recipe_text: The full recipe text including ingredients and instructions
        servings: Number of servings the recipe makes (default 4)
        
    Returns:
        dict: Contains total calories per serving and breakdown
    """
    print("LOG: calculate_calories tool called")
    recipe_lower = recipe_text.lower()
    total_calories = 0
    ingredient_breakdown = {}
    
    # Simple parsing - look for quantities and ingredients
    # This is a mock implementation - in reality you'd need better parsing
    for ingredient, calories_per_100g in CALORIE_DATA.items():
        if ingredient in recipe_lower:
            # Mock: assume 100g per ingredient mentioned
            # In reality, parse quantities from recipe
            ingredient_breakdown[ingredient] = calories_per_100g
            total_calories += calories_per_100g
    
    calories_per_serving = total_calories / servings if servings > 0 else total_calories
    
    return {
        "total_calories_per_serving": round(calories_per_serving),
        "total_calories_recipe": total_calories,
        "servings": servings,
        "ingredient_breakdown": ingredient_breakdown
    }

def get_ingredient_prices(ingredients: list) -> dict:
    """
    Tool to get price of ingredients.
    
    Args:
        ingredients: List of ingredient names
        
    Returns:
        dict: Contains price information for each ingredient and total cost
    """
    print("LOG: get_ingredient_prices tool called")
    prices = {}
    total_cost = 0
    
    for ingredient in ingredients:
        ingredient_lower = ingredient.lower().strip()
        found = False
        for key, price_info in PRICE_DATA.items():
            if key in ingredient_lower:
                prices[ingredient] = price_info
                # Mock: assume 1 unit per ingredient
                total_cost += price_info["price"]
                found = True
                break
        if not found:
            prices[ingredient] = {"price": "N/A", "unit": "N/A"}
    
    return {
        "ingredient_prices": prices,
        "estimated_total_cost": round(total_cost, 2),
        "currency": "USD"
    }

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

# MCP Tool Wrappers
async def mcp_echo(message: str) -> str:
    """Echo a message using MCP server."""
    print("LOG: mcp_echo tool called")
    try:
        result = await mcp_client.call_tool("echo", message=message)
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP echo: {e}"

async def mcp_add(a: float, b: float) -> str:
    """Add two numbers using MCP server."""
    print("LOG: mcp_add tool called")
    try:
        result = await mcp_client.call_tool("add", a=a, b=b)
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP add: {e}"

async def mcp_long_running_operation(duration: int = 10, steps: int = 5) -> str:
    """Run a long running operation with progress using MCP server."""
    print("LOG: mcp_long_running_operation tool called")
    try:
        result = await mcp_client.call_tool("longRunningOperation", duration=duration, steps=steps)
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP longRunningOperation: {e}"

async def mcp_print_env() -> str:
    """Print environment variables using MCP server."""
    print("LOG: mcp_print_env tool called")
    try:
        result = await mcp_client.call_tool("printEnv")
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP printEnv: {e}"

async def mcp_sample_llm(prompt: str, max_tokens: int = 100) -> str:
    """Sample LLM response using MCP server."""
    print("LOG: mcp_sample_llm tool called")
    try:
        result = await mcp_client.call_tool("sampleLLM", prompt=prompt, maxTokens=max_tokens)
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP sampleLLM: {e}"

async def mcp_get_tiny_image() -> str:
    """Get a tiny test image using MCP server."""
    print("LOG: mcp_get_tiny_image tool called")
    try:
        result = await mcp_client.call_tool("getTinyImage")
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP getTinyImage: {e}"

async def mcp_list_roots() -> str:
    """List MCP roots using MCP server."""
    print("LOG: mcp_list_roots tool called")
    try:
        result = await mcp_client.call_tool("listRoots")
        return result.get("content", [{}])[0].get("text", "No response")
    except Exception as e:
        return f"Error calling MCP listRoots: {e}"

# Synchronous wrappers for MS Agent Framework
def echo_message(message: str) -> str:
    """Echo a message using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If there's already a running loop, we need to handle this differently
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_echo(message))
                return future.result()
        else:
            return loop.run_until_complete(mcp_echo(message))
    except RuntimeError:
        # No event loop, create a new one
        return asyncio.run(mcp_echo(message))

def add_numbers(a: float, b: float) -> str:
    """Add two numbers using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_add(a, b))
                return future.result()
        else:
            return loop.run_until_complete(mcp_add(a, b))
    except RuntimeError:
        return asyncio.run(mcp_add(a, b))

def long_operation(duration: int = 10, steps: int = 5) -> str:
    """Run a long running operation with progress using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_long_running_operation(duration, steps))
                return future.result()
        else:
            return loop.run_until_complete(mcp_long_running_operation(duration, steps))
    except RuntimeError:
        return asyncio.run(mcp_long_running_operation(duration, steps))

def print_environment() -> str:
    """Print environment variables using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_print_env())
                return future.result()
        else:
            return loop.run_until_complete(mcp_print_env())
    except RuntimeError:
        return asyncio.run(mcp_print_env())

def sample_llm_response(prompt: str, max_tokens: int = 100) -> str:
    """Sample LLM response using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_sample_llm(prompt, max_tokens))
                return future.result()
        else:
            return loop.run_until_complete(mcp_sample_llm(prompt, max_tokens))
    except RuntimeError:
        return asyncio.run(mcp_sample_llm(prompt, max_tokens))

def get_test_image() -> str:
    """Get a tiny test image using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_get_tiny_image())
                return future.result()
        else:
            return loop.run_until_complete(mcp_get_tiny_image())
    except RuntimeError:
        return asyncio.run(mcp_get_tiny_image())

def list_mcp_roots() -> str:
    """List MCP roots using MCP server."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, mcp_list_roots())
                return future.result()
        else:
            return loop.run_until_complete(mcp_list_roots())
    except RuntimeError:
        return asyncio.run(mcp_list_roots())

async def chat_with_agent(user_input: str) -> str:
    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Please set the GITHUB_TOKEN environment variable with your GitHub Personal Access Token."

    # Initialize OpenAI client for GitHub models
    openai_client = AsyncOpenAI(
        base_url="https://models.github.ai/inference",
        api_key=github_token,
    )

    # Create chat client
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id="xai/grok-3"  # Using Grok 3 for advanced reasoning
    )

    # Create the cooking agent
    agent = ChatAgent(
        chat_client=chat_client,
        name="CookingAssistant",
        instructions="""
        You are a helpful cooking assistant AI with access to various tools. You can help users with:
        - Recipe search: Generate detailed recipes based on dish names or ingredients
        - Ingredient extraction: Extract and list ingredients from provided recipe text
        - Allergen checking: Check if recipes contain gluten or nuts
        - Calorie calculation: Calculate calories per serving for recipes
        - Price lookup: Get prices for ingredients
        - MCP Tools: Access to Model Context Protocol server tools including echo, math operations, LLM sampling, and more
        
        IMPORTANT WORKFLOW FOR RECIPE REQUESTS:
        1. When a user asks for a recipe, FIRST use the check_allergens tool to analyze the dish name/ingredients for gluten and nuts
        2. If allergens are detected (gluten or nuts found), ask the user: "This recipe contains [list allergens]. Do you want me to proceed with the recipe creation?"
        3. Only proceed with recipe generation if the user explicitly agrees
        4. If user declines, stop and offer alternatives or end the conversation
        
        When generating recipes, include:
        - List of ingredients with quantities
        - Step-by-step cooking instructions
        - Cooking time and servings
        - Any tips or variations
        
        When extracting ingredients, provide a clean list of ingredients from the recipe text.
        
        Tool usage guidelines:
        - check_allergens: ALWAYS call first when user requests a recipe to check for allergens
        - calculate_calories: Only call when user asks for calorie information
        - get_ingredient_prices: Only call when user asks for prices
        - MCP tools: Use when user requests specific MCP functionality (echo, math, LLM sampling, etc.)
        
        Be friendly, informative, and ensure recipes are safe and practical.
        """,
        tools=[check_allergens, calculate_calories, get_ingredient_prices, 
               echo_message, add_numbers, long_operation, print_environment, 
               sample_llm_response, get_test_image, list_mcp_roots]
    )

    # Create a thread for conversation persistence
    thread = agent.get_new_thread()

    try:
        # Run the agent with user input
        result = await agent.run(user_input, thread=thread)
        return result.text
    except Exception as e:
        return f"Error: {e}"

async def main():
    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Please set the GITHUB_TOKEN environment variable with your GitHub Personal Access Token.")
        return

    # Initialize OpenAI client for GitHub models
    openai_client = AsyncOpenAI(
        base_url="https://models.github.ai/inference",
        api_key=github_token,
    )

    # Create chat client
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id="xai/grok-3"  # Using Grok 3 for advanced reasoning
    )

    # Create the cooking agent
    agent = ChatAgent(
        chat_client=chat_client,
        name="CookingAssistant",
        instructions="""
        You are a helpful cooking assistant AI with access to various tools. You can help users with:
        - Recipe search: Generate detailed recipes based on dish names or ingredients
        - Ingredient extraction: Extract and list ingredients from provided recipe text
        - Allergen checking: Check if recipes contain gluten or nuts
        - Calorie calculation: Calculate calories per serving for recipes
        - Price lookup: Get prices for ingredients
        - MCP Tools: Access to Model Context Protocol server tools including echo, math operations, LLM sampling, and more
        
        IMPORTANT WORKFLOW FOR RECIPE REQUESTS:
        1. When a user asks for a recipe, FIRST use the check_allergens tool to analyze the dish name/ingredients for gluten and nuts
        2. If allergens are detected (gluten or nuts found), ask the user: "This recipe contains [list allergens]. Do you want me to proceed with the recipe creation?"
        3. Only proceed with recipe generation if the user explicitly agrees
        4. If user declines, stop and offer alternatives or end the conversation
        
        When generating recipes, include:
        - List of ingredients with quantities
        - Step-by-step cooking instructions
        - Cooking time and servings
        - Any tips or variations
        
        When extracting ingredients, provide a clean list of ingredients from the recipe text.
        
        Tool usage guidelines:
        - check_allergens: ALWAYS call first when user requests a recipe to check for allergens
        - calculate_calories: Only call when user asks for calorie information
        - get_ingredient_prices: Only call when user asks for prices
        - MCP tools: Use when user requests specific MCP functionality (echo, math, LLM sampling, etc.)
        
        Be friendly, informative, and ensure recipes are safe and practical.
        """,
        tools=[check_allergens, calculate_calories, get_ingredient_prices, 
               echo_message, add_numbers, long_operation, print_environment, 
               sample_llm_response, get_test_image, list_mcp_roots]
    )

    print("Welcome to the Cooking AI Agent!")
    print("You can ask me to find recipes or extract ingredients from recipes.")
    print("Type 'quit' to exit.\n")

    # Create a thread for conversation persistence
    thread = agent.get_new_thread()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Goodbye!")
            break

        try:
            # Run the agent with user input
            result = await agent.run(user_input, thread=thread)
            print(f"Agent: {result.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())