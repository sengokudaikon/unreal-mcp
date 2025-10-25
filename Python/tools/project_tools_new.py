"""
Project Tools for Unreal MCP - Refactored with service architecture.
"""

import logging
from typing import Any, Dict

from mcp.server.fastmcp import Context, FastMCP

from core.types import Result
from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_project_tools(mcp: FastMCP):
    """Register Project tools with the MCP server."""

    @mcp.tool()
    def create_input_mapping(
        ctx: Context, action_name: str, key: str, input_type: str = "Action"
    ) -> Dict[str, Any]:
        """Create an input mapping for the project."""
        try:
            service = get_service_manager().project_service
            result = service.create_input_mapping(action_name, key, input_type)
            return _handle_service_result(result, "create_input_mapping")
        except Exception as e:
            return _handle_error("create_input_mapping", e)


def _handle_service_result(result: Result, operation: str) -> Dict[str, Any]:
    """Handle service result and convert to MCP response format."""
    if result.is_success:
        response_data = result.get_value()
        if response_data.get("status") == "error":
            logger.error(f"Unreal error in {operation}: {response_data.get('error')}")
            return {
                "success": False,
                "message": response_data.get("error", "Unknown Unreal error"),
            }
        logger.info(f"Successfully completed {operation}")
        return response_data
    else:
        logger.error(f"Service error in {operation}: {result.get_error()}")
        return {"success": False, "message": result.get_error()}


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}
