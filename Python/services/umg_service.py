"""
UMG service for high-level widget operations.
"""

import logging
from typing import Any, Dict, List, Optional

from core.connection import UnrealConnection
from core.types import Result, Vector3

logger = logging.getLogger("UnrealMCP")


class UMGService:
    """Service for UMG widget operations."""

    def __init__(self, connection: UnrealConnection):
        self.connection = connection

    def create_widget_blueprint(
        self, widget_name: str, parent_class: str = "UserWidget", path: str = "/Game/UI"
    ) -> Result[Dict[str, Any]]:
        """Create a new UMG Widget Blueprint."""
        params = {
            "widget_name": widget_name,
            "parent_class": parent_class,
            "path": path,
        }
        return self.connection.send_command("create_umg_widget_blueprint", params)

    def add_text_block(
        self,
        widget_name: str,
        text_block_name: str,
        text: str = "",
        position: Vector3 = None,
        size: List[int] = None,
        font_size: int = 12,
        color: List[float] = None,
    ) -> Result[Dict[str, Any]]:
        """Add a Text Block widget to a UMG Widget Blueprint."""
        if position is None:
            position = Vector3(0, 0, 0)
        if size is None:
            size = [200, 50]
        if color is None:
            color = [1, 1, 1, 1]

        params = {
            "widget_name": widget_name,
            "text_block_name": text_block_name,
            "text": text,
            "position": [position.x, position.y],
            "size": size,
            "font_size": font_size,
            "color": color,
        }
        return self.connection.send_command("add_text_block_to_widget", params)

    def add_button(
        self,
        widget_name: str,
        button_name: str,
        text: str = "",
        position: Vector3 = None,
        size: List[int] = None,
        font_size: int = 12,
        color: List[float] = None,
        background_color: List[float] = None,
    ) -> Result[Dict[str, Any]]:
        """Add a Button widget to a UMG Widget Blueprint."""
        if position is None:
            position = Vector3(0, 0, 0)
        if size is None:
            size = [200, 50]
        if color is None:
            color = [1, 1, 1, 1]
        if background_color is None:
            background_color = [0.1, 0.1, 0.1, 1]

        params = {
            "widget_name": widget_name,
            "button_name": button_name,
            "text": text,
            "position": [position.x, position.y],
            "size": size,
            "font_size": font_size,
            "color": color,
            "background_color": background_color,
        }
        return self.connection.send_command("add_button_to_widget", params)

    def bind_widget_event(
        self,
        widget_name: str,
        widget_component_name: str,
        event_name: str,
        function_name: str = "",
    ) -> Result[Dict[str, Any]]:
        """Bind an event on a widget component to a function."""
        params = {
            "widget_name": widget_name,
            "widget_component_name": widget_component_name,
            "event_name": event_name,
        }
        if function_name:
            params["function_name"] = function_name

        return self.connection.send_command("bind_widget_event", params)

    def add_widget_to_viewport(
        self, widget_name: str, z_order: int = 0
    ) -> Result[Dict[str, Any]]:
        """Add a Widget Blueprint instance to the viewport."""
        params = {"widget_name": widget_name, "z_order": z_order}
        return self.connection.send_command("add_widget_to_viewport", params)

    def set_text_block_binding(
        self,
        widget_name: str,
        text_block_name: str,
        binding_property: str,
        binding_type: str = "Text",
    ) -> Result[Dict[str, Any]]:
        """Set up a property binding for a Text Block widget."""
        params = {
            "widget_name": widget_name,
            "text_block_name": text_block_name,
            "binding_property": binding_property,
            "binding_type": binding_type,
        }
        return self.connection.send_command("set_text_block_binding", params)
