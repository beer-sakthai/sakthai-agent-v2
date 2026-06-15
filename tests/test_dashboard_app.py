"""Smoke tests for the Streamlit dashboard app (sakthai/dashboard/app.py).

The module is pure Streamlit/plotly presentation glue; the data logic it renders
lives in dashboard/data.py (covered by test_dashboard_data.py) and app.py is
excluded from coverage/mypy in pyproject.toml. These tests run only where the
``dashboard`` extra is installed — they skip under CI's dev-only install — and
verify the module imports cleanly and its figure builders construct without a
live Streamlit runtime (``st`` side effects are stubbed).
"""

from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("streamlit")
pytest.importorskip("plotly")
pytest.importorskip("pandas")

from sakthai.dashboard import app  # noqa: E402  (guarded import after importorskip)


def test_main_is_callable() -> None:
    assert callable(app.main)


def test_growth_chart_builds(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: captured.setdefault("fig", fig))
    app._growth_chart({"labels": ["w1", "w2"], "facts": [1, 3], "observations": [0, 2]})
    assert len(captured["fig"].data) == 2  # facts + observations traces


def test_category_chart_skips_when_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[Any] = []
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: calls.append(fig))
    app._category_chart([])
    assert calls == []  # nothing rendered for empty categories


def test_category_chart_builds(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: captured.setdefault("fig", fig))
    app._category_chart([{"count": 3, "name": "memory", "color": "#abcdef"}])
    assert captured["fig"].data  # a bar trace was added


def test_kpi_row_builds(monkeypatch: pytest.MonkeyPatch) -> None:
    metrics: list[tuple[str, Any]] = []

    class _Col:
        def metric(self, label: str, value: Any, delta: str | None = None) -> None:
            metrics.append((label, value))

    monkeypatch.setattr(app.st, "columns", lambda n: (_Col(), _Col()))
    app._kpi_row(
        {
            "total_facts": 5,
            "total_facts_delta": 1,
            "total_observations": 2,
            "total_observations_delta": 0,
        }
    )
    assert ("Facts", 5) in metrics
    assert ("Observations", 2) in metrics


def test_session_timeline_chart_skips_when_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[Any] = []
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: calls.append(fig))
    app._session_timeline_chart({"labels": [], "sessions": [], "tokens": []})
    assert calls == []


def test_session_timeline_chart_builds(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: captured.setdefault("fig", fig))
    app._session_timeline_chart({"labels": ["d1", "d2"], "sessions": [1, 2], "tokens": [10, 20]})
    assert captured["fig"].data


def test_token_usage_chart_skips_when_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[Any] = []
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: calls.append(fig))
    app._token_usage_chart([])
    assert calls == []


def test_token_usage_chart_builds(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}
    monkeypatch.setattr(app.st, "plotly_chart", lambda fig, **k: captured.setdefault("fig", fig))
    app._token_usage_chart([{"model": "m", "sessions": 1, "total_tokens": 42}])
    assert captured["fig"].data


def test_session_kpi_row_builds(monkeypatch: pytest.MonkeyPatch) -> None:
    metrics: list[tuple[str, Any]] = []

    class _Col:
        def metric(self, label: str, value: Any, delta: str | None = None) -> None:
            metrics.append((label, value))

    monkeypatch.setattr(app.st, "columns", lambda n: (_Col(), _Col(), _Col()))
    app._session_kpi_row({"sessions": 3, "total_tokens": 100, "output_tokens": 40})
    assert ("Sessions", 3) in metrics
    assert ("Total tokens", 100) in metrics
