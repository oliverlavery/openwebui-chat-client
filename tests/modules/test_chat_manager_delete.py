"""
Tests for ChatManager delete_chat functionality (sync version).
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from openwebui_chat_client.modules.chat_manager import ChatManager


class TestChatManagerDeleteChat:
    """Test suite for ChatManager.delete_chat method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_base_client = MagicMock()
        self.mock_base_client.base_url = "http://test.com"
        self.mock_base_client.json_headers = {"Content-Type": "application/json"}

        # Mock session
        self.mock_base_client.session = MagicMock()

        self.manager = ChatManager(self.mock_base_client)

    def test_delete_chat_success(self):
        """Test successful deletion of a specific chat."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        self.mock_base_client.session.delete.return_value = mock_response

        result = self.manager.delete_chat("chat-uuid-123")

        assert result is True
        self.mock_base_client.session.delete.assert_called_once_with(
            "http://test.com/api/v1/chats/chat-uuid-123",
            headers={"Content-Type": "application/json"},
        )

    def test_delete_chat_failure(self):
        """Test failed deletion of a chat."""
        self.mock_base_client.session.delete.side_effect = (
            requests.exceptions.RequestException("Error")
        )

        result = self.manager.delete_chat("chat-uuid-123")

        assert result is False

    def test_delete_chat_empty_id(self):
        """Test deletion with empty chat_id."""
        result = self.manager.delete_chat("")

        assert result is False
        # Should not make any request
        self.mock_base_client.session.delete.assert_not_called()

    def test_delete_chat_none_id(self):
        """Test deletion with None chat_id."""
        result = self.manager.delete_chat(None)

        assert result is False
        # Should not make any request
        self.mock_base_client.session.delete.assert_not_called()

    def test_delete_chat_http_error(self):
        """Test deletion when HTTP error occurs."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )
        self.mock_base_client.session.delete.return_value = mock_response

        result = self.manager.delete_chat("nonexistent-chat")

        assert result is False

    def test_delete_chat_connection_error(self):
        """Test deletion when connection error occurs."""
        self.mock_base_client.session.delete.side_effect = (
            requests.exceptions.ConnectionError("Connection refused")
        )

        result = self.manager.delete_chat("chat-uuid-123")

        assert result is False

    def test_delete_chat_timeout(self):
        """Test deletion when request times out."""
        self.mock_base_client.session.delete.side_effect = (
            requests.exceptions.Timeout("Request timed out")
        )

        result = self.manager.delete_chat("chat-uuid-123")

        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
