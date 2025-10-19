import argparse
import json
from typing import Any
import urllib
import httpx
from mcp.server.fastmcp import FastMCP
import uvicorn

# Initialize FastMCP server
mcp = FastMCP("weather", stateless_http=True, debug=True)

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


# Helper functions
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
            Event: {props.get('event', 'Unknown')}
            Area: {props.get('areaDesc', 'Unknown')}
            Severity: {props.get('severity', 'Unknown')}
            Description: {props.get('description', 'No description available')}
            Instructions: {props.get('instruction', 'No specific instructions provided')}
            """


# Tool implementations
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
                    {period['name']}:
                    Temperature: {period['temperature']}°{period['temperatureUnit']}
                    Wind: {period['windSpeed']} {period['windDirection']}
                    Forecast: {period['detailedForecast']}
                    """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


@mcp.tool(description="Adds two numbers together")
async def add_2_numbers(a: int, b: int) -> int:
    return a + b


@mcp.resource(
    uri="resource://weather_glossary/",
    title="Weather API Glossary",
    description="A Glossary from the weather API to better understand the terms used in the report",
)
async def get_glossary() -> str:
    with open("glossary.json", "r") as file:
        json_file = file.read()
        glossary = json.loads(json_file)["glossary"]
        return glossary


@mcp.resource(
    uri="resource://weather_glossary_term/{word}",
    title="Weather API Glossary",
    description="Get a particuar word's information from the Glossary from weather API to better understand the words",
)
async def get_term_from_glossary(word) -> str:
    with open("glossary.json", "r") as file:
        json_file = file.read()
        glossary = json.loads(json_file)["glossary"]
        glossary_dict = {x["term"]: x["definition"] for x in glossary}
    word = urllib.parse.unquote(word)
    result = glossary_dict.get(word, "Term not found in glossary")
    return result


@mcp.tool()
async def greet_user_formal_tool(name:str) -> str:
    """
    A tool that returns a greeting message in a very formal tone
    Args:
        name (str): The name of the person to greet.
    Returns:
        str: A formal greeting message for the given name.
    """
    return f"Good day to you, {name}. I trust this message finds you well."

@mcp.tool()
async def greet_user_street_style_tool(name:str) -> str:
    """
    A tool that returns a greeting message in street style
    Args:
        name (str): The name of the person to greet.
    Returns:
        str: A street style greeting message for the given name.
    """
    return f"Yo {name}! Wassup? You good?"

@mcp.prompt()
def greet_user_prompt(name: str) -> str:
    """Generates a message asking for a greeting"""
    return f"""
    Return a greeting message for a user called '{name}'. 
    if the user is called 'Laurent', use a formal style, else use a street style.
    """



mcp_app = mcp.streamable_http_app()
