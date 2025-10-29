"""
Project Tools for Unreal MCP - Refactored with service architecture.
"""

import logging
from typing import Any, Dict

from mcp.server.fastmcp import Context, FastMCP

from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_project_tools(mcp: FastMCP):
    """Register Project tools with the MCP server."""

    @mcp.tool()
    def create_legacy_input_mapping(
        ctx: Context, action_name: str, key: str, input_type: str = "Action"
    ) -> Dict[str, Any]:
        """Create a legacy input mapping for the project (deprecated, use enhanced input system)."""
        try:
            service = get_service_manager().project_service
            result = service.create_legacy_input_mapping(action_name, key, input_type)
            return _handle_service_result(result, "create_legacy_input_mapping")
        except Exception as e:
            return _handle_error("create_legacy_input_mapping", e)


def _handle_service_result(result: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """Handle service result - just pass through C++ command response."""
    logger.info(f"Completed {operation}")
    return result


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}
