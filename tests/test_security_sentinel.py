from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from sakthai.agent.tools import _send_telegram_message
from sakthai.memory.store import MemoryStore


def test_telegram_token_leak_in_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that an invalid TELEGRAM_BOT_TOKEN is not leaked in the error message."""
    sensitive_token = "INVALID TOKEN WITH SECRET 12345"
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", sensitive_token)
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "67890")

    store = MagicMock(spec=MemoryStore)
    result = _send_telegram_message({"message": "hello"}, store)

    assert "Error: Invalid TELEGRAM_BOT_TOKEN format" in result
    assert sensitive_token not in result
    assert "SECRET" not in result
    assert "12345" not in result


if __name__ == "__main__":
    test_telegram_token_leak_in_error()
    print("Security test passed.")
