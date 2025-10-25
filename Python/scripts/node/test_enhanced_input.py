#!/usr/bin/env python
"""
Test script for Enhanced Input system via MCP.
This script creates Enhanced Input Actions, Mapping Contexts, and configures key bindings.

Enhanced Input is the modern input system for Unreal Engine 5.1+ and is recommended
over the legacy input system. It provides context-aware controls, modifiers, triggers,
and runtime remapping capabilities.
"""

import json
import logging
import os
import socket
import sys
import time
from typing import Any, Dict, List, Optional

# Add the parent directory to the path so we can import the server module
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("TestEnhancedInput")


def send_command(
    sock: socket.socket, command: str, params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Send a command to the Unreal MCP server and get the response."""
    try:
        # Create command object
        command_obj = {"type": command, "params": params}

        # Convert to JSON and send
        command_json = json.dumps(command_obj)
        logger.info(f"Sending command: {command_json}")
        sock.sendall(command_json.encode("utf-8"))

        # Receive response
        chunks = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

            # Try parsing to see if we have a complete response
            try:
                data = b"".join(chunks)
                json.loads(data.decode("utf-8"))
                # If we can parse it, we have the complete response
                break
            except json.JSONDecodeError:
                # Not a complete JSON object yet, continue receiving
                continue

        # Parse response
        data = b"".join(chunks)
        response = json.loads(data.decode("utf-8"))
        logger.info(f"Received response: {response}")
        return response

    except Exception as e:
        logger.error(f"Error sending command: {e}")
        return None


def check_success(response: Optional[Dict[str, Any]], operation: str) -> bool:
    """Check if a command response indicates success."""
    if not response:
        logger.error(f"{operation}: No response from server")
        return False

    # Check for error in response
    if "error" in response:
        logger.error(f"{operation}: Error - {response.get('error')}")
        return False

    # Check status field
    status = response.get("status")
    if status == "error":
        logger.error(
            f"{operation}: Status error - {response.get('message', 'Unknown error')}"
        )
        return False

    # For commands that return results
    result = response.get("result", {})
    if isinstance(result, dict):
        if "message" in result and "error" in result["message"].lower():
            logger.error(f"{operation}: {result['message']}")
            return False

        # Check if success field exists and is False
        if "success" in result and not result["success"]:
            logger.error(
                f"{operation}: Operation returned success=False - {result.get('message', '')}"
            )
            return False

    logger.info(f"{operation}: SUCCESS")
    return True


def main():
    """Main function to test Enhanced Input system."""
    try:
        logger.info("=" * 80)
        logger.info("Enhanced Input System Test")
        logger.info("=" * 80)

        # =========================================
        # Step 1: Create Enhanced Input Actions
        # =========================================
        logger.info("\n--- Step 1: Creating Enhanced Input Actions ---")

        # Create a Boolean action for Jump
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        jump_action_params = {
            "name": "Jump",
            "value_type": "Boolean",
            "path": "/Game/Input/Actions",
        }

        response = send_command(
            sock, "create_enhanced_input_action", jump_action_params
        )
        if not check_success(response, "Create Jump Action"):
            logger.error("Failed to create Jump action, aborting test")
            return

        jump_action_path = response.get("result", {}).get(
            "asset_path", "/Game/Input/Actions/IA_Jump"
        )
        logger.info(f"Jump action created at: {jump_action_path}")

        sock.close()
        time.sleep(0.5)

        # Create an Axis2D action for Movement
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        move_action_params = {
            "name": "Move",
            "value_type": "Axis2D",
            "path": "/Game/Input/Actions",
        }

        response = send_command(
            sock, "create_enhanced_input_action", move_action_params
        )
        if not check_success(response, "Create Move Action"):
            logger.error("Failed to create Move action, aborting test")
            return

        move_action_path = response.get("result", {}).get(
            "asset_path", "/Game/Input/Actions/IA_Move"
        )
        logger.info(f"Move action created at: {move_action_path}")

        sock.close()
        time.sleep(0.5)

        # Create an Axis1D action for Look (mouse X movement)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        look_action_params = {
            "name": "Look",
            "value_type": "Axis2D",
            "path": "/Game/Input/Actions",
        }

        response = send_command(
            sock, "create_enhanced_input_action", look_action_params
        )
        if not check_success(response, "Create Look Action"):
            logger.error("Failed to create Look action, aborting test")
            return

        look_action_path = response.get("result", {}).get(
            "asset_path", "/Game/Input/Actions/IA_Look"
        )
        logger.info(f"Look action created at: {look_action_path}")

        sock.close()
        time.sleep(0.5)

        # =========================================
        # Step 2: Create Input Mapping Context
        # =========================================
        logger.info("\n--- Step 2: Creating Input Mapping Context ---")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        context_params = {"name": "DefaultPlayer", "path": "/Game/Input/Contexts"}

        response = send_command(sock, "create_input_mapping_context", context_params)
        if not check_success(response, "Create Mapping Context"):
            logger.error("Failed to create mapping context, aborting test")
            return

        context_path = response.get("result", {}).get(
            "asset_path", "/Game/Input/Contexts/IMC_DefaultPlayer"
        )
        logger.info(f"Mapping context created at: {context_path}")

        sock.close()
        time.sleep(0.5)

        # =========================================
        # Step 3: Add Key Mappings to Context
        # =========================================
        logger.info("\n--- Step 3: Adding Key Mappings ---")

        # Define key mappings
        key_mappings = [
            ("Jump", jump_action_path, "SpaceBar", "Jump with spacebar"),
            ("Move Forward", move_action_path, "W", "Move forward with W"),
            ("Move Back", move_action_path, "S", "Move backward with S"),
            ("Move Left", move_action_path, "A", "Move left with A"),
            ("Move Right", move_action_path, "D", "Move right with D"),
            ("Look X", look_action_path, "MouseX", "Mouse X for looking"),
            ("Look Y", look_action_path, "MouseY", "Mouse Y for looking"),
        ]

        for name, action_path, key, description in key_mappings:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 55557))

            mapping_params = {
                "context_path": context_path,
                "action_path": action_path,
                "key": key,
            }

            response = send_command(sock, "add_enhanced_input_mapping", mapping_params)
            if not check_success(response, f"Add Mapping: {description}"):
                logger.warning(f"Failed to add mapping for {name}, continuing...")

            sock.close()
            time.sleep(0.5)

        # =========================================
        # Step 4: Apply Mapping Context (Runtime)
        # =========================================
        logger.info("\n--- Step 4: Applying Mapping Context at Runtime ---")

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        apply_params = {"context_path": context_path, "priority": 0}

        response = send_command(sock, "apply_mapping_context", apply_params)
        if not check_success(response, "Apply Mapping Context"):
            logger.warning("Failed to apply mapping context at runtime")
            logger.info("Note: This may fail if no player controller is active in PIE")
        else:
            logger.info("Mapping context applied successfully!")

        sock.close()
        time.sleep(0.5)

        # =========================================
        # Step 5: Test Runtime Context Management
        # =========================================
        logger.info("\n--- Step 5: Testing Runtime Context Management ---")

        # Remove the context
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        remove_params = {"context_path": context_path}

        response = send_command(sock, "remove_mapping_context", remove_params)
        if check_success(response, "Remove Mapping Context"):
            logger.info("Mapping context removed successfully!")

        sock.close()
        time.sleep(0.5)

        # Re-apply it
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 55557))

        response = send_command(sock, "apply_mapping_context", apply_params)
        if check_success(response, "Re-apply Mapping Context"):
            logger.info("Mapping context re-applied successfully!")

        sock.close()
        time.sleep(0.5)

        # =========================================
        # Test Complete
        # =========================================
        logger.info("\n" + "=" * 80)
        logger.info("Enhanced Input Test Complete!")
        logger.info("=" * 80)
        logger.info("\nCreated Assets:")
        logger.info(f"  - Input Action (Jump): {jump_action_path}")
        logger.info(f"  - Input Action (Move): {move_action_path}")
        logger.info(f"  - Input Action (Look): {look_action_path}")
        logger.info(f"  - Mapping Context: {context_path}")
        logger.info("\nKey Bindings:")
        for name, _, key, description in key_mappings:
            logger.info(f"  - {key}: {description}")
        logger.info("\nNext Steps:")
        logger.info("  1. Open Unreal Engine Editor")
        logger.info("  2. Navigate to Content/Input folder")
        logger.info("  3. Verify the created Input Actions and Mapping Context assets")
        logger.info("  4. You can now reference these assets in your Blueprints!")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"Error during test: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
