---
name: dbschenker-mcp-server
description: MCP Server for tracking DB Schenker Shipments. Use when you want to get the live details and history of a DB Schenker shipment.
---
## Configuration

{
  "command": "uvx",
  "args": ["dbschenker-mcp-server"],
}

## Tools

### get_shipment_info
Get the live details and history of a DB Schenker shipment.
- `reference_number` (string): The DB Schenker reference number.