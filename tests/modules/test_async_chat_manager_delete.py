"""
Tests for AsyncChatManager delete_chat functionality (async version).
"""

import httpx
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from openwebui_chat_client.modules.async_chat_manager import AsyncChatManager


class TestAsyncChatManagerDeleteChat:
    """Test suite for AsyncChatManager.delete_chat method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_base_client = MagicMock()
        self.mock_base_client.base_url = "http://test.com"

        # Mock _make_request as async method
        self.mock_base_client._make_request = AsyncMock()

        self.manager = AsyncChatManager(self.mock_base_client)

    @pytest.mark.asyncio
    async def test_delete_chat_success(self):
        """Test successful async deletion of a specific chat."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        self.mock_base_client._make_request.return_value = mock_response

        result = await self.manager.delete_chat("chat-uuid-123")

        assert result is True
        self.mock_base_client._make_request.assert_called_once_with(
            "DELETE", "/api/v1/chats/chat-uuid-123", timeout=30
        )

    @pytest.mark.asyncio
    async def test_delete_chat_failure_status_code(self):
        """Test failed async deletion (non-200 status code)."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        self.mock_base_client._make_request.return_value = mock_response

        result = await self.manager.delete_chat("chat-uuid-123")

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_chat_exception(self):
        """Test async deletion when exception occurs."""
        self.mock_base_client._make_request.side_effect = Exception("Network error")

        result = await self.manager.delete_chat("chat-uuid-123")

        assert result is False

    @pytest.mark.asyncio
    async def test_delete_chat_empty_id(self):
        """Test async deletion with empty chat_id."""
        result = await self.manager.delete_chat("")

        assert result is False
        # Should not make any request
        self.mock_base_client._make_request.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_chat_none_id(self):
        """Test async deletion with None chat_id."""
        result = await self.manager.delete_chat(None)

        assert result is False
        # Should not make any request
        self.mock_base_client._make_request.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_chat_no_response(self):
        """Test async deletion when no response is returned."""
        self.mock_base_client._make_request.return_value = None

        result = await self.manager.delete_chat("chat-uuid-123")

        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
