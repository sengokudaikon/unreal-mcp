"""
Registry Service for Unreal MCP.

This service provides access to registry information like available API methods,
supported parent classes, and component types.
"""

import logging
from typing import Any, Dict

from core.connection import UnrealConnection

logger = logging.getLogger("UnrealMCP")


class RegistryService:
    """Service for registry-related operations."""

    def __init__(self, connection: UnrealConnection):
        """Initialize the registry service."""
        self.connection = connection

    def get_available_api_methods(self) -> Dict[str, Any]:
        """
        Get all available API methods organized by category.

        Returns:
            Dict containing the API response with available methods
        """
        try:
            logger.info("Getting available API methods")
            result = self.connection.send_command("get_available_api_methods", {})
            return result
        except Exception as e:
            logger.error(f"Failed to get available API methods: {e}")
            raise

    def get_supported_parent_classes(self) -> Dict[str, Any]:
        """
        Get all supported parent classes for Blueprint creation.

        Returns:
            Dict containing the API response with supported parent classes
        """
        try:
            logger.info("Getting supported parent classes")
            result = self.connection.send_command("get_supported_parent_classes", {})
            return result
        except Exception as e:
            logger.error(f"Failed to get supported parent classes: {e}")
            raise

    def get_supported_component_types(self) -> Dict[str, Any]:
        """
        Get all supported component types.

        Returns:
            Dict containing the API response with supported component types
        """
        try:
            logger.info("Getting supported component types")
            result = self.connection.send_command("get_supported_component_types", {})
            return result
        except Exception as e:
            logger.error(f"Failed to get supported component types: {e}")
            raise