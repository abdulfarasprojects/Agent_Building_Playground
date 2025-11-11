# Currency Conversion Agent

This is an AI agent built using Google ADK that converts currencies and calculates conversion fees using specialized tools.

## Features

- **Fees Percentage Tool**: Determines conversion fees based on card type (Visa: 2%, Mastercard: 2.5%, Amex: 3%).
- **Conversion Rate Tool**: Provides exchange rates between currencies (hardcoded for demo; replace with API for real-time rates).
- **Calculation Agent Tool**: Uses Python code execution to perform accurate calculations, ensuring no computations are done by the LLM. Fees are deducted from the sending currency amount before applying the conversion rate.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Set up your Google API key in currency_agent/.env

3. Run the agent:
   adk web

Then, select currency_conversion_agent and chat with it.

## Example Prompts

- Convert 100 USD to EUR using Visa card
- What is the total amount for converting 50 GBP to JPY with Mastercard?
- Calculate fees for 200 EUR to USD with Amex