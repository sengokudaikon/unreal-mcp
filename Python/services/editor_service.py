"""
Editor service for high-level editor operations.
"""

import logging
from typing import Any, Dict, List, Optional

from core.connection import UnrealConnection
from core.types import Transform, Vector3

logger = logging.getLogger("UnrealMCP")


class EditorService:
    """Service for editor-related operations."""

    def __init__(self, connection: UnrealConnection):
        self.connection = connection

    def get_actors_in_level(self) -> Dict[str, Any]:
        """Get a list of all actors in the current level."""
        return self.connection.send_command("get_actors_in_level", {})

    def find_actors_by_name(self, pattern: str) -> Dict[str, Any]:
        """Find actors by name pattern."""
        params = {"pattern": pattern}
        return self.connection.send_command("find_actors_by_name", params)

    def spawn_actor(
        self, name: str, actor_type: str, transform: Transform = None
    ) -> Dict[str, Any]:
        """Spawn an actor in the level."""
        if transform is None:
            transform = Transform(
                location=Vector3(0, 0, 0),
                rotation=Vector3(0, 0, 0),
                scale=Vector3(1, 1, 1),
            )

        params = {
            "actor_name": name,  # C++ plugin expects 'actor_name' not 'name'
            "actor_class": actor_type,  # C++ plugin expects 'actor_class' not 'type'
            **transform.to_dict()
        }
        return self.connection.send_command("spawn_actor", params)

    def delete_actor(self, name: str) -> Dict[str, Any]:
        """Delete an actor from the level."""
        params = {"name": name}
        return self.connection.send_command("delete_actor", params)

    def set_actor_transform(
        self, name: str, transform: Transform
    ) -> Dict[str, Any]:
        """Set the transform of an actor."""
        params = {"name": name, **transform.to_dict()}
        return self.connection.send_command("set_actor_transform", params)

    def get_actor_properties(self, name: str) -> Dict[str, Any]:
        """Get properties of an actor."""
        params = {"name": name}
        return self.connection.send_command("get_actor_properties", params)

    def set_actor_property(self, name: str, property_name: str, property_value: str) -> Dict[str, Any]:
        """Set a property of an actor by name."""
        try:
            logger.info(f"Setting actor property: {name}.{property_name} = {property_value}")
            params = {
                "name": name,
                "property_name": property_name,
                "property_value": property_value,
            }
            return self.connection.send_command("set_actor_property", params)
        except Exception as e:
            logger.error(f"Failed to set actor property: {e}")
            raise

    def focus_viewport(
        self,
        target: str = None,
        location: Vector3 = None,
        distance: float = None,
        orientation: str = None,
    ) -> Dict[str, Any]:
        """Focus the viewport on a target or location."""
        params = {}
        if target:
            params["target"] = target
        if location:
            params["location"] = list(location)
        if distance is not None:
            params["distance"] = distance
        if orientation:
            params["orientation"] = orientation

        return self.connection.send_command("focus_viewport", params)

    def take_screenshot(
        self, filename: str = None, show_ui: bool = True, resolution: List[int] = None
    ) -> Dict[str, Any]:
        """Take a screenshot of the viewport."""
        params = {"show_ui": show_ui}
        if filename:
            params["filename"] = filename
        if resolution:
            params["resolution"] = resolution

        return self.connection.send_command("take_screenshot", params)
