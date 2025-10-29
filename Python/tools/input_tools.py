"""
Input Tools for Unreal MCP - Refactored with service architecture.

This module provides MCP tools for input operations using the service layer.
Input tools allow creation and management of Enhanced Input actions, mapping contexts,
and input bindings.
"""

import logging
from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context, FastMCP

from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_input_tools(mcp: FastMCP):
    """Register Input tools with the MCP server."""

    @mcp.tool()
    def create_enhanced_input_action(
        ctx: Context,
        name: str,
        value_type: str = "Axis1D",
        path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an Enhanced Input Action asset."""
        try:
            service = get_service_manager().input_service
            result = service.create_enhanced_input_action(name, value_type, path)
            return _handle_service_result(result, "create_enhanced_input_action")
        except Exception as e:
            return _handle_error("create_enhanced_input_action", e)

    @mcp.tool()
    def create_input_mapping_context(
        ctx: Context,
        name: str,
        path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an Input Mapping Context asset."""
        try:
            service = get_service_manager().input_service
            result = service.create_input_mapping_context(name, path)
            return _handle_service_result(result, "create_input_mapping_context")
        except Exception as e:
            return _handle_error("create_input_mapping_context", e)

    @mcp.tool()
    def add_enhanced_input_mapping(
        ctx: Context,
        context_path: str,
        action_path: str,
        key: str,
    ) -> Dict[str, Any]:
        """Add a key mapping to an Input Mapping Context."""
        try:
            service = get_service_manager().input_service
            result = service.add_enhanced_input_mapping(context_path, action_path, key)
            return _handle_service_result(result, "add_enhanced_input_mapping")
        except Exception as e:
            return _handle_error("add_enhanced_input_mapping", e)

    @mcp.tool()
    def remove_enhanced_input_mapping(
        ctx: Context,
        context_path: str,
        action_path: str,
        key: str,
    ) -> Dict[str, Any]:
        """Remove a key mapping from an Input Mapping Context."""
        try:
            service = get_service_manager().input_service
            result = service.remove_enhanced_input_mapping(context_path, action_path, key)
            return _handle_service_result(result, "remove_enhanced_input_mapping")
        except Exception as e:
            return _handle_error("remove_enhanced_input_mapping", e)

    @mcp.tool()
    def apply_mapping_context(
        ctx: Context,
        context_path: str,
        priority: int = 0,
    ) -> Dict[str, Any]:
        """Apply an Input Mapping Context."""
        try:
            service = get_service_manager().input_service
            result = service.apply_mapping_context(context_path, priority)
            return _handle_service_result(result, "apply_mapping_context")
        except Exception as e:
            return _handle_error("apply_mapping_context", e)

    @mcp.tool()
    def remove_mapping_context(
        ctx: Context,
        context_path: str,
    ) -> Dict[str, Any]:
        """Remove an applied Input Mapping Context."""
        try:
            service = get_service_manager().input_service
            result = service.remove_mapping_context(context_path)
            return _handle_service_result(result, "remove_mapping_context")
        except Exception as e:
            return _handle_error("remove_mapping_context", e)

    @mcp.tool()
    def clear_all_mapping_contexts(ctx: Context) -> Dict[str, Any]:
        """Clear all applied mapping contexts."""
        try:
            service = get_service_manager().input_service
            result = service.clear_all_mapping_contexts()
            return _handle_service_result(result, "clear_all_mapping_contexts")
        except Exception as e:
            return _handle_error("clear_all_mapping_contexts", e)


def _handle_service_result(result: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """Handle service result - just pass through C++ command response."""
    logger.info(f"Completed {operation}")
    return result


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}