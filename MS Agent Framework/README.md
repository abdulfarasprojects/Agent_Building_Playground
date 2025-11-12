# Cooking AI Agent

An interactive console-based AI agent that helps with cooking recipes and ingredient extraction using GitHub models and Microsoft Agent Framework.

## Features

- **Recipe Search**: Generate detailed recipes based on dish names or ingredients
- **Ingredient Extraction**: Extract ingredients from provided recipe text
- **Allergen Checking**: Check recipes for gluten and nut allergens
- **Calorie Calculation**: Calculate calories per serving for recipes
- **Price Lookup**: Get ingredient prices
- **MCP Tools**: Access to Model Context Protocol server tools including:
  - Echo messages
  - Math operations (addition)
  - Long-running operations with progress
  - Environment variable inspection
  - LLM sampling
  - Test image generation
  - MCP roots listing
- **Safety Workflow**: Automatically checks for allergens before recipe generation and asks for user confirmation

## Safety Workflow

When you request a recipe, the agent follows this safety workflow:

1. **Allergen Check**: Automatically analyzes the dish for gluten and nuts
2. **User Confirmation**: If allergens are detected, asks: "This recipe contains [allergens]. Do you want me to proceed?"
3. **Proceed or Stop**: Only generates the recipe if you explicitly agree
4. **Safe Cooking**: Ensures user awareness of potential allergens
- Interactive console interface for easy conversation

## Prerequisites

- Python 3.8+
- GitHub Personal Access Token with access to GitHub Models

## Setup

1. Clone or navigate to the project directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your GitHub token:
   Create a `.env` file in the project directory and add:
   ```
   GITHUB_TOKEN=your_github_personal_access_token
   ```

## Usage

### Console App
Run the agent in the terminal:
```bash
python cooking_agent.py
```

### Web UI
Run the web-based UI:
```bash
python -m uvicorn ui:app --reload
```
Then open http://127.0.0.1:8000 in your browser.

Example interactions:
- "Give me a recipe for chicken curry" (no allergens, proceeds directly)
- "Give me a recipe for pasta primavera" (may contain gluten, asks for confirmation)
- "Extract ingredients from this recipe: [paste recipe text]"
- "Check if this recipe contains gluten: [recipe text]"
- "How many calories per serving in this recipe?"
- "What's the price of chicken and rice?"
- "Echo this message: Hello World"
- "Add 15 and 27"
- "Show me the environment variables"
- "Generate a response to: What is AI?"

Type 'quit' or 'exit' to end the conversation.

## Model Selection

Uses `xai/grok-3` via GitHub Models for:
- Advanced reasoning capabilities from xAI
- Good for complex recipe generation and analysis
- Innovative model for cooking assistance

## Troubleshooting

- **Import errors**: Ensure you're using the virtual environment and dependencies are installed
- **Token errors**: Verify your GITHUB_TOKEN is set correctly
- **Model access**: Ensure your GitHub token has access to GitHub Models

## Dependencies

- Microsoft Agent Framework (Azure AI integration)
- OpenAI Python client
- MCP (Model Context Protocol) client and server-everything package