"""
Tests for EditorService.
"""

from unittest.mock import Mock

import pytest

from core.connection import UnrealConnection
from core.types import Result, Transform, Vector3
from services.editor_service import EditorService


class TestEditorService:
    """Test EditorService class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_connection = Mock(spec=UnrealConnection)
        self.service = EditorService(self.mock_connection)

    def test_initialization(self):
        """Test service initialization."""
        assert self.service.connection == self.mock_connection

    # get_actors_in_level tests
    def test_get_actors_in_level_success(self):
        """Test getting actors in level successfully."""
        mock_actors = [
            {"name": "Actor1", "type": "Pawn"},
            {"name": "Actor2", "type": "Character"},
        ]
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "actors": mock_actors}
        )

        result = self.service.get_actors_in_level()

        self.mock_connection.send_command.assert_called_once_with(
            "get_actors_in_level", {}
        )
        assert result.is_success
        assert result.get_value() == mock_actors

    def test_get_actors_in_level_empty(self):
        """Test getting actors when level is empty."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "actors": []}
        )

        result = self.service.get_actors_in_level()

        assert result.is_success
        assert result.get_value() == []

    def test_get_actors_in_level_failure(self):
        """Test getting actors with failure response."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Connection error"
        )

        result = self.service.get_actors_in_level()

        assert result.is_failure
        assert result.get_error() == "Connection error"

    def test_get_actors_in_level_no_success_flag(self):
        """Test getting actors when success flag is missing."""
        self.mock_connection.send_command.return_value = Result.success(
            {"actors": [{"name": "Actor1"}]}
        )

        result = self.service.get_actors_in_level()

        assert result.is_success
        assert result.get_value() == [{"name": "Actor1"}]

    def test_get_actors_in_level_false_success(self):
        """Test getting actors when success flag is False."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": False, "actors": []}
        )

        result = self.service.get_actors_in_level()

        assert result.is_failure
        assert result.get_error() == "Failed to get actors"

    # find_actors_by_name tests
    def test_find_actors_by_name_success(self):
        """Test finding actors by name successfully."""
        mock_actors = [{"name": "BP_Character_1", "type": "Character"}]
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "actors": mock_actors}
        )

        result = self.service.find_actors_by_name("BP_Character*")

        self.mock_connection.send_command.assert_called_once_with(
            "find_actors_by_name", {"pattern": "BP_Character*"}
        )
        assert result.is_success
        assert result.get_value() == mock_actors

    def test_find_actors_by_name_no_matches(self):
        """Test finding actors when pattern matches nothing."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "actors": []}
        )

        result = self.service.find_actors_by_name("NonExistent*")

        assert result.is_success
        assert result.get_value() == []

    def test_find_actors_by_name_failure(self):
        """Test finding actors with failure."""
        self.mock_connection.send_command.return_value = Result.failure("Pattern error")

        result = self.service.find_actors_by_name("Invalid*Pattern")

        assert result.is_failure
        assert result.get_error() == "Pattern error"

    def test_find_actors_by_name_false_success(self):
        """Test finding actors when success flag is False."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": False, "actors": []}
        )

        result = self.service.find_actors_by_name("Test*")

        assert result.is_failure
        assert result.get_error() == "Failed to find actors"

    # spawn_actor tests
    def test_spawn_actor_with_defaults(self):
        """Test spawning actor with default transform."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "actor_name": "TestActor"}
        )

        result = self.service.spawn_actor("TestActor", "Pawn")

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "spawn_actor"
        params = call_args[0][1]
        assert params["name"] == "TestActor"
        assert params["type"] == "Pawn"
        assert params["location"] == [0.0, 0.0, 0.0]
        assert params["rotation"] == [0.0, 0.0, 0.0]
        assert params["scale"] == [1.0, 1.0, 1.0]

    def test_spawn_actor_with_custom_transform(self):
        """Test spawning actor with custom transform."""
        transform = Transform(
            location=Vector3(100, 200, 300),
            rotation=Vector3(0, 90, 0),
            scale=Vector3(2, 2, 2),
        )
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "actor_name": "TestActor"}
        )

        result = self.service.spawn_actor("TestActor", "Character", transform)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["location"] == [100.0, 200.0, 300.0]
        assert params["rotation"] == [0.0, 90.0, 0.0]
        assert params["scale"] == [2.0, 2.0, 2.0]

    def test_spawn_actor_failure(self):
        """Test spawning actor with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Actor type not found"
        )

        result = self.service.spawn_actor("TestActor", "InvalidType")

        assert result.is_failure
        assert result.get_error() == "Actor type not found"

    # delete_actor tests
    def test_delete_actor_success(self):
        """Test deleting actor successfully."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "deleted": True}
        )

        result = self.service.delete_actor("TestActor")

        self.mock_connection.send_command.assert_called_once_with(
            "delete_actor", {"name": "TestActor"}
        )
        assert result.is_success
        assert result.get_value()["deleted"] is True

    def test_delete_actor_not_found(self):
        """Test deleting actor that doesn't exist."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Actor not found"
        )

        result = self.service.delete_actor("NonExistent")

        assert result.is_failure
        assert result.get_error() == "Actor not found"

    # set_actor_transform tests
    def test_set_actor_transform_success(self):
        """Test setting actor transform successfully."""
        transform = Transform(
            location=Vector3(50, 100, 150),
            rotation=Vector3(45, 0, 0),
            scale=Vector3(1.5, 1.5, 1.5),
        )
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.set_actor_transform("TestActor", transform)

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "set_actor_transform"
        params = call_args[0][1]
        assert params["name"] == "TestActor"
        assert params["location"] == [50.0, 100.0, 150.0]
        assert params["rotation"] == [45.0, 0.0, 0.0]
        assert params["scale"] == [1.5, 1.5, 1.5]

    def test_set_actor_transform_failure(self):
        """Test setting actor transform with failure."""
        transform = Transform(
            location=Vector3(0, 0, 0),
            rotation=Vector3(0, 0, 0),
            scale=Vector3(1, 1, 1),
        )
        self.mock_connection.send_command.return_value = Result.failure(
            "Actor not found"
        )

        result = self.service.set_actor_transform("NonExistent", transform)

        assert result.is_failure
        assert result.get_error() == "Actor not found"

    # get_actor_properties tests
    def test_get_actor_properties_success(self):
        """Test getting actor properties successfully."""
        properties = {"health": 100, "armor": 50}
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "properties": properties}
        )

        result = self.service.get_actor_properties("TestActor")

        self.mock_connection.send_command.assert_called_once_with(
            "get_actor_properties", {"name": "TestActor"}
        )
        assert result.is_success
        assert result.get_value()["properties"] == properties

    def test_get_actor_properties_not_found(self):
        """Test getting properties of non-existent actor."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Actor not found"
        )

        result = self.service.get_actor_properties("NonExistent")

        assert result.is_failure
        assert result.get_error() == "Actor not found"

    # focus_viewport tests
    def test_focus_viewport_with_target(self):
        """Test focusing viewport on target actor."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.focus_viewport(target="TestActor")

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "focus_viewport"
        params = call_args[0][1]
        assert params["target"] == "TestActor"
        assert "location" not in params

    def test_focus_viewport_with_location(self):
        """Test focusing viewport on location."""
        location = Vector3(100, 200, 300)
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.focus_viewport(location=location)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["location"] == [100.0, 200.0, 300.0]
        assert "target" not in params

    def test_focus_viewport_with_distance(self):
        """Test focusing viewport with distance parameter."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.focus_viewport(target="TestActor", distance=500.0)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["target"] == "TestActor"
        assert params["distance"] == 500.0

    def test_focus_viewport_with_orientation(self):
        """Test focusing viewport with orientation parameter."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.focus_viewport(target="TestActor", orientation="Front")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["target"] == "TestActor"
        assert params["orientation"] == "Front"

    def test_focus_viewport_all_parameters(self):
        """Test focusing viewport with all parameters."""
        location = Vector3(100, 200, 300)
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.focus_viewport(
            target="TestActor",
            location=location,
            distance=750.0,
            orientation="Top",
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["target"] == "TestActor"
        assert params["location"] == [100.0, 200.0, 300.0]
        assert params["distance"] == 750.0
        assert params["orientation"] == "Top"

    def test_focus_viewport_no_parameters(self):
        """Test focusing viewport with no parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.focus_viewport()

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params == {}

    def test_focus_viewport_failure(self):
        """Test focusing viewport with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Invalid target"
        )

        result = self.service.focus_viewport(target="NonExistent")

        assert result.is_failure
        assert result.get_error() == "Invalid target"

    # take_screenshot tests
    def test_take_screenshot_with_defaults(self):
        """Test taking screenshot with default parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "path": "/screenshots/capture.png"}
        )

        result = self.service.take_screenshot()

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "take_screenshot"
        params = call_args[0][1]
        assert params["show_ui"] is True
        assert "filename" not in params
        assert "resolution" not in params

    def test_take_screenshot_with_filename(self):
        """Test taking screenshot with custom filename."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "path": "/screenshots/custom.png"}
        )

        result = self.service.take_screenshot(filename="custom.png")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["filename"] == "custom.png"
        assert params["show_ui"] is True

    def test_take_screenshot_without_ui(self):
        """Test taking screenshot without UI."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "path": "/screenshots/no_ui.png"}
        )

        result = self.service.take_screenshot(show_ui=False)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["show_ui"] is False

    def test_take_screenshot_with_resolution(self):
        """Test taking screenshot with custom resolution."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "path": "/screenshots/1080p.png"}
        )

        result = self.service.take_screenshot(resolution=[1920, 1080])

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["resolution"] == [1920, 1080]

    def test_take_screenshot_all_parameters(self):
        """Test taking screenshot with all parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "path": "/screenshots/full.png"}
        )

        result = self.service.take_screenshot(
            filename="full.png", show_ui=False, resolution=[2560, 1440]
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["filename"] == "full.png"
        assert params["show_ui"] is False
        assert params["resolution"] == [2560, 1440]

    def test_take_screenshot_failure(self):
        """Test taking screenshot with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Screenshot failed"
        )

        result = self.service.take_screenshot(filename="test.png")

        assert result.is_failure
        assert result.get_error() == "Screenshot failed"
