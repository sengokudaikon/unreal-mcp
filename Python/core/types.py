"""
Core types and utilities for Unreal MCP.
Simplified to use standard library types where possible.
"""

from typing import (
    Any,
    Dict,
    Generic,
    List,
    NamedTuple,
    Optional,
    TypedDict,
    TypeVar,
)

T = TypeVar("T")


class Result(Generic[T]):
    """A simple Result type for handling success/failure operations."""

    def __init__(self, success: bool, value: T = None, error: str = None):
        self.success = success
        self.value = value
        self.error = error

    @property
    def is_success(self) -> bool:
        return self.success

    @property
    def is_failure(self) -> bool:
        return not self.success

    def get_value(self) -> T:
        """Get the value if successful, raise exception if failed."""
        if self.is_success:
            return self.value
        raise ValueError(f"Cannot get value from failed result: {self.error}")

    def get_error(self) -> Optional[str]:
        """Get the error message if failed."""
        return self.error

    @classmethod
    def success(cls, value: T = None) -> "Result[T]":
        """Create a successful result."""
        return cls(True, value=value)

    @classmethod
    def failure(cls, error: str) -> "Result[T]":
        """Create a failed result."""
        return cls(False, error=error)


class Vector3(NamedTuple):
    """Simple 3D vector using NamedTuple."""

    x: float
    y: float
    z: float

    @classmethod
    def from_list(cls, values: List[float]) -> "Vector3":
        """Create Vector3 from list, with validation."""
        if len(values) != 3:
            raise ValueError("Vector3 requires exactly 3 float values")
        return cls(float(values[0]), float(values[1]), float(values[2]))


class Transform(NamedTuple):
    """Transform with location, rotation, and scale."""

    location: Vector3
    rotation: Vector3
    scale: Vector3

    def to_dict(self) -> Dict[str, List[float]]:
        """Convert transform to dictionary format."""
        return {
            "location": list(self.location),
            "rotation": list(self.rotation),
            "scale": list(self.scale),
        }


class TransformDict(TypedDict, total=False):
    """TypedDict for transform parameters."""

    location: List[float]
    rotation: List[float]
    scale: List[float]


class BlueprintSpawnDict(TypedDict):
    """TypedDict for blueprint spawn parameters."""

    blueprint_name: str
    actor_name: str
    location: List[float]
    rotation: List[float]
    scale: List[float]


class ComponentDict(TypedDict, total=False):
    """TypedDict for component parameters."""

    blueprint_name: str
    component_type: str
    component_name: str
    location: List[float]
    rotation: List[float]
    scale: List[float]
    component_properties: Dict[str, Any]


class PhysicsDict(TypedDict, total=False):
    """TypedDict for physics parameters."""

    simulate_physics: bool
    gravity_enabled: bool
    mass: float
    linear_damping: float
    angular_damping: float


# Utility functions for parameter building
def create_transform(
    location: List[float] = None,
    rotation: List[float] = None,
    scale: List[float] = None,
) -> TransformDict:
    """Create transform dict with defaults."""
    return {
        "location": location or [0.0, 0.0, 0.0],
        "rotation": rotation or [0.0, 0.0, 0.0],
        "scale": scale or [1.0, 1.0, 1.0],
    }


def create_blueprint_spawn_params(
    blueprint_name: str,
    actor_name: str,
    location: List[float] = None,
    rotation: List[float] = None,
    scale: List[float] = None,
) -> BlueprintSpawnDict:
    """Create blueprint spawn parameters with validation."""
    if not blueprint_name or not actor_name:
        raise ValueError("blueprint_name and actor_name are required")

    return {
        "blueprint_name": blueprint_name,
        "actor_name": actor_name,
        "location": location or [0.0, 0.0, 0.0],
        "rotation": rotation or [0.0, 0.0, 0.0],
        "scale": scale or [1.0, 1.0, 1.0],
    }


def create_component_params(
    blueprint_name: str,
    component_type: str,
    component_name: str,
    location: List[float] = None,
    rotation: List[float] = None,
    scale: List[float] = None,
    properties: Dict[str, Any] = None,
) -> ComponentDict:
    """Create component parameters with validation."""
    if not all([blueprint_name, component_type, component_name]):
        raise ValueError(
            "blueprint_name, component_type, and component_name are required"
        )

    params = {
        "blueprint_name": blueprint_name,
        "component_type": component_type,
        "component_name": component_name,
        "location": location or [0.0, 0.0, 0.0],
        "rotation": rotation or [0.0, 0.0, 0.0],
        "scale": scale or [1.0, 1.0, 1.0],
    }

    if properties:
        params["component_properties"] = properties

    return params


def create_physics_params(
    simulate_physics: bool = True,
    gravity_enabled: bool = True,
    mass: float = 1.0,
    linear_damping: float = 0.01,
    angular_damping: float = 0.0,
) -> PhysicsDict:
    """Create physics parameters with validation."""
    if mass <= 0:
        raise ValueError("mass must be positive")
    if linear_damping < 0 or angular_damping < 0:
        raise ValueError("damping values must be non-negative")

    return {
        "simulate_physics": simulate_physics,
        "gravity_enabled": gravity_enabled,
        "mass": mass,
        "linear_damping": linear_damping,
        "angular_damping": angular_damping,
    }
