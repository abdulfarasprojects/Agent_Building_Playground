from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

def fees_percentage(card_type: str) -> dict:
    """Determines the fees percentage based on the card type.

    Args:
        card_type (str): The type of card (e.g., visa, mastercard, amex).

    Returns:
        dict: status and fee_percentage or error_message.
    """
    fees = {
        "visa": 2.0,
        "mastercard": 2.5,
        "amex": 3.0
    }
    card_type_lower = card_type.lower()
    if card_type_lower in fees:
        return {"status": "success", "fee_percentage": fees[card_type_lower]}
    else:
        return {"status": "error", "error_message": f"Unknown card type '{card_type}'. Supported types: visa, mastercard, amex."}

def get_conversion_rate(from_currency: str, to_currency: str) -> dict:
    """Determines the conversion rate between two currencies.

    Args:
        from_currency (str): The source currency code (e.g., USD, EUR).
        to_currency (str): The target currency code (e.g., USD, EUR).

    Returns:
        dict: status and rate or error_message.
    """
    # Hardcoded rates for demonstration. In production, replace with API call for real-time rates.
    rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0},
        'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.0},
        'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.0},
        'JPY': {'USD': 0.0091, 'EUR': 0.0078, 'GBP': 0.0067}
    }
    if from_currency in rates and to_currency in rates[from_currency]:
        return {"status": "success", "rate": rates[from_currency][to_currency]}
    else:
        return {"status": "error", "error_message": f"Conversion rate from {from_currency} to {to_currency} not available."}

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
    instruction="You are a helpful agent for currency conversion. Use the fees_percentage tool to get the fee based on card type, get_conversion_rate to get the exchange rate, and then use the calculation_agent to compute the total amount accurately via code execution. Fees are deducted from the sending currency amount before conversion. Ensure no calculations are done by the LLM; delegate to the calculation_agent.",
    tools=[fees_percentage, get_conversion_rate, AgentTool(agent=calculation_agent)],
)