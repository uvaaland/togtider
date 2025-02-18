# mcp_tool.py
from jattavagen_departures.service import get_upcoming_departures, format_departures

def run_tool(context=None):
    """
    Entry point for MCP integration.
    Optionally, a context dict can be provided.
    Returns the departures as a JSON-compatible dict.
    """
    departures = get_upcoming_departures()
    return format_departures(departures)

if __name__ == "__main__":
    # For local testing
    import json
    result = run_tool()
    print(json.dumps(result, indent=2))
