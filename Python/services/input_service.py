"""
Input Service for Unreal MCP.

This service provides access to input-related operations like creating enhanced input actions,
input mapping contexts, and managing input mappings.
"""

import logging
from typing import Any, Dict, Optional

from core.connection import UnrealConnection

logger = logging.getLogger("UnrealMCP")


class InputService:
    """Service for input-related operations."""

    def __init__(self, connection: UnrealConnection):
        """Initialize the input service."""
        self.connection = connection

    def create_enhanced_input_action(
        self,
        name: str,
        value_type: str = "Axis1D",
        path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create an Enhanced Input Action asset.

        Args:
            name: Name of the input action
            value_type: Type of value (Axis1D, Axis2D, Axis3D, Digital, etc.)
            path: Optional path where to create the asset

        Returns:
            Dict containing the API response with input action details
        """
        try:
            logger.info(f"Creating enhanced input action: {name} ({value_type})")
            params = {
                "name": name,
                "value_type": value_type,
            }

            if path:
                params["path"] = path

            result = self.connection.send_command("create_enhanced_input_action", params)
            return result
        except Exception as e:
            logger.error(f"Failed to create enhanced input action: {e}")
            raise

    def create_input_mapping_context(
        self,
        name: str,
        path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create an Input Mapping Context asset.

        Args:
            name: Name of the mapping context
            path: Optional path where to create the asset

        Returns:
            Dict containing the API response with mapping context details
        """
        try:
            logger.info(f"Creating input mapping context: {name}")
            params = {"name": name}

            if path:
                params["path"] = path

            result = self.connection.send_command("create_input_mapping_context", params)
            return result
        except Exception as e:
            logger.error(f"Failed to create input mapping context: {e}")
            raise

    def add_enhanced_input_mapping(
        self,
        context_path: str,
        action_path: str,
        key: str,
    ) -> Dict[str, Any]:
        """
        Add a key mapping to an Input Mapping Context.

        Args:
            context_path: Path to the mapping context asset
            action_path: Path to the input action asset
            key: Key to bind (e.g., "SpaceBar", "LeftMouseButton", etc.)

        Returns:
            Dict containing the API response confirming the mapping was added
        """
        try:
            logger.info(f"Adding enhanced input mapping: {key} -> {action_path} in {context_path}")
            params = {
                "context_path": context_path,
                "action_path": action_path,
                "key": key,
            }
            result = self.connection.send_command("add_enhanced_input_mapping", params)
            return result
        except Exception as e:
            logger.error(f"Failed to add enhanced input mapping: {e}")
            raise

    def remove_enhanced_input_mapping(
        self,
        context_path: str,
        action_path: str,
        key: str,
    ) -> Dict[str, Any]:
        """
        Remove a key mapping from an Input Mapping Context.

        Args:
            context_path: Path to the mapping context asset
            action_path: Path to the input action asset
            key: Key to unbind

        Returns:
            Dict containing the API response confirming the mapping was removed
        """
        try:
            logger.info(f"Removing enhanced input mapping: {key} -> {action_path} from {context_path}")
            params = {
                "context_path": context_path,
                "action_path": action_path,
                "key": key,
            }
            result = self.connection.send_command("remove_enhanced_input_mapping", params)
            return result
        except Exception as e:
            logger.error(f"Failed to remove enhanced input mapping: {e}")
            raise

    def apply_mapping_context(
        self,
        context_path: str,
        priority: int = 0,
    ) -> Dict[str, Any]:
        """
        Apply an Input Mapping Context.

        Args:
            context_path: Path to the mapping context asset
            priority: Priority of the mapping context

        Returns:
            Dict containing the API response confirming the context was applied
        """
        try:
            logger.info(f"Applying mapping context: {context_path} (priority: {priority})")
            params = {
                "context_path": context_path,
                "priority": priority,
            }
            result = self.connection.send_command("apply_mapping_context", params)
            return result
        except Exception as e:
            logger.error(f"Failed to apply mapping context: {e}")
            raise

    def remove_mapping_context(
        self,
        context_path: str,
    ) -> Dict[str, Any]:
        """
        Remove an applied Input Mapping Context.

        Args:
            context_path: Path to the mapping context asset

        Returns:
            Dict containing the API response confirming the context was removed
        """
        try:
            logger.info(f"Removing mapping context: {context_path}")
            params = {"context_path": context_path}
            result = self.connection.send_command("remove_mapping_context", params)
            return result
        except Exception as e:
            logger.error(f"Failed to remove mapping context: {e}")
            raise

    def clear_all_mapping_contexts(self) -> Dict[str, Any]:
        """
        Clear all applied mapping contexts.

        Returns:
            Dict containing the API response confirming all contexts were cleared
        """
        try:
            logger.info("Clearing all mapping contexts")
            result = self.connection.send_command("clear_all_mapping_contexts", {})
            return result
        except Exception as e:
            logger.error(f"Failed to clear all mapping contexts: {e}")
            raise