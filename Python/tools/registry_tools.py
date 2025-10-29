"""
Registry Tools for Unreal MCP - Refactored with service architecture.

This module provides MCP tools for registry operations using the service layer.
Registry tools allow querying what's available and supported in the API.
"""

import logging
from typing import Any, Dict

from mcp.server.fastmcp import Context, FastMCP

from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_registry_tools(mcp: FastMCP):
    """Register Registry tools with the MCP server."""

    @mcp.tool()
    def get_available_api_methods(ctx: Context) -> Dict[str, Any]:
        """Get all available API methods organized by category."""
        try:
            service = get_service_manager().registry_service
            result = service.get_available_api_methods()
            return _handle_service_result(result, "get_available_api_methods")
        except Exception as e:
            return _handle_error("get_available_api_methods", e)

    @mcp.tool()
    def get_supported_parent_classes(ctx: Context) -> Dict[str, Any]:
        """Get all supported parent classes for Blueprint creation."""
        try:
            service = get_service_manager().registry_service
            result = service.get_supported_parent_classes()
            return _handle_service_result(result, "get_supported_parent_classes")
        except Exception as e:
            return _handle_error("get_supported_parent_classes", e)

    @mcp.tool()
    def get_supported_component_types(ctx: Context) -> Dict[str, Any]:
        """Get all supported component types."""
        try:
            service = get_service_manager().registry_service
            result = service.get_supported_component_types()
            return _handle_service_result(result, "get_supported_component_types")
        except Exception as e:
            return _handle_error("get_supported_component_types", e)


def _handle_service_result(result: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """Handle service result - just pass through C++ command response."""
    logger.info(f"Completed {operation}")
    return result


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}