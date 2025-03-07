# mcp_tool.py
"""
Togtider - Train departure times for Jåttåvågen station

This module serves as an MCP integration tool for fetching train departure times
from Jåttåvågen station in Stavanger, Norway.

Usage:
    - Import and call run_tool() from your Python code
    - Run directly with python mcp_tool.py for testing

Returns:
    JSON-compatible dictionary with northbound and southbound departures.
"""
import logging
import json
import sys
from jattavagen_departures.service import get_upcoming_departures, format_departures

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('togtider-mcp')

def run_tool(context=None):
    """
    Entry point for MCP integration.
    
    Args:
        context (dict, optional): Optional context dictionary for future use.
        
    Returns:
        dict: JSON-compatible dictionary with departure information.
        
    Raises:
        Exception: Passes through any exceptions from the underlying service.
    """
    try:
        logger.info("MCP tool invoked")
        if context:
            logger.debug(f"Context provided: {context}")
            
        departures = get_upcoming_departures()
        formatted = format_departures(departures)
        
        # Add metadata to the response
        response = {
            "data": formatted,
            "station": "Jåttåvågen",
            "timestamp": formatted.get("timestamp", None)
        }
        
        logger.info("MCP tool execution completed successfully")
        return response
    
    except Exception as e:
        logger.error(f"Error in MCP tool: {str(e)}", exc_info=True)
        # For MCP integration, we might want to return an error object
        # rather than raising an exception
        return {
            "error": True,
            "message": str(e),
            "type": type(e).__name__
        }

def display_help():
    """Display help information about this tool."""
    help_text = """
Togtider - Train Departure Times for Jåttåvågen

This tool fetches real-time train departures from Jåttåvågen station
in Stavanger, Norway.

Usage:
  python mcp_tool.py             - Run the tool and display departures
  python mcp_tool.py --help      - Display this help message
  python mcp_tool.py --json      - Output as raw JSON
  python mcp_tool.py --pretty    - Output as formatted pretty JSON (default)
  
The tool returns a JSON object with northbound and southbound departures,
including scheduled and actual departure times.
"""
    print(help_text)

if __name__ == "__main__":
    # For local testing
    pretty_output = True
    
    # Simple command line argument parsing
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            display_help()
            sys.exit(0)
        elif sys.argv[1] == "--json":
            pretty_output = False
        elif sys.argv[1] == "--pretty":
            pretty_output = True
    
    try:
        result = run_tool()
        
        if "error" in result and result["error"]:
            print("Error:", result["message"])
            sys.exit(1)
            
        if pretty_output:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, ensure_ascii=False))
            
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        sys.exit(1)
