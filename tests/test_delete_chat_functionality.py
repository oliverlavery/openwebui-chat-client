"""
Tests for OpenWebUIClient delete_chat functionality.

This test file covers:
- delete_chat() method in the main client
- Integration between client and chat_manager
- Error handling for delete operations
"""

import unittest
from unittest.mock import MagicMock, patch

from openwebui_chat_client import OpenWebUIClient


class TestDeleteChat(unittest.TestCase):
    """Test delete_chat functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = OpenWebUIClient(
            base_url="http://localhost:3000",
            token="test-token",
            default_model_id="test-model",
            skip_model_refresh=True,
        )
        self.client._chat_manager = MagicMock()

    def test_delete_chat_success(self):
        """Test successful chat deletion."""
        self.client._chat_manager.delete_chat = MagicMock(return_value=True)

        result = self.client.delete_chat("chat-uuid-123")

        self.assertTrue(result)
        self.client._chat_manager.delete_chat.assert_called_once_with("chat-uuid-123")

    def test_delete_chat_failure(self):
        """Test failed chat deletion."""
        self.client._chat_manager.delete_chat = MagicMock(return_value=False)

        result = self.client.delete_chat("chat-uuid-123")

        self.assertFalse(result)
        self.client._chat_manager.delete_chat.assert_called_once_with("chat-uuid-123")

    def test_delete_chat_empty_id(self):
        """Test deletion with empty chat_id."""
        self.client._chat_manager.delete_chat = MagicMock(return_value=False)

        result = self.client.delete_chat("")

        self.assertFalse(result)

    def test_delete_chat_exception(self):
        """Test deletion when chat_manager raises exception."""
        self.client._chat_manager.delete_chat = MagicMock(
            side_effect=Exception("Unexpected error")
        )

        # Exceptions propagate through - this is consistent with library behavior
        with self.assertRaises(Exception) as context:
            self.client.delete_chat("chat-uuid-123")

        self.assertIn("Unexpected error", str(context.exception))


if __name__ == "__main__":
    unittest.main()
