"""
Custom exceptions for Unreal MCP.
"""


class UnrealMCPError(Exception):
    """Base exception for Unreal MCP errors."""

    pass


class ConnectionError(UnrealMCPError):
    """Raised when connection to Unreal Engine fails."""

    pass


class CommandError(UnrealMCPError):
    """Raised when a command to Unreal Engine fails."""

    pass


class ValidationError(UnrealMCPError):
    """Raised when parameter validation fails."""

    pass


class ResponseError(UnrealMCPError):
    """Raised when Unreal response indicates an error."""

    pass
