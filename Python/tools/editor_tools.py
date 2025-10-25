"""
Editor Tools for Unreal MCP - Refactored with service architecture.
"""

import logging
from typing import Any, Dict, List

from mcp.server.fastmcp import Context, FastMCP

from core.types import Transform, Vector3
from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_editor_tools(mcp: FastMCP):
    """Register Editor tools with the MCP server."""

    @mcp.tool()
    def get_actors_in_level(ctx: Context) -> Dict[str, Any]:
        """Get a list of all actors in the current level."""
        try:
            service = get_service_manager().editor_service
            result = service.get_actors_in_level()
            return _handle_service_result(result, "get_actors_in_level")
        except Exception as e:
            return _handle_error("get_actors_in_level", e)

    @mcp.tool()
    def find_actors_by_name(ctx: Context, pattern: str) -> Dict[str, Any]:
        """Find actors by name pattern."""
        try:
            service = get_service_manager().editor_service
            result = service.find_actors_by_name(pattern)
            return _handle_service_result(result, "find_actors_by_name")
        except Exception as e:
            return _handle_error("find_actors_by_name", e)

    @mcp.tool()
    def spawn_actor(
        ctx: Context,
        name: str,
        actor_type: str,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None,
    ) -> Dict[str, Any]:
        """Spawn an actor in the level."""
        try:
            transform = Transform(
                location=Vector3.from_list(location or [0.0, 0.0, 0.0]),
                rotation=Vector3.from_list(rotation or [0.0, 0.0, 0.0]),
                scale=Vector3.from_list(scale or [1.0, 1.0, 1.0]),
            )

            service = get_service_manager().editor_service
            result = service.spawn_actor(name, actor_type, transform)
            return _handle_service_result(result, "spawn_actor")
        except Exception as e:
            return _handle_error("spawn_actor", e)

    @mcp.tool()
    def delete_actor(ctx: Context, name: str) -> Dict[str, Any]:
        """Delete an actor from the level."""
        try:
            service = get_service_manager().editor_service
            result = service.delete_actor(name)
            return _handle_service_result(result, "delete_actor")
        except Exception as e:
            return _handle_error("delete_actor", e)

    @mcp.tool()
    def set_actor_transform(
        ctx: Context,
        name: str,
        location: List[float],
        rotation: List[float] = None,
        scale: List[float] = None,
    ) -> Dict[str, Any]:
        """Set the transform of an actor."""
        try:
            transform = Transform(
                location=Vector3.from_list(location),
                rotation=Vector3.from_list(rotation or [0.0, 0.0, 0.0]),
                scale=Vector3.from_list(scale or [1.0, 1.0, 1.0]),
            )

            service = get_service_manager().editor_service
            result = service.set_actor_transform(name, transform)
            return _handle_service_result(result, "set_actor_transform")
        except Exception as e:
            return _handle_error("set_actor_transform", e)

    @mcp.tool()
    def get_actor_properties(ctx: Context, name: str) -> Dict[str, Any]:
        """Get properties of an actor."""
        try:
            service = get_service_manager().editor_service
            result = service.get_actor_properties(name)
            return _handle_service_result(result, "get_actor_properties")
        except Exception as e:
            return _handle_error("get_actor_properties", e)

    @mcp.tool()
    def focus_viewport(
        ctx: Context,
        target: str = None,
        location: List[float] = None,
        distance: float = None,
        orientation: str = None,
    ) -> Dict[str, Any]:
        """Focus the viewport on a target or location."""
        try:
            service = get_service_manager().editor_service
            result = service.focus_viewport(
                target=target,
                location=Vector3.from_list(location) if location else None,
                distance=distance,
                orientation=orientation,
            )
            return _handle_service_result(result, "focus_viewport")
        except Exception as e:
            return _handle_error("focus_viewport", e)

    @mcp.tool()
    def take_screenshot(
        ctx: Context,
        filename: str = None,
        show_ui: bool = True,
        resolution: List[int] = None,
    ) -> Dict[str, Any]:
        """Take a screenshot of the viewport."""
        try:
            service = get_service_manager().editor_service
            result = service.take_screenshot(filename, show_ui, resolution)
            return _handle_service_result(result, "take_screenshot")
        except Exception as e:
            return _handle_error("take_screenshot", e)


def _handle_service_result(result: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """Handle service result - just pass through C++ command response."""
    logger.info(f"Completed {operation}")
    return result


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}
