from pathlib import Path
import json
import re

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_benchmarks():
    data = pd.read_csv(ROOT / "results/paper_vs_python.csv")
    assert data.passed.all()
    assert (abs(data.difference) < 1e-6).all()


def test_samples():
    data = pd.read_csv(ROOT / "results/robustness_results.csv")
    assert data.n.tolist() == [67, 66, 63, 51]
    assert data.formula.nunique() == 1
    assert np.allclose(
        data.r_squared, [.6079569056, .56809708, .5311222293, .6920474004], atol=1e-6
    )


def test_missingness():
    data = pd.read_csv(ROOT / "results/missingness_by_year.csv")
    assert data["sum"].sum() == 244
    assert data["count"].sum() == 501
    assert dict(zip(data.year, data["sum"])) == {
        2015: 31, 2016: 52, 2017: 53, 2018: 52, 2019: 52, 2020: 0,
        2021: 0, 2022: 0, 2023: 0, 2024: 0, 2025: 4, 2026: 0,
    }


def test_integrity():
    qa = json.loads((ROOT / "results/qa.json").read_text())
    assert qa["production_shape"] == [67, 19]
    assert qa["market_shape"] == [501, 21]
    assert qa["market_duplicate_dates"] == 0
    assert qa["nonpositive_gross"] == 0
    assert qa["log_gross_max_error"] < 1e-6


def test_artifacts():
    for name in ["capacity", "gross_distribution", "missingness", "residuals", "coefficients", "market", "groups"]:
        assert (ROOT / f"figures/{name}.png").stat().st_size > 1000
    for name in ["index", "production", "market"]:
        assert (ROOT / f"docs/{name}.html").is_file()


def test_public_aggregate_artifacts():
    expected = [
        "production_group_summary.csv",
        "production_style_summary.csv",
        "plot_category_summary.csv",
        "market_annual_summary.csv",
        "market_season_summary.csv",
        "market_quarter_summary.csv",
        "market_monthly_summary.csv",
        "market_holiday_summary.csv",
        "dashboard_data.json",
        "validation_summary.json",
    ]
    for name in expected:
        assert (ROOT / "results" / name).is_file(), name
    styles = pd.read_csv(ROOT / "results/production_style_summary.csv")
    assert styles.loc[styles.n < 3, "mean_gross_usd"].isna().all()
    market_models = pd.read_csv(ROOT / "results/market_extensions.csv")
    assert market_models.full_rank.all()
    dashboard_text = (ROOT / "results/dashboard_data.json").read_text(encoding="utf-8")
    assert "NaN" not in dashboard_text
    assert json.loads(dashboard_text)["metrics"]["productions"] == 67


def test_market_extensions_are_full_rank_and_repair_is_explicit():
    models = pd.read_csv(ROOT / "results/market_extensions.csv").set_index("model")
    assert models.full_rank.all()
    assert (models["rank"] == models["columns"]).all()
    assert np.isclose(models.loc["C", "r_squared"], 0.707510882083089)
    assert models.loc["C", "rank"] == 18
    assert "time_years" in models.loc["C", "formula"]
    assert "post_reopening" in models.loc["C", "formula"]


def test_notebooks_are_executed_computational_artifacts():
    expected_code_cells = {
        "01_data_and_provenance.ipynb": 5,
        "02_exploratory_analysis.ipynb": 6,
        "03_production_regression.ipynb": 5,
        "04_diagnostics_and_robustness.ipynb": 6,
        "05_market_analysis.ipynb": 6,
    }
    combined_source = []
    for name, expected_count in expected_code_cells.items():
        notebook = json.loads((ROOT / "notebooks" / name).read_text(encoding="utf-8"))
        code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
        assert len(code_cells) == expected_count
        assert all(cell.get("execution_count") is not None for cell in code_cells)
        assert not any(
            output.get("output_type") == "error"
            for cell in code_cells
            for output in cell.get("outputs", [])
        )
        combined_source.extend("".join(cell["source"]) for cell in code_cells)
    source = "\n".join(combined_source)
    for required in [
        "BROADWAY_INPUT_DIR",
        "load(input_dir)",
        "fit(production)",
        "cov_type=\"HAC\"",
        "get_influence()",
    ]:
        assert required in source


def test_dashboard_assets_and_values_match_research_outputs():
    index = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    script = (ROOT / "docs/assets/app.js").read_text(encoding="utf-8")
    assert (ROOT / "docs/assets/styles.css").stat().st_size > 1000
    assert (ROOT / "docs/assets/plotly.min.js").stat().st_size > 1_000_000
    for chart_id in [
        "coefficient-chart",
        "robustness-chart",
        "market-chart",
        "seasonality-chart",
        "missingness-chart",
        "market-model-chart",
    ]:
        assert f'id="{chart_id}"' in index
        assert f"'{chart_id}'" in script
    assert ".707511" in script
    assert ".698932" not in script


def test_research_traceability_is_complete_and_links_resolve():
    traceability_names = [
        "project_structure_map.md",
        "paper_to_code_traceability.md",
    ]
    documents = [ROOT / "README.md"] + [ROOT / "docs" / name for name in traceability_names]
    combined = []
    for document in documents:
        assert document.is_file(), document
        text = document.read_text(encoding="utf-8")
        combined.append(text)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split(" ", 1)[0]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_text = target.split("#", 1)[0]
            if path_text:
                assert (document.parent / path_text).resolve().exists(), (
                    document,
                    target,
                )

    content = "\n".join(combined)
    for required in [
        "1.007385",
        "244 of 501",
        "BROADWAY_INPUT_DIR",
        "Exact reproduction",
        "Methodological repair",
        "Exploratory extension",
        "```mermaid",
    ]:
        assert required in content
    assert len(re.findall(r"```mermaid", content)) >= 2
    assert not re.search(
        r"\b(homework|class|lesson|teacher|assignment|training)\b",
        content,
        flags=re.IGNORECASE,
    )
