"""
Blueprint Tools for Unreal MCP - Refactored with service architecture.

This module provides MCP tools for Blueprint operations using the service layer.
"""

import logging
from typing import Any, Dict, List

from mcp.server.fastmcp import Context, FastMCP

from services.service_manager import get_service_manager

logger = logging.getLogger("UnrealMCP")


def register_blueprint_tools(mcp: FastMCP):
    """Register Blueprint tools with the MCP server."""

    @mcp.tool()
    def create_blueprint(ctx: Context, name: str, parent_class: str) -> Dict[str, Any]:
        """Create a new Blueprint class."""
        try:
            service = get_service_manager().blueprint_service
            result = service.create_blueprint(name, parent_class)
            return _handle_service_result(result, "create_blueprint")
        except Exception as e:
            return _handle_error("create_blueprint", e)

    @mcp.tool()
    def spawn_blueprint_actor(
        ctx: Context,
        blueprint_name: str,
        actor_name: str,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None,
    ) -> Dict[str, Any]:
        """Spawn an actor from a Blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.spawn_blueprint_actor(
                blueprint_name, actor_name, location, rotation, scale
            )
            return _handle_service_result(result, "spawn_blueprint_actor")
        except Exception as e:
            return _handle_error("spawn_blueprint_actor", e)

    @mcp.tool()
    def add_component_to_blueprint(
        ctx: Context,
        blueprint_name: str,
        component_type: str,
        component_name: str,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None,
        component_properties: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Add a component to a Blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.add_component(
                blueprint_name,
                component_type,
                component_name,
                location,
                rotation,
                scale,
                component_properties,
            )
            return _handle_service_result(result, "add_component_to_blueprint")
        except Exception as e:
            return _handle_error("add_component_to_blueprint", e)

    @mcp.tool()
    def set_static_mesh_properties(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        static_mesh: str = "/Engine/BasicShapes/Cube.Cube",
    ) -> Dict[str, Any]:
        """Set static mesh properties on a component."""
        try:
            service = get_service_manager().blueprint_service
            result = service.set_static_mesh(
                blueprint_name, component_name, static_mesh
            )
            return _handle_service_result(result, "set_static_mesh_properties")
        except Exception as e:
            return _handle_error("set_static_mesh_properties", e)

    @mcp.tool()
    def set_physics_properties(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        simulate_physics: bool = True,
        gravity_enabled: bool = True,
        mass: float = 1.0,
        linear_damping: float = 0.01,
        angular_damping: float = 0.0,
    ) -> Dict[str, Any]:
        """Set physics properties on a component."""
        try:
            service = get_service_manager().blueprint_service
            result = service.set_physics_properties(
                blueprint_name,
                component_name,
                simulate_physics,
                gravity_enabled,
                mass,
                linear_damping,
                angular_damping,
            )
            return _handle_service_result(result, "set_physics_properties")
        except Exception as e:
            return _handle_error("set_physics_properties", e)

    @mcp.tool()
    def compile_blueprint(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Compile a Blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.compile_blueprint(blueprint_name)
            return _handle_service_result(result, "compile_blueprint")
        except Exception as e:
            return _handle_error("compile_blueprint", e)

    @mcp.tool()
    def set_blueprint_property(
        ctx: Context, blueprint_name: str, property_name: str, property_value: str
    ) -> Dict[str, Any]:
        """Set a property on a Blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.set_blueprint_property(
                blueprint_name, property_name, property_value
            )
            return _handle_service_result(result, "set_blueprint_property")
        except Exception as e:
            return _handle_error("set_blueprint_property", e)

    @mcp.tool()
    def list_blueprints(ctx: Context) -> Dict[str, Any]:
        """List all available blueprints in the project."""
        try:
            service = get_service_manager().blueprint_service
            result = service.list_blueprints()
            return _handle_service_result(result, "list_blueprints")
        except Exception as e:
            return _handle_error("list_blueprints", e)

    @mcp.tool()
    def blueprint_exists(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Check if a blueprint with the given name exists."""
        try:
            service = get_service_manager().blueprint_service
            result = service.blueprint_exists(blueprint_name)
            return _handle_service_result(result, "blueprint_exists")
        except Exception as e:
            return _handle_error("blueprint_exists", e)

    @mcp.tool()
    def get_blueprint_info(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Get detailed information about a specified blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_blueprint_info(blueprint_name)
            return _handle_service_result(result, "get_blueprint_info")
        except Exception as e:
            return _handle_error("get_blueprint_info", e)

    @mcp.tool()
    def get_blueprint_components(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Get all components of a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_blueprint_components(blueprint_name)
            return _handle_service_result(result, "get_blueprint_components")
        except Exception as e:
            return _handle_error("get_blueprint_components", e)

    @mcp.tool()
    def get_blueprint_variables(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Get all variables of a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_blueprint_variables(blueprint_name)
            return _handle_service_result(result, "get_blueprint_variables")
        except Exception as e:
            return _handle_error("get_blueprint_variables", e)

    @mcp.tool()
    def get_blueprint_functions(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Get all functions of a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_blueprint_functions(blueprint_name)
            return _handle_service_result(result, "get_blueprint_functions")
        except Exception as e:
            return _handle_error("get_blueprint_functions", e)

    @mcp.tool()
    def get_component_properties(ctx: Context, blueprint_name: str, component_name: str) -> Dict[str, Any]:
        """Get properties of a specific component in a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_component_properties(blueprint_name, component_name)
            return _handle_service_result(result, "get_component_properties")
        except Exception as e:
            return _handle_error("get_component_properties", e)

    @mcp.tool()
    def set_component_property(
        ctx: Context, blueprint_name: str, component_name: str, property_name: str, property_value: str
    ) -> Dict[str, Any]:
        """Set a property on a component in a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.set_component_property(blueprint_name, component_name, property_name, property_value)
            return _handle_service_result(result, "set_component_property")
        except Exception as e:
            return _handle_error("set_component_property", e)

    @mcp.tool()
    def remove_component(ctx: Context, blueprint_name: str, component_name: str) -> Dict[str, Any]:
        """Remove a component from a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.remove_component(blueprint_name, component_name)
            return _handle_service_result(result, "remove_component")
        except Exception as e:
            return _handle_error("remove_component", e)

    @mcp.tool()
    def rename_component(ctx: Context, blueprint_name: str, old_name: str, new_name: str) -> Dict[str, Any]:
        """Rename a component in a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.rename_component(blueprint_name, old_name, new_name)
            return _handle_service_result(result, "rename_component")
        except Exception as e:
            return _handle_error("rename_component", e)

    @mcp.tool()
    def get_blueprint_path(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Get the file path of a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_blueprint_path(blueprint_name)
            return _handle_service_result(result, "get_blueprint_path")
        except Exception as e:
            return _handle_error("get_blueprint_path", e)

    @mcp.tool()
    def get_component_hierarchy(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Get the component hierarchy of a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.get_component_hierarchy(blueprint_name)
            return _handle_service_result(result, "get_component_hierarchy")
        except Exception as e:
            return _handle_error("get_component_hierarchy", e)

    @mcp.tool()
    def set_component_transform(
        ctx: Context,
        blueprint_name: str,
        component_name: str,
        location: List[float] = None,
        rotation: List[float] = None,
        scale: List[float] = None,
    ) -> Dict[str, Any]:
        """Set the transform of a component in a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.set_component_transform(blueprint_name, component_name, location, rotation, scale)
            return _handle_service_result(result, "set_component_transform")
        except Exception as e:
            return _handle_error("set_component_transform", e)

    @mcp.tool()
    def delete_blueprint(ctx: Context, blueprint_name: str) -> Dict[str, Any]:
        """Delete a blueprint."""
        try:
            service = get_service_manager().blueprint_service
            result = service.delete_blueprint(blueprint_name)
            return _handle_service_result(result, "delete_blueprint")
        except Exception as e:
            return _handle_error("delete_blueprint", e)

    @mcp.tool()
    def duplicate_blueprint(ctx: Context, blueprint_name: str, new_name: str) -> Dict[str, Any]:
        """Duplicate a blueprint with a new name."""
        try:
            service = get_service_manager().blueprint_service
            result = service.duplicate_blueprint(blueprint_name, new_name)
            return _handle_service_result(result, "duplicate_blueprint")
        except Exception as e:
            return _handle_error("duplicate_blueprint", e)


def _handle_service_result(result: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """Handle service result - just pass through C++ command response."""
    logger.info(f"Completed {operation}")
    return result


def _handle_error(operation: str, error: Exception) -> Dict[str, Any]:
    """Handle exceptions and return error response."""
    error_msg = f"Error in {operation}: {error}"
    logger.error(error_msg)
    return {"success": False, "message": error_msg}
