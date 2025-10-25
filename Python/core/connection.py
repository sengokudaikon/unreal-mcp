"""
Unreal Engine connection management.
"""

import json
import logging
import socket
from typing import Any, Dict, Optional

from core.errors import ConnectionError

logger = logging.getLogger("UnrealMCP")


class UnrealConnection:
    """Manages connection to an Unreal Engine instance."""

    def __init__(self, host: str = "127.0.0.1", port: int = 55557):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.connected = False

    def connect(self, timeout: int = 5) -> None:
        """Connect to the Unreal Engine instance."""
        try:
            self._close_existing_socket()

            logger.info(f"Connecting to Unreal at {self.host}:{self.port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)

            # Set socket options for better stability
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)

            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info("Connected to Unreal Engine")

        except Exception as e:
            logger.error(f"Failed to connect to Unreal: {e}")
            self.connected = False
            raise ConnectionError(f"Connection failed: {e}")

    def disconnect(self):
        """Disconnect from the Unreal Engine instance."""
        self._close_existing_socket()
        self.connected = False

    def send_command(
        self, command: str, params: Dict[str, Any] = None, timeout: int = 5
    ) -> Dict[str, Any]:
        """Send a command to Unreal Engine and get the response."""
        # Unreal closes connections after each command, so we reconnect each time
        self.disconnect()

        try:
            self.connect(timeout)
        except ConnectionError as e:
            return {"status": "error", "error": str(e)}

        try:
            command_obj = {"type": command, "params": params or {}}

            command_json = json.dumps(command_obj)
            logger.info(f"Sending command: {command_json}")

            if not self.socket:
                return {"status": "error", "error": "No socket available"}

            self.socket.sendall(command_json.encode("utf-8"))

            # Receive response
            response_data = self._receive_full_response()
            if isinstance(response_data, dict) and "error" in response_data:
                return response_data

            response = json.loads(response_data.decode("utf-8"))
            logger.info(f"Complete response from Unreal: {response}")

            # Process response for errors
            return self._process_response(response)

        except Exception as e:
            logger.error(f"Error sending command: {e}")
            return {"status": "error", "error": f"Command failed: {e}"}
        finally:
            # Always disconnect after command (Unreal closes it anyway)
            self.disconnect()

    def _close_existing_socket(self):
        """Close any existing socket."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
        self.socket = None

    def _receive_full_response(self) -> bytes:
        """Receive a complete response from Unreal, handling chunked data."""
        if not self.socket:
            return {"status": "error", "error": "No socket available"}

        chunks = []
        try:
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    if not chunks:
                        raise ConnectionError("Connection closed before receiving data")
                    break
                chunks.append(chunk)

                # Try to parse as JSON to check if complete
                data = b"".join(chunks)
                try:
                    json.loads(data.decode("utf-8"))
                    logger.info(f"Received complete response ({len(data)} bytes)")
                    return data
                except json.JSONDecodeError:
                    logger.debug("Received partial response, waiting for more data...")
                    continue

        except socket.timeout:
            logger.warning("Socket timeout during receive")
            if chunks:
                data = b"".join(chunks)
                try:
                    json.loads(data.decode("utf-8"))
                    logger.info(
                        f"Using partial response after timeout ({len(data)} bytes)"
                    )
                    return data
                except Exception:
                    pass
            return {"status": "error", "error": "Timeout receiving Unreal response"}
        except Exception as e:
            logger.error(f"Error during receive: {e}")
            return {"status": "error", "error": f"Receive error: {e}"}

    def _process_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process response and check for errors."""
        # Check for both error formats
        if response.get("status") == "error":
            error_message = response.get("error") or response.get(
                "message", "Unknown Unreal error"
            )
            logger.error(f"Unreal error (status=error): {error_message}")
            if "error" not in response:
                response["error"] = error_message
            return response
        elif response.get("success") is False:
            error_message = response.get("error") or response.get(
                "message", "Unknown Unreal error"
            )
            logger.error(f"Unreal error (success=false): {error_message}")
            # Convert to standard format
            return {"status": "error", "error": error_message}

        return response
