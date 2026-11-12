"""Integration tests that rerun the real analysis when authorized inputs exist."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pytest

from broadway_research.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parents[1]


def _authorized_input_dir() -> Path:
    configured = os.environ.get("BROADWAY_PRIVATE_INPUT_DIR")
    if configured:
        candidate = Path(configured)
    else:
        candidate = ROOT.parents[1] / "work" / "private_inputs"
    if not candidate.exists() or not list(candidate.glob("*.xlsx")):
        pytest.skip(
            "Authorized workbook unavailable; set BROADWAY_PRIVATE_INPUT_DIR to run integration tests"
        )
    return candidate


def test_pipeline_reruns_scientific_analysis_and_preserves_site(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    sentinel = docs / "index.html"
    sentinel.write_text("curated-site-must-survive", encoding="utf-8")

    run = run_pipeline(_authorized_input_dir(), tmp_path)

    assert sentinel.read_text(encoding="utf-8") == "curated-site-must-survive"
    assert run["validation"]["status"] == "passed"
    assert run["validation"]["market_models_full_rank"] is True
    assert run["comparison"]["passed"].all()
    assert run["robustness"]["n"].tolist() == [67, 66, 63, 51]
    assert run["market_extensions"]["full_rank"].all()

    regenerated = pd.read_csv(tmp_path / "results" / "paper_vs_python.csv")
    assert regenerated["passed"].all()
    assert (tmp_path / "results" / "dashboard_data.json").is_file()
    assert (tmp_path / "results" / "market_monthly_summary.csv").is_file()
    assert (tmp_path / "figures" / "coefficients.png").stat().st_size > 1000


def test_pipeline_aggregate_outputs_do_not_disclose_singleton_values(tmp_path):
    run_pipeline(_authorized_input_dir(), tmp_path)
    styles = pd.read_csv(tmp_path / "results" / "production_style_summary.csv")
    assert styles.loc[styles["n"] < 3, "mean_gross_usd"].isna().all()
    assert styles.loc[styles["n"] < 3, "mean_seats"].isna().all()
