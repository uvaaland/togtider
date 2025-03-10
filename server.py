import os
from typing import Dict, Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from pydantic import Field

from jattavagen_departures.service import get_upcoming_departures, format_departures


# Load environment variables
load_dotenv()

# Get Application Insights credentials
API_ENDPOINT = os.getenv("API_ENDPOINT")
SUBSCRIPTION_KEY = os.getenv("SUBSCRIPTION_KEY")
REQUESTOR_REF=os.getenv("REQUESTOR_REF")

# Validate environment variables
if not API_ENDPOINT or not SUBSCRIPTION_KEY or not REQUESTOR_REF:
    raise ValueError("API_ENDPOINT, SUBSCRIPTION_KEY and REQUESTOR_REF must be set in .env file")

# Create an MCP server
mcp = FastMCP(
    name="Togtider", 
    log_level="DEBUG", 
    debug=True, 
    port=8080
)

@mcp.tool()
def togtider(
#    station: str = Field(description="The train station to get departures for", default="Jåttåvågen"), 
    ctx: Context = Field(description="MCP context")
) -> Dict[str, Any]:
    """
    Endpoint to get departures from Jåttåvågen station.
    Returns JSON with northbound and southbound departures.
    """
    deps = get_upcoming_departures()
    formatted = format_departures(deps)
        
    # Add metadata to the response
    return  {
        "data": formatted,
        "station": "Jåttåvågen",
        "timestamp": formatted.get("timestamp", None)
    }

if __name__ == "__main__":
    mcp.run(transport="sse")

# Alternatively run with: mcp run server.py --transport sse
# Or with MCP Inspector with: npx @modelcontextprotocol/inspector