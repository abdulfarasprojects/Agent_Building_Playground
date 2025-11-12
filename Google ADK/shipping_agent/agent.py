from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def coordinate_shipping(num_containers: int, tool_context: ToolContext) -> str:
    """Coordinates shipping orders with approval workflow.

    Args:
        num_containers (int): Number of containers in the shipping order.
        tool_context (ToolContext): Context for tool execution and approval requests.

    Returns:
        str: Status message about the shipping coordination.
    """
    print(f"DEBUG: coordinate_shipping called with {num_containers} containers")

    if num_containers <= 5:
        # Auto-approve small orders
        result = f"✅ Auto-approved shipping order for {num_containers} containers. Order will be processed immediately."
        print(f"DEBUG: Auto-approved: {result}")
        return result
    else:
        # Check if we already have a confirmation
        if tool_context.tool_confirmation:
            # We have a confirmation response
            if tool_context.tool_confirmation.confirmed:
                result = f"✅ Approved shipping order for {num_containers} containers. Order will be processed."
                tool_context.send_message(result)  # Send confirmation message
            else:
                result = f"❌ Cancelled shipping order for {num_containers} containers. Order has been cancelled."
                tool_context.send_message(result)  # Send cancellation message
        else:
            # No confirmation yet, request it
            tool_context.request_confirmation(
                hint=f"Large shipping order detected: {num_containers} containers. Please approve or reject this shipment."
            )
            # Return error dict to indicate confirmation is needed (similar to built-in tools)
            return {
                'error': f'This shipping order requires approval. Please check the UI to approve or reject the {num_containers} container shipment.'
            }

        print(f"DEBUG: Final result: {result}")
        return result

# Shipping Coordinator Agent
root_agent = Agent(
    name="shipping_coordinator_agent",
    model="gemini-2.0-flash",
    description="Agent to coordinate shipping orders with approval workflow for large shipments",
    instruction="You are a shipping coordinator agent. When given a shipping request with number of containers, use the coordinate_shipping tool to handle the approval process. For small orders (≤5 containers), they are auto-approved. For large orders (>5 containers), the tool will request approval and show an error message until approval is granted. Always provide clear status updates to the user about the shipping coordination outcome.",
    tools=[coordinate_shipping],
)