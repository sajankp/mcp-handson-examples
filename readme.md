# MCP Weather Tool Server

This project is a demonstration of the `mcp` library to create a tool server that provides weather-related information. It also includes other example tools and resources.

This is intended as a hands-on learning project for understanding how an MCP server works.

## Quick Start

1. Start the MCP server by running:
```bash
./run.sh
```

2. Create a `.vscode/mcp.json` file with the following content:
```json
{
	"servers": {
		"weather-http": {
			"url": "http://localhost:8000/mcp",
			"type": "http"
		}
	},
	"inputs": []
}
```
This will start the weather_streamable_http server that you can connect to via the MCP protocol.

## Features

This server exposes several tools and resources:

### Weather Tools

*   **`get_alerts(state: str)`**: Get weather alerts for a US state.
    *   `state`: Two-letter US state code (e.g., CA, NY).
*   **`get_forecast(latitude: float, longitude: float)`**: Get the weather forecast for a specific location.
    *   `latitude`: The latitude of the location.
    *   `longitude`: The longitude of the location.

### Other Tools

*   **`add_2_numbers(a: int, b: int)`**: Adds two numbers together.
*   **`greet_user_formal_tool(name: str)`**: Greets a user formally.
*   **`greet_user_street_style_tool(name: str)`**: Greets a user in a "street" style.

### Prompts

*   **`greet_user_prompt(name: str)`**: A prompt that will greet the user '''Laurent''' formally, and all other users in a "street" style.

### Resources

*   **`resource://weather_glossary/`**: Retrieves a full glossary of weather-related terms.
*   **`resource://weather_glossary_term/{word}`**: Retrieves the definition of a specific term from the weather glossary.

## Setup and Installation

1.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

This project includes three different implementations for running the MCP server.

### 1. Standard I/O (stdio)

This runs the server over standard input/output.

```bash
python weather.py
```

### 2. Server-Sent Events (SSE)

This runs the server using Server-Sent Events.

```bash
python weather_sse.py
```

### 3. Streamable HTTP Server

This runs the server as a streamable HTTP application using `uvicorn`. This is the most feature-rich example, including the glossary resources and extra tools.

You can run it using the provided shell script:

```bash
./run.sh
```

This will start the server on `http://localhost:8000`.
