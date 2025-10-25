"""
Tests for Unreal connection management.
"""

import json
import socket
from unittest.mock import MagicMock, Mock, patch

import pytest

from core.connection import UnrealConnection
from core.errors import ConnectionError


class TestUnrealConnection:
    """Test UnrealConnection class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.connection = UnrealConnection("127.0.0.1", 12345)

    def test_connection_initialization(self):
        """Test connection initialization."""
        assert self.connection.host == "127.0.0.1"
        assert self.connection.port == 12345
        assert self.connection.socket is None
        assert self.connection.connected is False

    @patch("socket.socket")
    def test_connect_success(self, mock_socket):
        """Test successful connection."""
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        self.connection.connect()

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock_instance.setsockopt.assert_called()
        mock_sock_instance.connect.assert_called_once_with(("127.0.0.1", 12345))
        assert self.connection.connected is True
        assert self.connection.socket == mock_sock_instance

    @patch("socket.socket")
    def test_connect_failure(self, mock_socket):
        """Test connection failure."""
        mock_socket.side_effect = Exception("Connection failed")

        with pytest.raises(ConnectionError, match="Connection failed"):
            self.connection.connect()

        assert self.connection.connected is False

    def test_disconnect(self):
        """Test disconnection."""
        mock_socket = Mock()
        self.connection.socket = mock_socket
        self.connection.connected = True

        self.connection.disconnect()

        mock_socket.close.assert_called_once()
        assert self.connection.socket is None
        assert self.connection.connected is False

    @patch("socket.socket")
    def test_send_command_success(self, mock_socket):
        """Test successful command sending."""
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # Mock successful connection
        mock_sock_instance.recv.side_effect = [
            b'{"success": true, "result": "ok"}'  # Complete JSON response
        ]

        self.connection.connect()

        result = self.connection.send_command("test_command", {"param": "value"})

        assert result["success"] is True
        assert result["result"] == "ok"
        mock_sock_instance.sendall.assert_called_once()
        assert self.connection.socket is None  # Should be disconnected after command

    @patch("socket.socket")
    def test_send_command_connection_failure(self, mock_socket):
        """Test command sending with connection failure."""
        mock_socket.side_effect = Exception("Connection failed")

        result = self.connection.send_command("test_command")

        assert result["status"] == "error"
        assert "Connection failed" in result["error"]

    @patch("socket.socket")
    def test_send_command_unreal_error_response(self, mock_socket):
        """Test command sending with Unreal error response."""
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # Mock error response from Unreal
        mock_sock_instance.recv.side_effect = [
            b'{"status": "error", "error": "Unreal command failed"}'
        ]

        result = self.connection.send_command("test_command")

        assert result["status"] == "error"
        assert result["error"] == "Unreal command failed"

    @patch("socket.socket")
    def test_send_command_chunked_response(self, mock_socket):
        """Test command sending with chunked response."""
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # Mock chunked response
        mock_sock_instance.recv.side_effect = [
            b'{"success": true, ',
            b'"result": "chunked',
            b'_response"}',
        ]

        self.connection.connect()

        result = self.connection.send_command("test_command")

        assert result["success"] is True
        assert result["result"] == "chunked_response"

    @patch("socket.socket")
    def test_receive_timeout(self, mock_socket):
        """Test handling of socket timeout during receive."""
        mock_sock_instance = Mock()
        mock_socket.return_value = mock_sock_instance

        # Mock timeout after partial data
        mock_sock_instance.recv.side_effect = [
            socket.timeout(),
            b'{"success": true}',  # This won't be reached due to timeout handling
        ]

        self.connection.connect()

        result = self.connection.send_command("test_command")

        assert result["status"] == "error"
        assert "Timeout" in result["error"]

    def test_close_existing_socket(self):
        """Test closing existing socket."""
        mock_socket = Mock()
        self.connection.socket = mock_socket

        self.connection._close_existing_socket()

        mock_socket.close.assert_called_once()
        assert self.connection.socket is None

    def test_close_existing_socket_with_exception(self):
        """Test closing existing socket that raises exception."""
        mock_socket = Mock()
        mock_socket.close.side_effect = Exception("Close failed")
        self.connection.socket = mock_socket

        # Should not raise exception
        self.connection._close_existing_socket()

        assert self.connection.socket is None

    def test_process_response_success(self):
        """Test processing successful response."""
        response = {"success": True, "result": "ok"}
        result = self.connection._process_response(response)
        assert result == response

    def test_process_response_error_status(self):
        """Test processing response with error status."""
        response = {"status": "error", "message": "Something went wrong"}
        result = self.connection._process_response(response)
        assert result["status"] == "error"
        assert result["error"] == "Something went wrong"

    def test_process_response_success_false(self):
        """Test processing response with success=false."""
        response = {"success": False, "error": "Command failed"}
        result = self.connection._process_response(response)
        assert result["status"] == "error"
        assert result["error"] == "Command failed"

    def test_process_response_add_error_field(self):
        """Test processing response that has error status but no error field."""
        response = {"status": "error", "message": "Error without error field"}
        result = self.connection._process_response(response)
        assert result["status"] == "error"
        assert result["error"] == "Error without error field"
        assert result["message"] == "Error without error field"
