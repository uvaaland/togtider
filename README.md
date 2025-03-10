# Togtider

A Python application that fetches and displays train departure information for Jåttåvågen station in Stavanger, Norway.

## Features

- Fetches real-time train departure information from Bane NOR API
- Groups departures by direction (northbound/southbound)
- Shows both scheduled and actual departure times
- Identifies delayed departures
- Provides departure information via:
  - REST API
  - Python module
  - MCP tool integration for Claude Desktop

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- Bane NOR API subscription key

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

4. Configure your API credentials:
```bash
cp jattavagen_departures/config.py.example jattavagen_departures/config.py
```
Then edit `config.py` with your Bane NOR API subscription key.

## Usage

### As a REST API

Run the Flask server:
```bash
python server.py
```

Then access the API at: `http://127.0.0.1:5001/departures`

### As a Python Module

```python
from jattavagen_departures.service import get_upcoming_departures, format_departures

# Get raw departure data
departures = get_upcoming_departures()

# Get formatted departure data
formatted_departures = format_departures(departures)

# Use the data as needed
for direction, deps in formatted_departures.items():
    print(f"{direction.capitalize()} departures:")
    for dep in deps:
        print(f"{dep['aimed']} to {dep['destination']} - {dep['status']}")
```

### Integration with Claude Desktop (MCP)

The togtider application can be integrated with Claude Desktop as an MCP (Model Context Protocol) tool, allowing Claude to fetch real-time train departure information.

#### Setting up MCP Integration on macOS

1. Ensure the repository is cloned to your local machine
2. Configure your API credentials in `config.py`
3. Modify your Claude Desktop configuration:

```bash
# Open the Claude Desktop config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

4. Add the togtider MCP configuration to the `mcpServers` section:

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

#### Setting up MCP Integration on Windows

1. Ensure the repository is cloned to your local machine
2. Configure your API credentials in `config.py`
3. Locate and modify your Claude Desktop configuration file:
   - Typically found at `%APPDATA%\Claude\claude_desktop_config.json`
   - You can open this file using Notepad or any text editor

4. Add the togtider MCP configuration to the `mcpServers` section:

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

#### Using Togtider in Claude Desktop

Once configured, you can ask Claude to fetch train departure information by using prompts like:

- "Show me the upcoming train departures from Jåttåvågen station"
- "Are there any delayed trains at Jåttåvågen?"
- "When is the next train to Stavanger from Jåttåvågen?"

Claude will use the togtider tool to fetch and display real-time departure information.

## API Response Format

The API returns a JSON object with the following structure:

```json
{
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
}
```

## Docker Deployment

The project includes a Dockerfile and docker-compose.yml for easy deployment:

```bash
# Build and start with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f
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
