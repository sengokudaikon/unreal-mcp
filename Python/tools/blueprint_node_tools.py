"""
Blueprint Node Tools for Unreal MCP - Refactored with service architecture.

This module provides MCP tools for blueprint node operations using the service layer.
Blueprint node tools allow manipulation of blueprint graphs including connecting nodes,
adding events, functions, variables, and other node types.
"""

import logging
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context, FastMCP

from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_blueprint_node_tools(mcp: FastMCP):
    """Register Blueprint Node tools with the MCP server."""

    @mcp.tool()
    def connect_blueprint_nodes(
        ctx: Context,
        blueprint_name: str,
        source_node_id: str,
        target_node_id: str,
        source_pin: str,
        target_pin: str,
    ) -> Dict[str, Any]:
        """Connect two blueprint nodes via their pins."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.connect_blueprint_nodes(
                blueprint_name, source_node_id, target_node_id, source_pin, target_pin
            )
            return _handle_service_result(result, "connect_blueprint_nodes")
        except Exception as e:
            return _handle_error("connect_blueprint_nodes", e)

    @mcp.tool()
    def add_blueprint_event_node(
        ctx: Context,
        blueprint_name: str,
        event_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """Add an event node to a blueprint graph."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.add_blueprint_event(blueprint_name, event_name, node_position)
            return _handle_service_result(result, "add_blueprint_event_node")
        except Exception as e:
            return _handle_error("add_blueprint_event_node", e)

    @mcp.tool()
    def add_blueprint_function_node(
        ctx: Context,
        blueprint_name: str,
        function_name: str,
        target: Optional[str] = None,
        node_position: Optional[List[float]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Add a function call node to a blueprint graph."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.add_blueprint_function_call(
                blueprint_name, function_name, target, node_position, params
            )
            return _handle_service_result(result, "add_blueprint_function_node")
        except Exception as e:
            return _handle_error("add_blueprint_function_node", e)

    @mcp.tool()
    def add_blueprint_variable(
        ctx: Context,
        blueprint_name: str,
        variable_name: str,
        variable_type: str,
        is_exposed: bool = False,
    ) -> Dict[str, Any]:
        """Add a variable to a blueprint."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.add_blueprint_variable(
                blueprint_name, variable_name, variable_type, is_exposed
            )
            return _handle_service_result(result, "add_blueprint_variable")
        except Exception as e:
            return _handle_error("add_blueprint_variable", e)

    @mcp.tool()
    def find_blueprint_nodes(
        ctx: Context,
        blueprint_name: str,
        node_type: Optional[str] = None,
        event_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Find nodes in a blueprint graph by type and criteria."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.find_blueprint_nodes(blueprint_name, node_type, event_name)
            return _handle_service_result(result, "find_blueprint_nodes")
        except Exception as e:
            return _handle_error("find_blueprint_nodes", e)

    @mcp.tool()
    def add_blueprint_input_action_node(
        ctx: Context,
        blueprint_name: str,
        action_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """Add a legacy input action node to a blueprint graph."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.add_blueprint_input_action_node(
                blueprint_name, action_name, node_position
            )
            return _handle_service_result(result, "add_blueprint_input_action_node")
        except Exception as e:
            return _handle_error("add_blueprint_input_action_node", e)

    @mcp.tool()
    def add_blueprint_self_reference_node(
        ctx: Context,
        blueprint_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """Add a self reference node to a blueprint graph."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.add_blueprint_self_reference(blueprint_name, node_position)
            return _handle_service_result(result, "add_blueprint_self_reference_node")
        except Exception as e:
            return _handle_error("add_blueprint_self_reference_node", e)

    @mcp.tool()
    def add_blueprint_get_self_component_reference_node(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """Add a self component reference node to a blueprint graph."""
        try:
            service = get_service_manager().blueprint_node_service
            result = service.add_blueprint_get_self_component_reference(
                blueprint_name, component_name, node_position
            )
            return _handle_service_result(result, "add_blueprint_get_self_component_reference_node")
        except Exception as e:
            return _handle_error("add_blueprint_get_self_component_reference_node", e)


def _handle_service_result(result: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """Handle service result - just pass through C++ command response."""
    logger.info(f"Completed {operation}")
    return result


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}