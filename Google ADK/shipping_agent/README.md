# Shipping Coordinator Agent

A Google ADK agent that demonstrates long-running operations with human approval workflows for shipping coordination.

## Overview

This agent coordinates shipping orders with an intelligent approval system:

- **Small Orders (≤5 containers)**: Auto-approved and processed immediately
- **Large Orders (>5 containers)**: Requires human approval before processing

The agent uses the `ToolContext` to request confirmations for large orders, demonstrating the core pattern of pause → wait for human input → resume.

## Architecture

### Core Components

1. **Shipping Coordinator Agent**: Main agent that handles user requests
2. **coordinate_shipping Tool**: Implements the approval workflow logic
3. **ToolContext Integration**: Handles approval requests and status checking

### Tool Function

```python
def coordinate_shipping(num_containers: int, tool_context: ToolContext) -> str:
    """Coordinates shipping orders with approval workflow."""
    if num_containers <= 5:
        # Auto-approve small orders
        return f"✅ Auto-approved shipping order for {num_containers} containers."
    else:
        # Request approval for large orders
        approval = tool_context.request_confirmation(
            message=f"Large shipping order detected: {num_containers} containers. Do you approve this shipment?",
            options=["approve", "cancel"]
        )
        if approval == "approve":
            return f"✅ Approved shipping order for {num_containers} containers."
        else:
            return f"❌ Cancelled shipping order for {num_containers} containers."
```

## Usage

### Running the Agent

```bash
cd "/path/to/Agent_Building_Playground/Google ADK"
adk run shipping_agent
```

### Example Interactions

**Small Order (Auto-approved):**
```
User: Please coordinate shipping for 3 containers
Agent: ✅ Auto-approved shipping order for 3 containers. Order will be processed immediately.
```

**Large Order (Requires Approval):**
```
User: Please coordinate shipping for 8 containers
Agent: [Requests confirmation from user]
User: approve
Agent: ✅ Approved shipping order for 8 containers. Order will be processed.
```

## Key Features

- **Intelligent Approval Logic**: Automatic approval for small orders, human oversight for large ones
- **ToolContext Integration**: Proper use of ADK's approval mechanism
- **Clear Status Updates**: Informative messages about approval status
- **Error Handling**: Graceful handling of approval decisions

## Testing

Run the test script to verify functionality:

```bash
python test_shipping.py
```

This tests:
- Small order auto-approval
- Large order approval workflow
- Large order cancellation workflow

## Files

- `agent.py`: Main agent definition with the shipping coordination tool
- `config.yaml`: Agent configuration
- `__init__.py`: Package initialization
- `../test_shipping.py`: Tool testing script

## Learning Outcomes

This agent demonstrates:

1. **Long-running Operations**: Pause and resume patterns with human input
2. **ToolContext Usage**: Requesting and handling confirmations
3. **Conditional Logic**: Different behaviors based on input parameters
4. **User Experience**: Clear communication of approval status
5. **Google ADK Patterns**: Proper agent and tool structure