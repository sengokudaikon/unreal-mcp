"""
Enhanced Input Tools for Unreal MCP.

This module provides tools for managing Enhanced Input actions and mapping contexts.
Enhanced Input is the modern input system for Unreal Engine 5.1+, replacing the legacy input system.
"""

import logging
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP, Context

# Get logger
logger = logging.getLogger("UnrealMCP")

def register_enhanced_input_tools(mcp: FastMCP):
    """Register Enhanced Input tools with the MCP server."""

    @mcp.tool()
    def create_enhanced_input_action(
        ctx: Context,
        name: str,
        value_type: str = "Boolean",
        path: str = "/Game/Input"
    ) -> Dict[str, Any]:
        """
        Create an Enhanced Input Action asset.

        Enhanced Input Actions represent logical player actions (Jump, Move, Attack, etc.)
        and are data assets that can be referenced by blueprints and C++ code.

        Args:
            name: Name of the input action (e.g., "Jump", "Move", "Attack")
            value_type: Type of value the action produces:
                - "Boolean": Simple pressed/released actions (Jump, Crouch)
                - "Axis1D": Single axis analog input (Throttle, Zoom)
                - "Axis2D": Two axis input (Movement, Mouse Delta)
                - "Axis3D": Three axis input (rarely used)
            path: Content browser path where the asset will be created (default: /Game/Input)

        Returns:
            Response with asset details or error message

        Example:
            # Create a jump action
            create_enhanced_input_action("Jump", "Boolean", "/Game/Input/Actions")

            # Create a movement action
            create_enhanced_input_action("Move", "Axis2D", "/Game/Input/Actions")
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            params = {
                "name": name,
                "value_type": value_type,
                "path": path
            }

            logger.info(f"Creating Enhanced Input Action '{name}' with value type '{value_type}'")
            response = unreal.send_command("create_enhanced_input_action", params)

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Enhanced Input Action creation response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error creating Enhanced Input Action: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def create_input_mapping_context(
        ctx: Context,
        name: str,
        path: str = "/Game/Input"
    ) -> Dict[str, Any]:
        """
        Create an Input Mapping Context asset.

        Input Mapping Contexts are collections of key-to-action mappings that can be
        activated or deactivated at runtime. This allows for context-sensitive controls
        (e.g., different mappings for on-foot vs. in-vehicle gameplay).

        Args:
            name: Name of the mapping context (e.g., "OnFoot", "InVehicle", "Menu")
            path: Content browser path where the asset will be created (default: /Game/Input)

        Returns:
            Response with asset details or error message

        Example:
            # Create a mapping context for on-foot gameplay
            create_input_mapping_context("OnFoot", "/Game/Input/Contexts")

            # Create a mapping context for vehicle controls
            create_input_mapping_context("InVehicle", "/Game/Input/Contexts")
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            params = {
                "name": name,
                "path": path
            }

            logger.info(f"Creating Input Mapping Context '{name}'")
            response = unreal.send_command("create_input_mapping_context", params)

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Input Mapping Context creation response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error creating Input Mapping Context: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def add_enhanced_input_mapping(
        ctx: Context,
        context_path: str,
        action_path: str,
        key: str
    ) -> Dict[str, Any]:
        """
        Add a key mapping to an Input Mapping Context.

        This binds a physical key (keyboard, mouse, gamepad) to an Input Action
        within a specific Mapping Context.

        Args:
            context_path: Full asset path to the Input Mapping Context
                         (e.g., "/Game/Input/IMC_OnFoot")
            action_path: Full asset path to the Input Action
                        (e.g., "/Game/Input/IA_Jump")
            key: Key to bind (e.g., "SpaceBar", "W", "Gamepad_FaceButton_Bottom")
                Common keys:
                - Keyboard: "W", "A", "S", "D", "SpaceBar", "LeftShift", etc.
                - Mouse: "LeftMouseButton", "RightMouseButton", "MouseX", "MouseY"
                - Gamepad: "Gamepad_LeftStick_Up", "Gamepad_FaceButton_Bottom"

        Returns:
            Response with mapping details or error message

        Example:
            # Bind spacebar to Jump action in OnFoot context
            add_enhanced_input_mapping(
                "/Game/Input/IMC_OnFoot",
                "/Game/Input/IA_Jump",
                "SpaceBar"
            )

            # Bind W key to Move action
            add_enhanced_input_mapping(
                "/Game/Input/IMC_OnFoot",
                "/Game/Input/IA_Move",
                "W"
            )
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            params = {
                "context_path": context_path,
                "action_path": action_path,
                "key": key
            }

            logger.info(f"Adding Enhanced Input mapping: {key} -> {action_path} in {context_path}")
            response = unreal.send_command("add_enhanced_input_mapping", params)

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Enhanced Input mapping addition response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error adding Enhanced Input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def remove_enhanced_input_mapping(
        ctx: Context,
        context_path: str,
        action_path: str
    ) -> Dict[str, Any]:
        """
        Remove all key mappings for an Input Action from a Mapping Context.

        Args:
            context_path: Full asset path to the Input Mapping Context
            action_path: Full asset path to the Input Action

        Returns:
            Response indicating success or failure

        Example:
            remove_enhanced_input_mapping(
                "/Game/Input/IMC_OnFoot",
                "/Game/Input/IA_Jump"
            )
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            params = {
                "context_path": context_path,
                "action_path": action_path
            }

            logger.info(f"Removing Enhanced Input mapping: {action_path} from {context_path}")
            response = unreal.send_command("remove_enhanced_input_mapping", params)

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Enhanced Input mapping removal response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error removing Enhanced Input mapping: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def apply_mapping_context(
        ctx: Context,
        context_path: str,
        priority: int = 0
    ) -> Dict[str, Any]:
        """
        Apply an Input Mapping Context to the player's input subsystem at runtime.

        This activates the key bindings defined in the Mapping Context. Multiple contexts
        can be active simultaneously, with priority determining which mapping takes
        precedence when conflicts occur.

        Args:
            context_path: Full asset path to the Input Mapping Context
            priority: Priority level (higher = takes precedence). Default: 0

        Returns:
            Response indicating success or failure

        Example:
            # Apply on-foot controls
            apply_mapping_context("/Game/Input/IMC_OnFoot", priority=0)

            # Apply UI controls (higher priority overrides gameplay)
            apply_mapping_context("/Game/Input/IMC_UI", priority=10)
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            params = {
                "context_path": context_path,
                "priority": priority
            }

            logger.info(f"Applying Input Mapping Context: {context_path} with priority {priority}")
            response = unreal.send_command("apply_mapping_context", params)

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Mapping context application response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error applying mapping context: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def remove_mapping_context(
        ctx: Context,
        context_path: str
    ) -> Dict[str, Any]:
        """
        Remove an Input Mapping Context from the player's input subsystem.

        This deactivates all key bindings defined in the Mapping Context.

        Args:
            context_path: Full asset path to the Input Mapping Context

        Returns:
            Response indicating success or failure

        Example:
            # Remove on-foot controls when entering a vehicle
            remove_mapping_context("/Game/Input/IMC_OnFoot")
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            params = {
                "context_path": context_path
            }

            logger.info(f"Removing Input Mapping Context: {context_path}")
            response = unreal.send_command("remove_mapping_context", params)

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Mapping context removal response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error removing mapping context: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    @mcp.tool()
    def clear_all_mapping_contexts(ctx: Context) -> Dict[str, Any]:
        """
        Clear all Input Mapping Contexts from the player's input subsystem.

        This deactivates all Enhanced Input bindings. Useful for resetting input state
        or when transitioning to a completely different input mode.

        Returns:
            Response indicating success or failure

        Example:
            # Clear all input mappings
            clear_all_mapping_contexts()
        """
        from unreal_mcp_server import get_unreal_connection

        try:
            unreal = get_unreal_connection()
            if not unreal:
                logger.error("Failed to connect to Unreal Engine")
                return {"success": False, "message": "Failed to connect to Unreal Engine"}

            logger.info("Clearing all Input Mapping Contexts")
            response = unreal.send_command("clear_all_mapping_contexts", {})

            if not response:
                logger.error("No response from Unreal Engine")
                return {"success": False, "message": "No response from Unreal Engine"}

            logger.info(f"Clear all mapping contexts response: {response}")
            return response

        except Exception as e:
            error_msg = f"Error clearing mapping contexts: {e}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}

    logger.info("Enhanced Input tools registered successfully")
