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
