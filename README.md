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
  - MCP tool integration

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

### As an MCP Tool

```python
from mcp_tool import run_tool

# Get departures
departures = run_tool()
```

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

## Testing

Run the tests with:
```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Data provided by [Bane NOR](https://www.banenor.no/)
- Uses the SIRI-ET API standard for public transport information
