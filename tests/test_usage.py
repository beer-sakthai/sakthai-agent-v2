"""Tests for token usage tracking."""

from __future__ import annotations

from sakthai.agent.usage import UsageTracker, extract_usage


def test_usage_tracker_accumulation() -> None:
    tracker = UsageTracker()
    assert tracker.input_tokens == 0
    assert tracker.output_tokens == 0
    assert tracker.total() == 0

    tracker.record(input_tokens=10, output_tokens=5)
    assert tracker.input_tokens == 10
    assert tracker.output_tokens == 5
    assert tracker.total() == 15

    tracker.record(input_tokens=20, output_tokens=15)
    assert tracker.input_tokens == 30
    assert tracker.output_tokens == 20
    assert tracker.total() == 50

    d = tracker.to_dict()
    assert d == {
        "input_tokens": 30,
        "output_tokens": 20,
        "total_tokens": 50,
    }


class _FakeUsage:
    def __init__(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens


class _FakeAnthropicResponse:
    def __init__(self, input_tokens: int, output_tokens: int) -> None:
        self.usage = _FakeUsage(input_tokens, output_tokens)


class _FakeGeminiMetadata:
    def __init__(self, prompt: int, candidates: int) -> None:
        self.prompt_token_count = prompt
        self.candidates_token_count = candidates


class _FakeGeminiResponse:
    def __init__(self, prompt: int, candidates: int) -> None:
        self.usage_metadata = _FakeGeminiMetadata(prompt, candidates)


def test_extract_usage_anthropic() -> None:
    resp = _FakeAnthropicResponse(120, 45)
    u = extract_usage(resp)
    assert u == {"input_tokens": 120, "output_tokens": 45}


def test_extract_usage_gemini() -> None:
    resp = _FakeGeminiResponse(200, 80)
    u = extract_usage(resp)
    assert u == {"input_tokens": 200, "output_tokens": 80}


def test_extract_usage_openai_dict() -> None:
    resp = {
        "usage": {
            "prompt_tokens": 50,
            "completion_tokens": 30,
        }
    }
    u = extract_usage(resp)
    assert u == {"input_tokens": 50, "output_tokens": 30}


class _FakeOpenAIModelDump:
    def __init__(self, data: dict) -> None:
        self.data = data

    def model_dump(self) -> dict:
        return self.data


def test_extract_usage_openai_dumpable() -> None:
    resp = _FakeOpenAIModelDump(
        {
            "usage": {
                "prompt_tokens": 70,
                "completion_tokens": 40,
            }
        }
    )
    u = extract_usage(resp)
    assert u == {"input_tokens": 70, "output_tokens": 40}


def test_extract_usage_fallback() -> None:
    assert extract_usage(None) == {"input_tokens": 0, "output_tokens": 0}
    assert extract_usage("invalid") == {"input_tokens": 0, "output_tokens": 0}
