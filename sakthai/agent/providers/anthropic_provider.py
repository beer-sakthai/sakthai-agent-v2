"""Anthropic (Claude) provider backend."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import anthropic

from .base import AgentError, logger, with_retry


def call_anthropic(
    client: Any,
    model: str,
    max_tokens: int,
    system: str,
    tool_schemas: list[dict[str, Any]],
    messages: list[dict[str, Any]],
    on_token: Callable[[str], None] | None = None,
) -> Any:
    """Make one Claude Messages API call, returning the raw SDK response.

    ``on_token`` is accepted for interface parity; streaming is implemented in a
    later task.
    """
    try:
        return with_retry(
            client.messages.create,
            model=model,
            max_tokens=max_tokens,
            system=system,
            tools=tool_schemas,
            messages=messages,
        )
    except (anthropic.APIError, OSError) as exc:
        logger.error("Anthropic API call failed: %s", exc)
        raise AgentError(f"Anthropic API call failed: {exc}") from exc
