"""
Tests for BlueprintService.
"""

from unittest.mock import Mock, patch

import pytest

from core.connection import UnrealConnection
from services.blueprint_service import BlueprintService


class TestBlueprintService:
    """Test BlueprintService class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_connection = Mock(spec=UnrealConnection)
        self.service = BlueprintService(self.mock_connection)

    def test_initialization(self):
        """Test service initialization."""
        assert self.service.connection == self.mock_connection

    def test_create_blueprint_success(self):
        """Test creating a blueprint successfully."""
        self.mock_connection.send_command.return_value = {
            "success": True,
            "blueprint_name": "BP_Test",
        }

        result = self.service.create_blueprint("BP_Test", "Actor")

        self.mock_connection.send_command.assert_called_once_with(
            "create_blueprint", {"name": "BP_Test", "parent_class": "Actor"}
        )
        assert result["success"] is True
        assert result["blueprint_name"] == "BP_Test"

    def test_create_blueprint_error(self):
        """Test creating a blueprint with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Blueprint already exists",
        }

        result = self.service.create_blueprint("BP_Test", "Actor")

        assert result["status"] == "error"
        assert result["error"] == "Blueprint already exists"

    def test_spawn_blueprint_actor_with_defaults(self):
        """Test spawning blueprint actor with default transform."""
        self.mock_connection.send_command.return_value = {
            "success": True,
            "actor_name": "TestActor",
        }

        result = self.service.spawn_blueprint_actor("BP_Test", "TestActor")

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "spawn_blueprint_actor"
        params = call_args[0][1]
        assert params["blueprint_name"] == "BP_Test"
        assert params["actor_name"] == "TestActor"
        assert params["location"] == [0.0, 0.0, 0.0]
        assert params["rotation"] == [0.0, 0.0, 0.0]
        assert params["scale"] == [1.0, 1.0, 1.0]

    def test_spawn_blueprint_actor_with_transform(self):
        """Test spawning blueprint actor with custom transform."""
        self.mock_connection.send_command.return_value = {"success": True}

        result = self.service.spawn_blueprint_actor(
            "BP_Test",
            "TestActor",
            location=[100, 200, 300],
            rotation=[0, 90, 0],
            scale=[2, 2, 2],
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["location"] == [100, 200, 300]
        assert params["rotation"] == [0, 90, 0]
        assert params["scale"] == [2, 2, 2]

    def test_spawn_blueprint_actor_error(self):
        """Test spawning blueprint actor with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Blueprint not found",
        }

        result = self.service.spawn_blueprint_actor("BP_Test", "TestActor")

        assert result["status"] == "error"
        assert result["error"] == "Blueprint not found"

    def test_add_component_with_defaults(self):
        """Test adding component with default values."""
        self.mock_connection.send_command.return_value = {"success": True}

        result = self.service.add_component(
            "BP_Test", "StaticMeshComponent", "TestMesh"
        )

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "add_component_to_blueprint"
        params = call_args[0][1]
        assert params["blueprint_name"] == "BP_Test"
        assert params["component_type"] == "StaticMeshComponent"
        assert params["component_name"] == "TestMesh"
        assert params["location"] == [0.0, 0.0, 0.0]
        assert params["rotation"] == [0.0, 0.0, 0.0]
        assert params["scale"] == [1.0, 1.0, 1.0]

    def test_add_component_with_properties(self):
        """Test adding component with custom properties."""
        self.mock_connection.send_command.return_value = {"success": True}

        properties = {"static_mesh": "/Engine/BasicShapes/Cube.Cube"}
        result = self.service.add_component(
            "BP_Test",
            "StaticMeshComponent",
            "TestMesh",
            location=[0, 0, 100],
            rotation=[0, 0, 45],
            scale=[2, 2, 2],
            properties=properties,
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["location"] == [0, 0, 100]
        assert params["rotation"] == [0, 0, 45]
        assert params["scale"] == [2, 2, 2]
        assert params["component_properties"] == properties

    def test_add_component_error(self):
        """Test adding component with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Invalid component type",
        }

        result = self.service.add_component("BP_Test", "InvalidComponent", "TestMesh")

        assert result["status"] == "error"
        assert result["error"] == "Invalid component type"

    def test_set_static_mesh_success(self):
        """Test setting static mesh successfully."""
        self.mock_connection.send_command.return_value = {"success": True}

        result = self.service.set_static_mesh(
            "BP_Test", "MeshComponent", "/Engine/BasicShapes/Cube.Cube"
        )

        self.mock_connection.send_command.assert_called_once_with(
            "set_static_mesh_properties",
            {
                "blueprint_name": "BP_Test",
                "component_name": "MeshComponent",
                "static_mesh": "/Engine/BasicShapes/Cube.Cube",
            },
        )
        assert result["success"] is True

    def test_set_static_mesh_error(self):
        """Test setting static mesh with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Static mesh not found",
        }

        result = self.service.set_static_mesh(
            "BP_Test", "MeshComponent", "/Invalid/Path.Path"
        )

        assert result["status"] == "error"
        assert result["error"] == "Static mesh not found"

    def test_set_physics_properties_defaults(self):
        """Test setting physics properties with defaults."""
        self.mock_connection.send_command.return_value = {"success": True}

        result = self.service.set_physics_properties("BP_Test", "MeshComponent")

        call_args = self.mock_connection.send_command.call_args
        assert call_args[0][0] == "set_physics_properties"
        params = call_args[0][1]
        assert params["blueprint_name"] == "BP_Test"
        assert params["component_name"] == "MeshComponent"
        assert params["simulate_physics"] is True
        assert params["gravity_enabled"] is True
        assert params["mass"] == 1.0
        assert params["linear_damping"] == 0.01
        assert params["angular_damping"] == 0.0

    def test_set_physics_properties_custom(self):
        """Test setting physics properties with custom values."""
        self.mock_connection.send_command.return_value = {"success": True}

        result = self.service.set_physics_properties(
            "BP_Test",
            "MeshComponent",
            simulate_physics=True,
            gravity_enabled=False,
            mass=10.5,
            linear_damping=0.1,
            angular_damping=0.2,
        )

        call_args = self.mock_connection.send_command.call_args
        params = call_args[0][1]
        assert params["simulate_physics"] is True
        assert params["gravity_enabled"] is False
        assert params["mass"] == 10.5
        assert params["linear_damping"] == 0.1
        assert params["angular_damping"] == 0.2

    def test_set_physics_properties_error(self):
        """Test setting physics properties with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Component not found",
        }

        result = self.service.set_physics_properties("BP_Test", "MeshComponent")

        assert result["status"] == "error"
        assert result["error"] == "Component not found"

    def test_compile_blueprint_success(self):
        """Test compiling blueprint successfully."""
        self.mock_connection.send_command.return_value = {
            "success": True,
            "compiled": True,
        }

        result = self.service.compile_blueprint("BP_Test")

        self.mock_connection.send_command.assert_called_once_with(
            "compile_blueprint", {"blueprint_name": "BP_Test"}
        )
        assert result["success"] is True
        assert result["compiled"] is True

    def test_compile_blueprint_error(self):
        """Test compiling blueprint with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Compilation failed",
        }

        result = self.service.compile_blueprint("BP_Test")

        assert result["status"] == "error"
        assert result["error"] == "Compilation failed"

    def test_set_blueprint_property_success(self):
        """Test setting blueprint property successfully."""
        self.mock_connection.send_command.return_value = {"success": True}

        result = self.service.set_blueprint_property("BP_Test", "MaxHealth", "100.0")

        self.mock_connection.send_command.assert_called_once_with(
            "set_blueprint_property",
            {
                "blueprint_name": "BP_Test",
                "property_name": "MaxHealth",
                "property_value": "100.0",
            },
        )
        assert result["success"] is True

    def test_set_blueprint_property_error(self):
        """Test setting blueprint property with error."""
        self.mock_connection.send_command.return_value = {
            "status": "error",
            "error": "Property not found",
        }

        result = self.service.set_blueprint_property("BP_Test", "InvalidProp", "value")

        assert result["status"] == "error"
        assert result["error"] == "Property not found"
