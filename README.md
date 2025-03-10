# Togtider

A Python application that fetches and displays train departure information for Jåttåvågen station in Stavanger, Norway, designed specifically as an MCP (Model Context Protocol) integration for Claude Desktop.

## Features

- Fetches real-time train departure information from Bane NOR API
- Groups departures by direction (northbound/southbound)
- Shows both scheduled and actual departure times
- Identifies delayed departures
- Provides seamless integration with Claude Desktop via MCP

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- Claude Desktop application

## Installation

1. Clone the repository:
```bash
git clone https://github.com/uvaaland/togtider.git
cd togtider
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage: Integration with Claude Desktop (MCP)

Togtider is designed as an MCP (Model Context Protocol) tool for Claude Desktop, allowing Claude to fetch real-time train departure information from Jåttåvågen station.

### Setting up MCP Integration on macOS

1. Ensure the repository is cloned to your local machine
2. Modify your Claude Desktop configuration:

```bash
# Open the Claude Desktop config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

3. Add the togtider MCP configuration to the `mcpServers` section:

```json
"togtider": {
  "command": "python",
  "args": [
    "-m",
    "mcp_tool",
    "/path/to/your/togtider/directory"
  ]
}
```

Replace `/path/to/your/togtider/directory` with the actual path to the repository on your system.

Alternatively, if you're using environment management tools like `uv` or `conda`, configure it like this:

```json
"togtider": {
  "command": "uv",
  "args": [
    "--directory",
    "/path/to/your/togtider",
    "run",
    "mcp_tool.py"
  ]
}
```

### Setting up MCP Integration on Windows

1. Ensure the repository is cloned to your local machine
2. Locate and modify your Claude Desktop configuration file:
   - Typically found at `%APPDATA%\Claude\claude_desktop_config.json`
   - You can open this file using Notepad or any text editor

3. Add the togtider MCP configuration to the `mcpServers` section:

```json
"togtider": {
  "command": "python",
  "args": [
    "-m",
    "mcp_tool",
    "C:\\path\\to\\your\\togtider\\directory"
  ]
}
```

Replace `C:\\path\\to\\your\\togtider\\directory` with the actual path to the repository on your system, using double backslashes for directory separators.

### Using Togtider in Claude Desktop

Once configured, you can ask Claude to fetch train departure information by using prompts like:

- "Show me the upcoming train departures from Jåttåvågen station"
- "Are there any delayed trains at Jåttåvågen?"
- "When is the next train to Stavanger from Jåttåvågen?"

Claude will use the togtider tool to fetch and display real-time departure information.

## Response Format

The tool returns a JSON object with the following structure:

```json
{
  "data": {
    "timestamp": "2025-03-10T12:45:30.123456",
    "southbound": [
      {
        "aimed": "10:32",
        "actual": "10:36", 
        "destination": "Nærbø",
        "status": "delayed"
      },
      // More departures...
    ],
    "northbound": [
      {
        "aimed": "10:37",
        "actual": "10:37",
        "destination": "Stavanger",
        "status": "on schedule"
      },
      // More departures...
    ]
  },
  "station": "Jåttåvågen"
}
```

## Testing

Run the tests with:
```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Acknowledgments

- Data provided by [Bane NOR](https://www.banenor.no/)
- Uses the SIRI-ET API standard for public transport information
