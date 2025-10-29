"""
Project service for high-level project operations.
"""

import logging
from typing import Any, Dict

from core.connection import UnrealConnection

logger = logging.getLogger("UnrealMCP")


class ProjectService:
    """Service for project-level operations."""

    def __init__(self, connection: UnrealConnection):
        self.connection = connection

    def create_legacy_input_mapping(
        self, action_name: str, key: str, input_type: str = "Action"
    ) -> Dict[str, Any]:
        """Create a legacy input mapping for the project (deprecated, use enhanced input system)."""
        params = {"action_name": action_name, "key": key, "input_type": input_type}
        return self.connection.send_command("create_legacy_input_mapping", params)
