"""
Blueprint service for high-level Blueprint operations.
"""

import logging
from typing import Any, Dict

from core.connection import UnrealConnection
from core.types import (
    BlueprintSpawnDict,
    ComponentDict,
    PhysicsDict,
    create_blueprint_spawn_params,
    create_component_params,
    create_physics_params,
)

logger = logging.getLogger("UnrealMCP")


class BlueprintService:
    """Service for Blueprint-related operations."""

    def __init__(self, connection: UnrealConnection):
        self.connection = connection

    def create_blueprint(self, name: str, parent_class: str) -> Dict[str, Any]:
        """Create a new Blueprint class."""
        params = {"name": name, "parent_class": parent_class}
        return self.connection.send_command("create_blueprint", params)

    def spawn_blueprint_actor(
        self,
        blueprint_name: str,
        actor_name: str,
        location: list = None,
        rotation: list = None,
        scale: list = None,
    ) -> Dict[str, Any]:
        """Spawn an actor from a Blueprint."""
        params = create_blueprint_spawn_params(
            blueprint_name, actor_name, location, rotation, scale
        )
        return self.connection.send_command("spawn_blueprint_actor", params)

    def add_component(
        self,
        blueprint_name: str,
        component_type: str,
        component_name: str,
        location: list = None,
        rotation: list = None,
        scale: list = None,
        properties: dict = None,
    ) -> Dict[str, Any]:
        """Add a component to a Blueprint."""
        params = create_component_params(
            blueprint_name,
            component_type,
            component_name,
            location,
            rotation,
            scale,
            properties,
        )
        return self.connection.send_command("add_component_to_blueprint", params)

    def set_static_mesh(
        self, blueprint_name: str, component_name: str, static_mesh: str
    ) -> Dict[str, Any]:
        """Set static mesh on a component."""
        params = {
            "blueprint_name": blueprint_name,
            "component_name": component_name,
            "static_mesh": static_mesh,
        }
        return self.connection.send_command("set_static_mesh_properties", params)

    def set_physics_properties(
        self,
        blueprint_name: str,
        component_name: str,
        simulate_physics: bool = True,
        gravity_enabled: bool = True,
        mass: float = 1.0,
        linear_damping: float = 0.01,
        angular_damping: float = 0.0,
    ) -> Dict[str, Any]:
        """Set physics properties on a component."""
        params = create_physics_params(
            simulate_physics, gravity_enabled, mass, linear_damping, angular_damping
        )
        params["blueprint_name"] = blueprint_name
        params["component_name"] = component_name
        return self.connection.send_command("set_physics_properties", params)

    def compile_blueprint(self, blueprint_name: str) -> Dict[str, Any]:
        """Compile a Blueprint."""
        params = {"blueprint_name": blueprint_name}
        return self.connection.send_command("compile_blueprint", params)

    def set_blueprint_property(
        self, blueprint_name: str, property_name: str, property_value: str
    ) -> Dict[str, Any]:
        """Set a property on a Blueprint."""
        params = {
            "blueprint_name": blueprint_name,
            "property_name": property_name,
            "property_value": property_value,
        }
        return self.connection.send_command("set_blueprint_property", params)

    def list_blueprints(self) -> Dict[str, Any]:
        """List all available blueprints in the project."""
        try:
            logger.info("Listing all blueprints")
            result = self.connection.send_command("list_blueprints", {})
            return result
        except Exception as e:
            logger.error(f"Failed to list blueprints: {e}")
            raise

    def blueprint_exists(self, blueprint_name: str) -> Dict[str, Any]:
        """Check if a blueprint with the given name exists."""
        try:
            logger.info(f"Checking if blueprint exists: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("blueprint_exists", params)
            return result
        except Exception as e:
            logger.error(f"Failed to check if blueprint exists: {e}")
            raise

    def get_blueprint_info(self, blueprint_name: str) -> Dict[str, Any]:
        """Get detailed information about a specified blueprint."""
        try:
            logger.info(f"Getting blueprint info: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("get_blueprint_info", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get blueprint info: {e}")
            raise

    def get_blueprint_components(self, blueprint_name: str) -> Dict[str, Any]:
        """Get all components of a blueprint."""
        try:
            logger.info(f"Getting blueprint components: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("get_blueprint_components", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get blueprint components: {e}")
            raise

    def get_blueprint_variables(self, blueprint_name: str) -> Dict[str, Any]:
        """Get all variables of a blueprint."""
        try:
            logger.info(f"Getting blueprint variables: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("get_blueprint_variables", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get blueprint variables: {e}")
            raise

    def get_blueprint_functions(self, blueprint_name: str) -> Dict[str, Any]:
        """Get all functions of a blueprint."""
        try:
            logger.info(f"Getting blueprint functions: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("get_blueprint_functions", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get blueprint functions: {e}")
            raise

    def get_component_properties(self, blueprint_name: str, component_name: str) -> Dict[str, Any]:
        """Get properties of a specific component in a blueprint."""
        try:
            logger.info(f"Getting component properties: {blueprint_name}.{component_name}")
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
            }
            result = self.connection.send_command("get_component_properties", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get component properties: {e}")
            raise

    def set_component_property(
        self, blueprint_name: str, component_name: str, property_name: str, property_value: str
    ) -> Dict[str, Any]:
        """Set a property on a component in a blueprint."""
        try:
            logger.info(f"Setting component property: {blueprint_name}.{component_name}.{property_name}")
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
                "property_name": property_name,
                "property_value": property_value,
            }
            result = self.connection.send_command("set_component_property", params)
            return result
        except Exception as e:
            logger.error(f"Failed to set component property: {e}")
            raise

    def remove_component(self, blueprint_name: str, component_name: str) -> Dict[str, Any]:
        """Remove a component from a blueprint."""
        try:
            logger.info(f"Removing component: {blueprint_name}.{component_name}")
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
            }
            result = self.connection.send_command("remove_component", params)
            return result
        except Exception as e:
            logger.error(f"Failed to remove component: {e}")
            raise

    def rename_component(self, blueprint_name: str, old_name: str, new_name: str) -> Dict[str, Any]:
        """Rename a component in a blueprint."""
        try:
            logger.info(f"Renaming component: {blueprint_name}.{old_name} -> {new_name}")
            params = {
                "blueprint_name": blueprint_name,
                "old_name": old_name,
                "new_name": new_name,
            }
            result = self.connection.send_command("rename_component", params)
            return result
        except Exception as e:
            logger.error(f"Failed to rename component: {e}")
            raise

    def get_blueprint_path(self, blueprint_name: str) -> Dict[str, Any]:
        """Get the file path of a blueprint."""
        try:
            logger.info(f"Getting blueprint path: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("get_blueprint_path", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get blueprint path: {e}")
            raise

    def get_component_hierarchy(self, blueprint_name: str) -> Dict[str, Any]:
        """Get the component hierarchy of a blueprint."""
        try:
            logger.info(f"Getting component hierarchy: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("get_component_hierarchy", params)
            return result
        except Exception as e:
            logger.error(f"Failed to get component hierarchy: {e}")
            raise

    def set_component_transform(
        self,
        blueprint_name: str,
        component_name: str,
        location: list = None,
        rotation: list = None,
        scale: list = None,
    ) -> Dict[str, Any]:
        """Set the transform of a component in a blueprint."""
        try:
            logger.info(f"Setting component transform: {blueprint_name}.{component_name}")
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
            }

            if location:
                params["location"] = location
            if rotation:
                params["rotation"] = rotation
            if scale:
                params["scale"] = scale

            result = self.connection.send_command("set_component_transform", params)
            return result
        except Exception as e:
            logger.error(f"Failed to set component transform: {e}")
            raise

    def delete_blueprint(self, blueprint_name: str) -> Dict[str, Any]:
        """Delete a blueprint."""
        try:
            logger.info(f"Deleting blueprint: {blueprint_name}")
            params = {"blueprint_name": blueprint_name}
            result = self.connection.send_command("delete_blueprint", params)
            return result
        except Exception as e:
            logger.error(f"Failed to delete blueprint: {e}")
            raise

    def duplicate_blueprint(self, blueprint_name: str, new_name: str) -> Dict[str, Any]:
        """Duplicate a blueprint with a new name."""
        try:
            logger.info(f"Duplicating blueprint: {blueprint_name} -> {new_name}")
            params = {
                "blueprint_name": blueprint_name,
                "new_name": new_name,
            }
            result = self.connection.send_command("duplicate_blueprint", params)
            return result
        except Exception as e:
            logger.error(f"Failed to duplicate blueprint: {e}")
            raise
