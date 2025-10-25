"""
UMG Tools for Unreal MCP - Refactored with service architecture.
"""

import logging
from typing import Any, Dict, List

from mcp.server.fastmcp import Context, FastMCP

from core.types import Result, Vector3
from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_umg_tools(mcp: FastMCP):
    """Register UMG tools with the MCP server."""

    @mcp.tool()
    def create_umg_widget_blueprint(
        ctx: Context,
        widget_name: str,
        parent_class: str = "UserWidget",
        path: str = "/Game/UI",
    ) -> Dict[str, Any]:
        """Create a new UMG Widget Blueprint."""
        try:
            service = get_service_manager().umg_service
            result = service.create_widget_blueprint(widget_name, parent_class, path)
            return _handle_service_result(result, "create_umg_widget_blueprint")
        except Exception as e:
            return _handle_error("create_umg_widget_blueprint", e)

    @mcp.tool()
    def add_text_block_to_widget(
        ctx: Context,
        widget_name: str,
        text_block_name: str,
        text: str = "",
        position: List[float] = None,
        size: List[int] = None,
        font_size: int = 12,
        color: List[float] = None,
    ) -> Dict[str, Any]:
        """Add a Text Block widget to a UMG Widget Blueprint."""
        try:
            service = get_service_manager().umg_service
            result = service.add_text_block(
                widget_name=widget_name,
                text_block_name=text_block_name,
                text=text,
                position=Vector3.from_list(position or [0.0, 0.0, 0.0]),
                size=size,
                font_size=font_size,
                color=color,
            )
            return _handle_service_result(result, "add_text_block_to_widget")
        except Exception as e:
            return _handle_error("add_text_block_to_widget", e)

    @mcp.tool()
    def add_button_to_widget(
        ctx: Context,
        widget_name: str,
        button_name: str,
        text: str = "",
        position: List[float] = None,
        size: List[int] = None,
        font_size: int = 12,
        color: List[float] = None,
        background_color: List[float] = None,
    ) -> Dict[str, Any]:
        """Add a Button widget to a UMG Widget Blueprint."""
        try:
            service = get_service_manager().umg_service
            result = service.add_button(
                widget_name=widget_name,
                button_name=button_name,
                text=text,
                position=Vector3.from_list(position or [0.0, 0.0, 0.0]),
                size=size,
                font_size=font_size,
                color=color,
                background_color=background_color,
            )
            return _handle_service_result(result, "add_button_to_widget")
        except Exception as e:
            return _handle_error("add_button_to_widget", e)

    @mcp.tool()
    def bind_widget_event(
        ctx: Context,
        widget_name: str,
        widget_component_name: str,
        event_name: str,
        function_name: str = "",
    ) -> Dict[str, Any]:
        """Bind an event on a widget component to a function."""
        try:
            service = get_service_manager().umg_service
            result = service.bind_widget_event(
                widget_name=widget_name,
                widget_component_name=widget_component_name,
                event_name=event_name,
                function_name=function_name,
            )
            return _handle_service_result(result, "bind_widget_event")
        except Exception as e:
            return _handle_error("bind_widget_event", e)

    @mcp.tool()
    def add_widget_to_viewport(
        ctx: Context, widget_name: str, z_order: int = 0
    ) -> Dict[str, Any]:
        """Add a Widget Blueprint instance to the viewport."""
        try:
            service = get_service_manager().umg_service
            result = service.add_widget_to_viewport(widget_name, z_order)
            return _handle_service_result(result, "add_widget_to_viewport")
        except Exception as e:
            return _handle_error("add_widget_to_viewport", e)

    @mcp.tool()
    def set_text_block_binding(
        ctx: Context,
        widget_name: str,
        text_block_name: str,
        binding_property: str,
        binding_type: str = "Text",
    ) -> Dict[str, Any]:
        """Set up a property binding for a Text Block widget."""
        try:
            service = get_service_manager().umg_service
            result = service.set_text_block_binding(
                widget_name=widget_name,
                text_block_name=text_block_name,
                binding_property=binding_property,
                binding_type=binding_type,
            )
            return _handle_service_result(result, "set_text_block_binding")
        except Exception as e:
            return _handle_error("set_text_block_binding", e)


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
