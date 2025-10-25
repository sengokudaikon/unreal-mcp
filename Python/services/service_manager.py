"""
Service manager for handling dependency injection and service lifecycle.
"""

import logging
from typing import Optional

from core.connection import UnrealConnection
from core.errors import ConnectionError
from services.blueprint_service import BlueprintService
from services.editor_service import EditorService
from services.project_service import ProjectService
from services.umg_service import UMGService

logger = logging.getLogger("UnrealMCP")


class ServiceManager:
    """Manages all services and their dependencies."""

    def __init__(self):
        self.connection: Optional[UnrealConnection] = None
        self._blueprint_service: Optional[BlueprintService] = None
        self._editor_service: Optional[EditorService] = None
        self._umg_service: Optional[UMGService] = None
        self._project_service: Optional[ProjectService] = None

    def initialize(self, host: str = "127.0.0.1", port: int = 55557) -> None:
        """Initialize the service manager with a connection."""
        try:
            self.connection = UnrealConnection(host, port)
            # Test connection
            self.connection.connect()
            # Disconnect after test - services will reconnect as needed
            self.connection.disconnect()
            logger.info("Service manager initialized successfully")
        except Exception as e:
            logger.error(f"Service manager initialization failed: {e}")
            raise ConnectionError(f"Service manager initialization failed: {e}")

    @property
    def blueprint_service(self) -> BlueprintService:
        """Get the Blueprint service."""
        if self._blueprint_service is None:
            if self.connection is None:
                raise RuntimeError("Service manager not initialized")
            self._blueprint_service = BlueprintService(self.connection)
        return self._blueprint_service

    @property
    def editor_service(self) -> EditorService:
        """Get the Editor service."""
        if self._editor_service is None:
            if self.connection is None:
                raise RuntimeError("Service manager not initialized")
            self._editor_service = EditorService(self.connection)
        return self._editor_service

    @property
    def umg_service(self) -> UMGService:
        """Get the UMG service."""
        if self._umg_service is None:
            if self.connection is None:
                raise RuntimeError("Service manager not initialized")
            self._umg_service = UMGService(self.connection)
        return self._umg_service

    @property
    def project_service(self) -> ProjectService:
        """Get the Project service."""
        if self._project_service is None:
            if self.connection is None:
                raise RuntimeError("Service manager not initialized")
            self._project_service = ProjectService(self.connection)
        return self._project_service

    def shutdown(self):
        """Shutdown the service manager and clean up resources."""
        if self.connection:
            self.connection.disconnect()
            logger.info("Service manager shutdown complete")


# Global service manager instance
_service_manager: Optional[ServiceManager] = None


def get_service_manager() -> ServiceManager:
    """Get the global service manager instance."""
    global _service_manager
    if _service_manager is None:
        _service_manager = ServiceManager()
    return _service_manager


def initialize_services(host: str = "127.0.0.1", port: int = 55557) -> None:
    """Initialize the global service manager."""
    get_service_manager().initialize(host, port)


def shutdown_services():
    """Shutdown the global service manager."""
    global _service_manager
    if _service_manager:
        _service_manager.shutdown()
        _service_manager = None
