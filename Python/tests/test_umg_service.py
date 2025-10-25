"""
Tests for UMGService.
"""

from unittest.mock import Mock

import pytest

from core.connection import UnrealConnection
from core.types import Result, Vector3
from services.umg_service import UMGService


class TestUMGService:
    """Test UMGService class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_connection = Mock(spec=UnrealConnection)
        self.service = UMGService(self.mock_connection)

    def test_initialization(self):
        """Test service initialization."""
        assert self.service.connection == self.mock_connection

    # create_widget_blueprint tests
    def test_create_widget_blueprint_with_defaults(self):
        """Test creating widget blueprint with default parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "widget_name": "WBP_MainMenu"}
        )

        result = self.service.create_widget_blueprint("WBP_MainMenu")

        self.mock_connection.send_command.assert_called_once_with(
            "create_umg_widget_blueprint",
            {
                "widget_name": "WBP_MainMenu",
                "parent_class": "UserWidget",
                "path": "/Game/UI",
            },
        )
        assert result.is_success
        assert result.get_value()["widget_name"] == "WBP_MainMenu"

    def test_create_widget_blueprint_custom_parent(self):
        """Test creating widget blueprint with custom parent class."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "widget_name": "WBP_Custom"}
        )

        result = self.service.create_widget_blueprint(
            "WBP_Custom", parent_class="UserWidget"
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["parent_class"] == "UserWidget"

    def test_create_widget_blueprint_custom_path(self):
        """Test creating widget blueprint with custom path."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "widget_name": "WBP_Custom"}
        )

        result = self.service.create_widget_blueprint(
            "WBP_Custom", path="/Game/UI/Menus"
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["path"] == "/Game/UI/Menus"

    def test_create_widget_blueprint_all_parameters(self):
        """Test creating widget blueprint with all parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "widget_name": "WBP_Full"}
        )

        result = self.service.create_widget_blueprint(
            "WBP_Full", parent_class="CanvasPanel", path="/Game/UI/Custom"
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["widget_name"] == "WBP_Full"
        assert params["parent_class"] == "CanvasPanel"
        assert params["path"] == "/Game/UI/Custom"

    def test_create_widget_blueprint_failure(self):
        """Test creating widget blueprint with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Widget already exists"
        )

        result = self.service.create_widget_blueprint("WBP_Existing")

        assert result.is_failure
        assert result.get_error() == "Widget already exists"

    # add_text_block tests
    def test_add_text_block_with_defaults(self):
        """Test adding text block with default parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "text_block_name": "TextBlock_1"}
        )

        result = self.service.add_text_block("WBP_MainMenu", "TextBlock_1")

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "add_text_block_to_widget"
        params = call_args[0][1]
        assert params["widget_name"] == "WBP_MainMenu"
        assert params["text_block_name"] == "TextBlock_1"
        assert params["text"] == ""
        assert params["position"] == [0.0, 0.0]
        assert params["size"] == [200, 50]
        assert params["font_size"] == 12
        assert params["color"] == [1, 1, 1, 1]

    def test_add_text_block_with_text(self):
        """Test adding text block with text content."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_text_block("WBP_MainMenu", "Title", text="Main Menu")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["text"] == "Main Menu"

    def test_add_text_block_with_position(self):
        """Test adding text block with custom position."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        position = Vector3(100, 200, 0)
        result = self.service.add_text_block(
            "WBP_MainMenu", "TextBlock_1", position=position
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["position"] == [100.0, 200.0]

    def test_add_text_block_with_size(self):
        """Test adding text block with custom size."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_text_block(
            "WBP_MainMenu", "TextBlock_1", size=[400, 100]
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["size"] == [400, 100]

    def test_add_text_block_with_font_size(self):
        """Test adding text block with custom font size."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_text_block(
            "WBP_MainMenu", "TextBlock_1", font_size=24
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["font_size"] == 24

    def test_add_text_block_with_color(self):
        """Test adding text block with custom color."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_text_block(
            "WBP_MainMenu", "TextBlock_1", color=[1, 0, 0, 1]
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["color"] == [1, 0, 0, 1]

    def test_add_text_block_all_parameters(self):
        """Test adding text block with all parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        position = Vector3(50, 100, 0)
        result = self.service.add_text_block(
            "WBP_MainMenu",
            "Title",
            text="Game Title",
            position=position,
            size=[500, 150],
            font_size=48,
            color=[1, 1, 1, 1],
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["widget_name"] == "WBP_MainMenu"
        assert params["text_block_name"] == "Title"
        assert params["text"] == "Game Title"
        assert params["position"] == [50.0, 100.0]
        assert params["size"] == [500, 150]
        assert params["font_size"] == 48
        assert params["color"] == [1, 1, 1, 1]

    def test_add_text_block_failure(self):
        """Test adding text block with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Widget not found"
        )

        result = self.service.add_text_block("NonExistent", "TextBlock_1")

        assert result.is_failure
        assert result.get_error() == "Widget not found"

    # add_button tests
    def test_add_button_with_defaults(self):
        """Test adding button with default parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "button_name": "Button_1"}
        )

        result = self.service.add_button("WBP_MainMenu", "Button_1")

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "add_button_to_widget"
        params = call_args[0][1]
        assert params["widget_name"] == "WBP_MainMenu"
        assert params["button_name"] == "Button_1"
        assert params["text"] == ""
        assert params["position"] == [0.0, 0.0]
        assert params["size"] == [200, 50]
        assert params["font_size"] == 12
        assert params["color"] == [1, 1, 1, 1]
        assert params["background_color"] == [0.1, 0.1, 0.1, 1]

    def test_add_button_with_text(self):
        """Test adding button with text."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_button("WBP_MainMenu", "PlayButton", text="Play")

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["text"] == "Play"

    def test_add_button_with_position(self):
        """Test adding button with custom position."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        position = Vector3(150, 250, 0)
        result = self.service.add_button("WBP_MainMenu", "Button_1", position=position)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["position"] == [150.0, 250.0]

    def test_add_button_with_size(self):
        """Test adding button with custom size."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_button("WBP_MainMenu", "Button_1", size=[300, 75])

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["size"] == [300, 75]

    def test_add_button_with_font_size(self):
        """Test adding button with custom font size."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_button("WBP_MainMenu", "Button_1", font_size=18)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["font_size"] == 18

    def test_add_button_with_colors(self):
        """Test adding button with custom colors."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_button(
            "WBP_MainMenu",
            "Button_1",
            color=[0, 1, 0, 1],
            background_color=[0.2, 0.2, 0.2, 1],
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["color"] == [0, 1, 0, 1]
        assert params["background_color"] == [0.2, 0.2, 0.2, 1]

    def test_add_button_all_parameters(self):
        """Test adding button with all parameters."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        position = Vector3(200, 300, 0)
        result = self.service.add_button(
            "WBP_MainMenu",
            "PlayButton",
            text="Start Game",
            position=position,
            size=[250, 100],
            font_size=32,
            color=[1, 1, 0, 1],
            background_color=[0.3, 0.3, 0.3, 1],
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["widget_name"] == "WBP_MainMenu"
        assert params["button_name"] == "PlayButton"
        assert params["text"] == "Start Game"
        assert params["position"] == [200.0, 300.0]
        assert params["size"] == [250, 100]
        assert params["font_size"] == 32
        assert params["color"] == [1, 1, 0, 1]
        assert params["background_color"] == [0.3, 0.3, 0.3, 1]

    def test_add_button_failure(self):
        """Test adding button with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Widget not found"
        )

        result = self.service.add_button("NonExistent", "Button_1")

        assert result.is_failure
        assert result.get_error() == "Widget not found"

    # bind_widget_event tests
    def test_bind_widget_event_without_function(self):
        """Test binding widget event without function name."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.bind_widget_event(
            "WBP_MainMenu", "PlayButton", "OnClicked"
        )

        self.mock_connection.send_command.assert_called_once_with(
            "bind_widget_event",
            {
                "widget_name": "WBP_MainMenu",
                "widget_component_name": "PlayButton",
                "event_name": "OnClicked",
            },
        )
        assert result.is_success

    def test_bind_widget_event_with_function(self):
        """Test binding widget event with function name."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.bind_widget_event(
            "WBP_MainMenu",
            "PlayButton",
            "OnClicked",
            function_name="OnPlayButtonClicked",
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["function_name"] == "OnPlayButtonClicked"

    def test_bind_widget_event_failure(self):
        """Test binding widget event with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Component not found"
        )

        result = self.service.bind_widget_event(
            "WBP_MainMenu", "NonExistent", "OnClicked"
        )

        assert result.is_failure
        assert result.get_error() == "Component not found"

    # add_widget_to_viewport tests
    def test_add_widget_to_viewport_default_z_order(self):
        """Test adding widget to viewport with default z-order."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True, "added": True}
        )

        result = self.service.add_widget_to_viewport("WBP_MainMenu")

        self.mock_connection.send_command.assert_called_once_with(
            "add_widget_to_viewport", {"widget_name": "WBP_MainMenu", "z_order": 0}
        )
        assert result.is_success
        assert result.get_value()["added"] is True

    def test_add_widget_to_viewport_custom_z_order(self):
        """Test adding widget to viewport with custom z-order."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_widget_to_viewport("WBP_Overlay", z_order=10)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["widget_name"] == "WBP_Overlay"
        assert params["z_order"] == 10

    def test_add_widget_to_viewport_negative_z_order(self):
        """Test adding widget to viewport with negative z-order."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.add_widget_to_viewport("WBP_Background", z_order=-5)

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["z_order"] == -5

    def test_add_widget_to_viewport_failure(self):
        """Test adding widget to viewport with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Widget not found"
        )

        result = self.service.add_widget_to_viewport("NonExistent")

        assert result.is_failure
        assert result.get_error() == "Widget not found"

    # set_text_block_binding tests
    def test_set_text_block_binding_with_defaults(self):
        """Test setting text block binding with default binding type."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.set_text_block_binding(
            "WBP_MainMenu", "HealthText", "CurrentHealth"
        )

        self.mock_connection.send_command.assert_called_once_with(
            "set_text_block_binding",
            {
                "widget_name": "WBP_MainMenu",
                "text_block_name": "HealthText",
                "binding_property": "CurrentHealth",
                "binding_type": "Text",
            },
        )
        assert result.is_success

    def test_set_text_block_binding_custom_type(self):
        """Test setting text block binding with custom binding type."""
        self.mock_connection.send_command.return_value = Result.success(
            {"success": True}
        )

        result = self.service.set_text_block_binding(
            "WBP_MainMenu",
            "HealthText",
            "CurrentHealth",
            binding_type="Visibility",
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["binding_type"] == "Visibility"

    def test_set_text_block_binding_failure(self):
        """Test setting text block binding with failure."""
        self.mock_connection.send_command.return_value = Result.failure(
            "Text block not found"
        )

        result = self.service.set_text_block_binding(
            "WBP_MainMenu", "NonExistent", "Property"
        )

        assert result.is_failure
        assert result.get_error() == "Text block not found"
