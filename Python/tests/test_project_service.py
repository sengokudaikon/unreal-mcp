"""
Tests for ProjectService.
"""

from unittest.mock import Mock

import pytest

from core.connection import UnrealConnection
from core.types import Result
from services.project_service import ProjectService


class TestProjectService:
    """Test ProjectService class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_connection = Mock(spec=UnrealConnection)
        self.service = ProjectService(self.mock_connection)

    def test_initialization(self):
        """Test service initialization."""
        assert self.service.connection == self.mock_connection

    # create_input_mapping tests
    def test_create_input_mapping_default_type(self):
        """Test creating input mapping with default input type."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "action_name": "Jump"}
        )

        result = self.service.create_input_mapping("Jump", "SpaceBar")

        self.mock_connection.send_command.assert_called_once_with(
            "create_input_mapping",
            {"action_name": "Jump", "key": "SpaceBar", "input_type": "Action"},
        )
        assert result.is_success
        assert result.get_value()["action_name"] == "Jump"

    def test_create_input_mapping_action_type(self):
        """Test creating input mapping with Action type."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.create_input_mapping("Jump", "SpaceBar", "Action")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["input_type"] == "Action"

    def test_create_input_mapping_axis_type(self):
        """Test creating input mapping with Axis type."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.create_input_mapping("MoveForward", "W", "Axis")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["input_type"] == "Axis"
        assert params["action_name"] == "MoveForward"
        assert params["key"] == "W"

    def test_create_input_mapping_multiple_keys(self):
        """Test creating multiple input mappings with different keys."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        # Test first mapping
        result1 = self.service.create_input_mapping("Jump", "SpaceBar")
        assert result1.is_success

        # Reset mock
        self.mock_connection.reset_mock()
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        # Test second mapping
        result2 = self.service.create_input_mapping("Jump", "Gamepad_FaceButton_Bottom")
        assert result2.is_success

        # Verify both calls were made
        assert self.mock_connection.send_command.call_count == 1

    def test_create_input_mapping_failure_duplicate(self):
        """Test creating input mapping with duplicate action."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Action already exists"
        )

        result = self.service.create_input_mapping("Jump", "SpaceBar")

        assert result.is_failure
        assert result.get_error() == "Action already exists"

    def test_create_input_mapping_failure_invalid_key(self):
        """Test creating input mapping with invalid key."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Invalid key name"
        )

        result = self.service.create_input_mapping("Jump", "InvalidKey123")

        assert result.is_failure
        assert result.get_error() == "Invalid key name"

    def test_create_input_mapping_failure_invalid_type(self):
        """Test creating input mapping with invalid input type."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Invalid input type"
        )

        result = self.service.create_input_mapping("Jump", "SpaceBar", "Invalid")

        assert result.is_failure
        assert result.get_error() == "Invalid input type"

    def test_create_input_mapping_common_keys(self):
        """Test creating input mappings with common key names."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        keys = [
            "W",
            "A",
            "S",
            "D",
            "SpaceBar",
            "LeftShift",
            "LeftCtrl",
            "Tab",
        ]

        for key in keys:
            result = self.service.create_input_mapping("TestAction", key)
            assert result.is_success

    def test_create_input_mapping_gamepad_keys(self):
        """Test creating input mappings with gamepad keys."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        gamepad_keys = [
            "Gamepad_FaceButton_Bottom",
            "Gamepad_FaceButton_Right",
            "Gamepad_FaceButton_Left",
            "Gamepad_FaceButton_Top",
            "Gamepad_LeftTrigger",
            "Gamepad_RightTrigger",
        ]

        for key in gamepad_keys:
            result = self.service.create_input_mapping("GamepadAction", key)
            assert result.is_success

    def test_create_input_mapping_empty_action_name(self):
        """Test creating input mapping with empty action name."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Action name cannot be empty"
        )

        result = self.service.create_input_mapping("", "SpaceBar")

        assert result.is_failure

    def test_create_input_mapping_empty_key(self):
        """Test creating input mapping with empty key."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Key cannot be empty"
        )

        result = self.service.create_input_mapping("Jump", "")

        assert result.is_failure

    def test_create_input_mapping_special_characters_in_action(self):
        """Test creating input mapping with special characters in action name."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.create_input_mapping("Jump_Action_01", "SpaceBar")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["action_name"] == "Jump_Action_01"
        assert result.is_success

    def test_create_input_mapping_case_sensitivity(self):
        """Test creating input mapping with different case variations."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        # Test uppercase
        result1 = self.service.create_input_mapping("JUMP", "SpaceBar")
        assert result1.is_success

        # Reset and test lowercase
        self.mock_connection.reset_mock()
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result2 = self.service.create_input_mapping("jump", "SpaceBar")
        assert result2.is_success

    def test_create_input_mapping_connection_error(self):
        """Test creating input mapping with connection error."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Connection refused"
        )

        result = self.service.create_input_mapping("Jump", "SpaceBar")

        assert result.is_failure
        assert result.get_error() == "Connection refused"

    def test_create_input_mapping_timeout_error(self):
        """Test creating input mapping with timeout."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Request timeout"
        )

        result = self.service.create_input_mapping("Jump", "SpaceBar")

        assert result.is_failure
        assert result.get_error() == "Request timeout"

    def test_create_input_mapping_response_structure(self):
        """Test that response contains expected structure."""
        response_data = {
            "success": True,
            "action_name": "Jump",
            "key": "SpaceBar",
            "input_type": "Action",
        }
        self.mock_connection.send_command.return_value = Result.success(response_data)

        result = self.service.create_input_mapping("Jump", "SpaceBar")

        assert result.is_success
        response = result.get_value()
        assert response["success"] is True
        assert response["action_name"] == "Jump"
        assert response["key"] == "SpaceBar"
        assert response["input_type"] == "Action"

    def test_create_input_mapping_with_all_parameter_variations(self):
        """Test create_input_mapping with different parameter combinations."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        # Test combination 1: Default type
        result1 = self.service.create_input_mapping("Action1", "Key1")
        assert result1.is_success

        # Reset mock
        self.mock_connection.reset_mock()
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        # Test combination 2: Custom type
        result2 = self.service.create_input_mapping("Action2", "Key2", "Axis")
        assert result2.is_success

    def test_create_input_mapping_long_action_name(self):
        """Test creating input mapping with long action name."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        long_name = "VeryLongActionNameForTestingPurposes123"
        result = self.service.create_input_mapping(long_name, "SpaceBar")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["action_name"] == long_name
        assert result.is_success
