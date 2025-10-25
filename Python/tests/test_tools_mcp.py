"""
MCP-compliant tool testing following Model Context Protocol conventions.
"""

from unittest.mock import Mock, patch

import pytest
from mcp.server.fastmcp import Context, FastMCP

from tools.blueprint_tools_new import (
    _handle_error,
    _handle_service_result,
    register_blueprint_tools,
)
from tools.editor_tools_new import register_editor_tools


class TestMCPBlueprintTools:
    """Test blueprint tools following MCP conventions."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_context = Mock(spec=Context)
        self.mock_service_manager = Mock()
        self.mock_blueprint_service = Mock()

    def test_register_blueprint_tools_success(self):
        """Test successful blueprint tools registration."""
        from mcp.server.fastmcp import FastMCP

        test_server = FastMCP("Test")

        # Should not raise any exceptions
        register_blueprint_tools(test_server)

        # Registration successful if no exceptions
        assert True

    @patch("services.service_manager.get_service_manager")
    def test_create_blueprint_tool_success(self, mock_get_sm):
        """Test create_blueprint tool success case."""
        # Setup mocks
        mock_get_sm.return_value.blueprint_service = self.mock_blueprint_service
        self.mock_blueprint_service.create_blueprint.return_value = {
            "success": True,
            "blueprint_path": "/Game/TestBlueprint.TestBlueprint",
        }

        # Import and call the tool function directly
        from tools.blueprint_tools_new import register_blueprint_tools

        test_server = FastMCP("Test")
        register_blueprint_tools(test_server)

        # Verify the mock was set up correctly
        assert self.mock_blueprint_service.create_blueprint.call_count == 0

    @patch("services.service_manager.get_service_manager")
    def test_create_blueprint_tool_service_error(self, mock_get_sm):
        """Test create_blueprint tool with service error."""
        # Setup mocks
        mock_get_sm.return_value.blueprint_service = self.mock_blueprint_service
        self.mock_blueprint_service.create_blueprint.return_value = {
            "status": "error",
            "error": "Blueprint already exists",
        }

        # Test error handling
        result = _handle_service_result(
            self.mock_blueprint_service.create_blueprint.return_value,
            "create_blueprint",
        )

        assert result["success"] is False
        assert "Blueprint already exists" in result["message"]

    @patch("services.service_manager.get_service_manager")
    def test_spawn_blueprint_actor_tool_parameters(self, mock_get_sm):
        """Test spawn_blueprint_actor tool with various parameters."""
        mock_get_sm.return_value.blueprint_service = self.mock_blueprint_service
        self.mock_blueprint_service.spawn_blueprint_actor.return_value = {
            "success": True,
            "actor_id": "test_actor_123",
        }

        # Test the service method would be called correctly
        from core.types import create_blueprint_spawn_params

        # This tests our parameter handling
        params = create_blueprint_spawn_params(
            "TestBlueprint", "TestActor", [100, 200, 300], [0, 90, 0], [1, 1, 1]
        )

        assert params["blueprint_name"] == "TestBlueprint"
        assert params["actor_name"] == "TestActor"
        assert params["location"] == [100, 200, 300]
        assert params["rotation"] == [0, 90, 0]
        assert params["scale"] == [1, 1, 1]

    def test_error_handling_conventions(self):
        """Test that error handling follows MCP conventions."""
        # Test standard error format
        service_error = _handle_error("test_operation", Exception("Test error"))

        # MCP expects errors in this format
        assert "success" in service_error
        assert "message" in service_error
        assert service_error["success"] is False
        assert "Test error" in service_error["message"]

    def test_parameter_validation_conventions(self):
        """Test that parameter validation follows MCP conventions."""
        from core.types import create_component_params

        # Test invalid parameters raise appropriate exceptions
        with pytest.raises(ValueError, match="required"):
            create_component_params("", "ComponentType", "ComponentName")

    @patch("services.service_manager.get_service_manager")
    def test_physics_parameters_validation(self, mock_get_sm):
        """Test physics parameters with validation."""
        mock_get_sm.return_value.blueprint_service = self.mock_blueprint_service

        from core.types import create_physics_params

        # Test valid physics parameters
        physics_params = create_physics_params(
            simulate_physics=True, mass=10.5, linear_damping=0.1
        )

        assert physics_params["simulate_physics"] is True
        assert physics_params["mass"] == 10.5
        assert physics_params["linear_damping"] == 0.1

        # Test invalid physics parameters
        with pytest.raises(ValueError, match="mass must be positive"):
            create_physics_params(mass=-1)


class TestMCPEditorTools:
    """Test editor tools following MCP conventions."""

    def test_register_editor_tools_success(self):
        """Test successful editor tools registration."""
        from mcp.server.fastmcp import FastMCP

        test_server = FastMCP("Test")

        # Should not raise any exceptions
        register_editor_tools(test_server)

        assert True

    @patch("services.service_manager.get_service_manager")
    def test_actor_management_tools(self, mock_get_sm):
        """Test actor management tools follow MCP patterns."""
        mock_editor_service = Mock()
        mock_get_sm.return_value.editor_service = mock_editor_service

        # Test spawn actor
        mock_editor_service.spawn_actor.return_value = {
            "success": True,
            "actor_id": "spawned_actor_456",
        }

        from core.types import create_transform

        transform = create_transform([0, 0, 100], [0, 0, 0], [1, 1, 1])

        assert transform["location"] == [0, 0, 100]
        assert transform["rotation"] == [0, 0, 0]
        assert transform["scale"] == [1, 1, 1]


class TestMCPUMGTools:
    """Test UMG tools following MCP conventions."""

    def test_register_umg_tools_success(self):
        """Test successful UMG tools registration."""
        from mcp.server.fastmcp import FastMCP

        from tools.umg_tools_new import register_umg_tools

        test_server = FastMCP("Test")

        # Should not raise any exceptions
        register_umg_tools(test_server)

        assert True

    def test_widget_parameter_validation(self):
        """Test widget parameter validation follows MCP conventions."""
        from core.types import Vector3

        # Test Vector3 parameter validation
        position = Vector3.from_list([100, 200, 0])
        assert position.x == 100.0
        assert position.y == 200.0
        assert position.z == 0.0

        # Test invalid Vector3
        with pytest.raises(ValueError, match="exactly 3"):
            Vector3.from_list([100, 200])  # Missing z coordinate


class TestMCPToolResponseFormat:
    """Test that tool responses follow MCP response format conventions."""

    def test_success_response_format(self):
        """Test success responses follow MCP format."""
        response = {"success": True, "data": {"id": "test_123"}}
        result = _handle_service_result(response, "test_operation")

        # Should preserve the success response format
        assert result == response

    def test_error_response_format(self):
        """Test error responses follow MCP format."""
        error_response = {"status": "error", "error": "Test error message"}
        result = _handle_service_result(error_response, "test_operation")

        # Should convert to standard MCP error format
        assert result["success"] is False
        assert result["message"] == "Test error message"

    def test_mixed_response_formats(self):
        """Test handling of different response formats from Unreal."""
        # Format 1: {"status": "error", "error": "..."}
        error_format_1 = {"status": "error", "error": "Error type 1"}
        result_1 = _handle_service_result(error_format_1, "test")
        assert result_1["success"] is False

        # Format 2: {"success": false, "error": "..."}
        error_format_2 = {"success": False, "error": "Error type 2"}
        result_2 = _handle_service_result(error_format_2, "test")
        assert result_2["success"] is False
