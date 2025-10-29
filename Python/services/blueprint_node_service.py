"""
Blueprint Node Service for Unreal MCP.

This service provides access to blueprint node operations like connecting nodes,
adding events, functions, variables, and other node types to blueprint graphs.
"""

import logging
from typing import Any, Dict, List, Optional

from core.connection import UnrealConnection
from core.types import Vector3

logger = logging.getLogger("UnrealMCP")


class BlueprintNodeService:
    """Service for blueprint node operations."""

    def __init__(self, connection: UnrealConnection):
        """Initialize the blueprint node service."""
        self.connection = connection

    def connect_blueprint_nodes(
        self,
        blueprint_name: str,
        source_node_id: str,
        target_node_id: str,
        source_pin: str,
        target_pin: str,
    ) -> Dict[str, Any]:
        """
        Connect two blueprint nodes via their pins.

        Args:
            blueprint_name: Name of the blueprint
            source_node_id: ID of the source node
            target_node_id: ID of the target node
            source_pin: Name of the source pin
            target_pin: Name of the target pin

        Returns:
            Dict containing the API response
        """
        try:
            logger.info(f"Connecting blueprint nodes: {source_node_id} -> {target_node_id}")
            params = {
                "blueprint_name": blueprint_name,
                "source_node_id": source_node_id,
                "target_node_id": target_node_id,
                "source_pin": source_pin,
                "target_pin": target_pin,
            }
            result = self.connection.send_command("connect_blueprint_nodes", params)
            return result
        except Exception as e:
            logger.error(f"Failed to connect blueprint nodes: {e}")
            raise

    def add_blueprint_event(
        self,
        blueprint_name: str,
        event_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """
        Add an event node to a blueprint graph.

        Args:
            blueprint_name: Name of the blueprint
            event_name: Name of the event to add
            node_position: Position for the node [x, y]

        Returns:
            Dict containing the API response with node ID
        """
        try:
            logger.info(f"Adding blueprint event node: {event_name}")
            params = {
                "blueprint_name": blueprint_name,
                "event_name": event_name,
                "node_position": {"x": node_position[0], "y": node_position[1]},
            }
            result = self.connection.send_command("add_blueprint_event", params)
            return result
        except Exception as e:
            logger.error(f"Failed to add blueprint event: {e}")
            raise

    def add_blueprint_function_call(
        self,
        blueprint_name: str,
        function_name: str,
        target: Optional[str] = None,
        node_position: Optional[List[float]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Add a function call node to a blueprint graph.

        Args:
            blueprint_name: Name of the blueprint
            function_name: Name of the function to call
            target: Optional target for the function call
            node_position: Optional position for the node [x, y]
            params: Optional parameters for the function

        Returns:
            Dict containing the API response with node ID
        """
        try:
            logger.info(f"Adding blueprint function call: {function_name}")
            command_params = {
                "blueprint_name": blueprint_name,
                "function_name": function_name,
            }

            if target:
                command_params["target"] = target
            if node_position:
                command_params["node_position"] = {"x": node_position[0], "y": node_position[1]}
            if params:
                command_params["params"] = params

            result = self.connection.send_command("add_blueprint_function_call", command_params)
            return result
        except Exception as e:
            logger.error(f"Failed to add blueprint function call: {e}")
            raise

    def add_blueprint_variable(
        self,
        blueprint_name: str,
        variable_name: str,
        variable_type: str,
        is_exposed: bool = False,
    ) -> Dict[str, Any]:
        """
        Add a variable to a blueprint.

        Args:
            blueprint_name: Name of the blueprint
            variable_name: Name of the variable
            variable_type: Type of the variable
            is_exposed: Whether the variable should be exposed

        Returns:
            Dict containing the API response with variable details
        """
        try:
            logger.info(f"Adding blueprint variable: {variable_name} ({variable_type})")
            params = {
                "blueprint_name": blueprint_name,
                "variable_name": variable_name,
                "variable_type": variable_type,
                "is_exposed": is_exposed,
            }
            result = self.connection.send_command("add_blueprint_variable", params)
            return result
        except Exception as e:
            logger.error(f"Failed to add blueprint variable: {e}")
            raise

    def find_blueprint_nodes(
        self,
        blueprint_name: str,
        node_type: Optional[str] = None,
        event_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Find nodes in a blueprint graph by type and criteria.

        Args:
            blueprint_name: Name of the blueprint
            node_type: Optional type of nodes to find
            event_name: Optional event name to filter by

        Returns:
            Dict containing the API response with array of node GUIDs
        """
        try:
            logger.info(f"Finding blueprint nodes: {node_type or 'all'}")
            params = {"blueprint_name": blueprint_name}

            if node_type:
                params["node_type"] = node_type
            if event_name:
                params["event_name"] = event_name

            result = self.connection.send_command("find_blueprint_nodes", params)
            return result
        except Exception as e:
            logger.error(f"Failed to find blueprint nodes: {e}")
            raise

    def add_blueprint_input_action_node(
        self,
        blueprint_name: str,
        action_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """
        Add a legacy input action node to a blueprint graph.

        Args:
            blueprint_name: Name of the blueprint
            action_name: Name of the input action
            node_position: Position for the node [x, y]

        Returns:
            Dict containing the API response with node ID
        """
        try:
            logger.info(f"Adding blueprint input action node: {action_name}")
            params = {
                "blueprint_name": blueprint_name,
                "action_name": action_name,
                "node_position": {"x": node_position[0], "y": node_position[1]},
            }
            result = self.connection.send_command("add_blueprint_input_action_node", params)
            return result
        except Exception as e:
            logger.error(f"Failed to add blueprint input action node: {e}")
            raise

    def add_blueprint_self_reference(
        self,
        blueprint_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """
        Add a self reference node to a blueprint graph.

        Args:
            blueprint_name: Name of the blueprint
            node_position: Position for the node [x, y]

        Returns:
            Dict containing the API response with node ID
        """
        try:
            logger.info("Adding blueprint self reference node")
            params = {
                "blueprint_name": blueprint_name,
                "node_position": {"x": node_position[0], "y": node_position[1]},
            }
            result = self.connection.send_command("add_blueprint_self_reference", params)
            return result
        except Exception as e:
            logger.error(f"Failed to add blueprint self reference: {e}")
            raise

    def add_blueprint_get_self_component_reference(
        self,
        blueprint_name: str,
        component_name: str,
        node_position: List[float],
    ) -> Dict[str, Any]:
        """
        Add a self component reference node to a blueprint graph.

        Args:
            blueprint_name: Name of the blueprint
            component_name: Name of the component
            node_position: Position for the node [x, y]

        Returns:
            Dict containing the API response with node ID
        """
        try:
            logger.info(f"Adding blueprint self component reference: {component_name}")
            params = {
                "blueprint_name": blueprint_name,
                "component_name": component_name,
                "node_position": {"x": node_position[0], "y": node_position[1]},
            }
            result = self.connection.send_command("add_blueprint_get_self_component_reference", params)
            return result
        except Exception as e:
            logger.error(f"Failed to add blueprint self component reference: {e}")
            raise