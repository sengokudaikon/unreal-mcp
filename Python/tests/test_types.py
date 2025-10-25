"""
Tests for core types and utilities.
"""

import pytest

from core.types import (
    Vector3,
    create_blueprint_spawn_params,
    create_component_params,
    create_physics_params,
    create_transform,
)


class TestVector3:
    """Test Vector3 NamedTuple."""

    def test_vector3_creation(self):
        """Test Vector3 creation."""
        v = Vector3(1.0, 2.0, 3.0)
        assert v.x == 1.0
        assert v.y == 2.0
        assert v.z == 3.0

    def test_vector3_from_list_valid(self):
        """Test Vector3.from_list with valid input."""
        v = Vector3.from_list([1, 2, 3])
        assert v == Vector3(1.0, 2.0, 3.0)

    def test_vector3_from_list_invalid_length(self):
        """Test Vector3.from_list with invalid length."""
        with pytest.raises(ValueError, match="Vector3 requires exactly 3 float values"):
            Vector3.from_list([1, 2])

    def test_vector3_from_list_string_conversion(self):
        """Test Vector3.from_list converts strings to float."""
        v = Vector3.from_list(["1", "2", "3"])
        assert v == Vector3(1.0, 2.0, 3.0)


class TestTransformUtils:
    """Test transform utility functions."""

    def test_create_transform_defaults(self):
        """Test create_transform with default values."""
        transform = create_transform()
        assert transform["location"] == [0.0, 0.0, 0.0]
        assert transform["rotation"] == [0.0, 0.0, 0.0]
        assert transform["scale"] == [1.0, 1.0, 1.0]

    def test_create_transform_custom_values(self):
        """Test create_transform with custom values."""
        transform = create_transform(
            location=[1, 2, 3], rotation=[45, 90, 135], scale=[2, 2, 2]
        )
        assert transform["location"] == [1, 2, 3]
        assert transform["rotation"] == [45, 90, 135]
        assert transform["scale"] == [2, 2, 2]

    def test_create_transform_partial_values(self):
        """Test create_transform with partial values."""
        transform = create_transform(location=[5, 10, 15])
        assert transform["location"] == [5, 10, 15]
        assert transform["rotation"] == [0.0, 0.0, 0.0]
        assert transform["scale"] == [1.0, 1.0, 1.0]


class TestBlueprintSpawnParams:
    """Test blueprint spawn parameter utilities."""

    def test_create_blueprint_spawn_params_valid(self):
        """Test create_blueprint_spawn_params with valid input."""
        params = create_blueprint_spawn_params(
            "TestBlueprint", "TestActor", [10, 20, 30], [0, 90, 0], [1, 1, 1]
        )
        assert params["blueprint_name"] == "TestBlueprint"
        assert params["actor_name"] == "TestActor"
        assert params["location"] == [10, 20, 30]
        assert params["rotation"] == [0, 90, 0]
        assert params["scale"] == [1, 1, 1]

    def test_create_blueprint_spawn_params_defaults(self):
        """Test create_blueprint_spawn_params with default values."""
        params = create_blueprint_spawn_params("BP_Test", "Actor_Test")
        assert params["blueprint_name"] == "BP_Test"
        assert params["actor_name"] == "Actor_Test"
        assert params["location"] == [0.0, 0.0, 0.0]
        assert params["rotation"] == [0.0, 0.0, 0.0]
        assert params["scale"] == [1.0, 1.0, 1.0]

    def test_create_blueprint_spawn_params_missing_names(self):
        """Test create_blueprint_spawn_params with missing names."""
        with pytest.raises(
            ValueError, match="blueprint_name and actor_name are required"
        ):
            create_blueprint_spawn_params("", "Actor")

        with pytest.raises(
            ValueError, match="blueprint_name and actor_name are required"
        ):
            create_blueprint_spawn_params("Blueprint", "")

        with pytest.raises(
            ValueError, match="blueprint_name and actor_name are required"
        ):
            create_blueprint_spawn_params("", "")


class TestComponentParams:
    """Test component parameter utilities."""

    def test_create_component_params_valid(self):
        """Test create_component_params with valid input."""
        params = create_component_params(
            "TestBlueprint",
            "StaticMeshComponent",
            "TestMesh",
            [0, 0, 100],
            [0, 0, 0],
            [1, 1, 1],
            {"static_mesh": "/Engine/BasicShapes/Cube.Cube"},
        )
        assert params["blueprint_name"] == "TestBlueprint"
        assert params["component_type"] == "StaticMeshComponent"
        assert params["component_name"] == "TestMesh"
        assert params["location"] == [0, 0, 100]
        assert params["rotation"] == [0, 0, 0]
        assert params["scale"] == [1, 1, 1]
        assert (
            params["component_properties"]["static_mesh"]
            == "/Engine/BasicShapes/Cube.Cube"
        )

    def test_create_component_params_defaults(self):
        """Test create_component_params with default values."""
        params = create_component_params("BP_Test", "MeshComponent", "Mesh")
        assert params["blueprint_name"] == "BP_Test"
        assert params["component_type"] == "MeshComponent"
        assert params["component_name"] == "Mesh"
        assert params["location"] == [0.0, 0.0, 0.0]
        assert params["rotation"] == [0.0, 0.0, 0.0]
        assert params["scale"] == [1.0, 1.0, 1.0]
        assert (
            "component_properties" not in params
        )  # Only added when properties provided

    def test_create_component_params_missing_required(self):
        """Test create_component_params with missing required fields."""
        with pytest.raises(
            ValueError,
            match="blueprint_name, component_type, and component_name are required",
        ):
            create_component_params("", "MeshComponent", "Mesh")

        with pytest.raises(
            ValueError,
            match="blueprint_name, component_type, and component_name are required",
        ):
            create_component_params("Blueprint", "", "Mesh")

        with pytest.raises(
            ValueError,
            match="blueprint_name, component_type, and component_name are required",
        ):
            create_component_params("Blueprint", "MeshComponent", "")


class TestPhysicsParams:
    """Test physics parameter utilities."""

    def test_create_physics_params_defaults(self):
        """Test create_physics_params with default values."""
        params = create_physics_params()
        assert params["simulate_physics"] is True
        assert params["gravity_enabled"] is True
        assert params["mass"] == 1.0
        assert params["linear_damping"] == 0.01
        assert params["angular_damping"] == 0.0

    def test_create_physics_params_custom_values(self):
        """Test create_physics_params with custom values."""
        params = create_physics_params(
            simulate_physics=False,
            gravity_enabled=False,
            mass=10.5,
            linear_damping=0.1,
            angular_damping=0.2,
        )
        assert params["simulate_physics"] is False
        assert params["gravity_enabled"] is False
        assert params["mass"] == 10.5
        assert params["linear_damping"] == 0.1
        assert params["angular_damping"] == 0.2

    def test_create_physics_params_invalid_mass(self):
        """Test create_physics_params with invalid mass."""
        with pytest.raises(ValueError, match="mass must be positive"):
            create_physics_params(mass=0)

        with pytest.raises(ValueError, match="mass must be positive"):
            create_physics_params(mass=-1)

    def test_create_physics_params_invalid_damping(self):
        """Test create_physics_params with invalid damping values."""
        with pytest.raises(ValueError, match="damping values must be non-negative"):
            create_physics_params(linear_damping=-0.1)

        with pytest.raises(ValueError, match="damping values must be non-negative"):
            create_physics_params(angular_damping=-0.1)
