#!/bin/bash
uvicorn weather_streamable_http:mcp_app --port=8000 --reload
