"""Tests for the sessions CLI commands."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest
from click.testing import CliRunner

from sakthai.cli import main
from sakthai.config import sessions_dir


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_sessions_empty(sakthai_home: Path, runner: CliRunner) -> None:
    res = runner.invoke(main, ["sessions", "list"])
    assert res.exit_code == 0
    assert "No sessions found." in res.output


def test_sessions_list_and_show(sakthai_home: Path, runner: CliRunner) -> None:
    s_dir = sessions_dir()
    s_dir.mkdir(parents=True, exist_ok=True)

    # Write a fake session
    sess_id = f"{int(time.time()) - 100}_fake-session-123"
    sess_file = s_dir / f"{sess_id}.json"
    payload = {
        "timestamp": int(time.time()) - 100,
        "task": "Explain quantum physics in simple terms",
        "model": "claude-opus-4-8",
        "usage": {
            "input_tokens": 150,
            "output_tokens": 300,
            "total_tokens": 450,
        },
        "result": {
            "text": "Quantum physics is cool.",
            "iterations": 1,
            "stop_reason": "end_turn",
            "tool_calls": [],
        },
        "messages": [
            {"role": "user", "content": "Explain quantum physics"},
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Quantum physics is cool."}],
            },
        ],
    }
    sess_file.write_text(json.dumps(payload), encoding="utf-8")

    # List
    res_list = runner.invoke(main, ["sessions", "list"])
    assert res_list.exit_code == 0
    assert sess_id in res_list.output
    assert "claude-opus-4-8" in res_list.output
    assert "450" in res_list.output
    assert "Explain quantum physics in simple terms" in res_list.output

    # Show
    res_show = runner.invoke(main, ["sessions", "show", sess_id])
    assert res_show.exit_code == 0
    assert sess_id in res_show.output
    assert "Explain quantum physics in simple terms" in res_show.output
    assert "Quantum physics is cool." in res_show.output
    assert "USER" in res_show.output
    assert "ASSISTANT" in res_show.output


def test_sessions_show_not_found(sakthai_home: Path, runner: CliRunner) -> None:
    res = runner.invoke(main, ["sessions", "show", "nonexistent"])
    assert res.exit_code != 0
    assert "Session 'nonexistent' not found." in res.output


def test_sessions_clean(sakthai_home: Path, runner: CliRunner) -> None:
    s_dir = sessions_dir()
    s_dir.mkdir(parents=True, exist_ok=True)

    now = int(time.time())
    # 1. Old session (3 days old)
    old_id = f"{now - 3 * 86400}_old-sess"
    (s_dir / f"{old_id}.json").write_text(
        json.dumps({"timestamp": now - 3 * 86400, "task": "old"}), encoding="utf-8"
    )

    # 2. New session (1 hour old)
    new_id = f"{now - 3600}_new-sess"
    (s_dir / f"{new_id}.json").write_text(
        json.dumps({"timestamp": now - 3600, "task": "new"}), encoding="utf-8"
    )

    # Test clean older than 2d (should match 1 old session)
    # Aborted path
    res_clean_abort = runner.invoke(main, ["sessions", "clean", "--older-than", "2d"], input="n\n")
    assert res_clean_abort.exit_code == 0
    assert "Found 1 session(s) older than 2d." in res_clean_abort.output
    assert "Aborted." in res_clean_abort.output
    assert (s_dir / f"{old_id}.json").exists()

    # Confirmed path
    res_clean = runner.invoke(main, ["sessions", "clean", "--older-than", "2d", "--yes"])
    assert res_clean.exit_code == 0
    assert "Successfully deleted 1 session log file(s)." in res_clean.output
    assert not (s_dir / f"{old_id}.json").exists()
    assert (s_dir / f"{new_id}.json").exists()
