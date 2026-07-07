"""Tests for benchmark JSON to Markdown rendering."""

import json
import subprocess
import sys
from pathlib import Path

from scripts.render_report import render_markdown

PROJECT_ROOT = Path(__file__).parent.parent


def sample_payload():
    """Return a compact runner-like payload for report tests."""
    return {
        "environment": {
            "timestamp_utc": "2026-07-07T12:00:00+00:00",
            "python_implementation": "CPython",
            "python_version": "3.11.0",
            "platform": "test-platform",
            "machine": "arm64",
            "cpu_count": 8,
            "git_sha": "abc1234",
            "quick": True,
            "runs": 2,
            "warmups": 1,
        },
        "summary": {
            "total": 2,
            "passed": 1,
            "failed": 1,
            "skipped": 0,
            "cases_total": 3,
            "cases_passed": 1,
            "cases_failed": 1,
            "cases_skipped": 1,
        },
        "benchmarks": [
            {
                "module": "example_perf_test",
                "category": "basic",
                "status": "passed",
                "cases": [
                    {
                        "name": "perf_test1_fast",
                        "status": "passed",
                        "seconds_median": 0.001,
                    },
                    {
                        "name": "perf_test2_optional",
                        "status": "skipped",
                        "seconds_median": None,
                        "reason": "optional dependency not installed: example",
                    },
                ],
                "errors": [],
            },
            {
                "module": "broken_perf_test",
                "category": "expert",
                "status": "failed",
                "cases": [
                    {
                        "name": "perf_test1_broken",
                        "status": "failed",
                        "seconds_median": None,
                        "error": "RuntimeError: broken",
                    },
                ],
                "errors": [{"message": "RuntimeError: broken"}],
            },
        ],
    }


def test_report_renderer_produces_markdown():
    """Test renderer includes environment, summary, and benchmark sections."""
    markdown = render_markdown(sample_payload())

    assert "# Python Practical Benchmarks Report" in markdown
    assert "| Python | CPython 3.11.0 |" in markdown
    assert "| Benchmarks total | 2 |" in markdown
    assert "`example_perf_test`" in markdown


def test_report_renderer_includes_skips_and_failures():
    """Test renderer makes skipped and failed cases explicit."""
    markdown = render_markdown(sample_payload())

    assert "## Explicit Skips" in markdown
    assert "optional dependency not installed: example" in markdown
    assert "## Failed Cases" in markdown
    assert "RuntimeError: broken" in markdown


def test_report_renderer_cli_writes_output(tmp_path):
    """Test report renderer CLI writes Markdown to disk."""
    input_path = tmp_path / "payload.json"
    output_path = tmp_path / "report.md"
    input_path.write_text(json.dumps(sample_payload()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/render_report.py",
            str(input_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    assert result.returncode == 0
    assert output_path.exists()
    assert "Python Practical Benchmarks Report" in output_path.read_text(encoding="utf-8")
