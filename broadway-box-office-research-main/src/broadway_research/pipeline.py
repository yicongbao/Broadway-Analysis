"""Deterministic end-to-end research pipeline.

The pipeline reads an authorized private workbook and writes generated research
artifacts to ``results/`` and ``figures/``. It deliberately does not write to
``docs/`` or ``research/`` so a scientific rerun cannot overwrite the curated
portfolio website or authored narrative.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .diagnostics import inspect
from .ingest import load
from .market_analysis import model_notes, models
from .production_analysis import fit, formula, samples

PRODUCTION_BENCHMARKS = {
    "r_squared": 0.6079569056109908,
    "capacity": 1.0073848481499095,
    "capacity_p": 3.582017220037733e-5,
    "adapted": 0.2867209169,
}
PAPER_MARKET_N = {"A": 501, "B": 257, "C": 236, "D": 257}
PAPER_MARKET_R2 = {"A": 0.507, "B": 0.699, "C": 0.671, "D": 0.696}


def _json_default(value):
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, (pd.Timestamp, pd.Period)):
        return str(value)
    raise TypeError(f"Cannot serialize {type(value)!r}")


def _records(frame: pd.DataFrame) -> list[dict[str, object]]:
    """Return strict-JSON records, translating missing values to null."""
    clean = frame.astype(object).where(pd.notna(frame), None)
    return clean.to_dict("records")


def _save_figure(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()


def _public_aggregates(production: pd.DataFrame, market: pd.DataFrame, results: Path):
    """Write aggregates that are safe for a public dashboard.

    Means are suppressed for music-style cells with fewer than three
    productions so singleton categories do not disclose an underlying row.
    """
    groups = []
    for variable in ("Adapted", "Revival"):
        for value, sample in production.groupby(variable, observed=True):
            se = float(sample["Avg_Gross_USD"].sem())
            groups.append(
                {
                    "variable": variable,
                    "value": int(value),
                    "n": int(len(sample)),
                    "mean_gross_usd": float(sample["Avg_Gross_USD"].mean()),
                    "median_gross_usd": float(sample["Avg_Gross_USD"].median()),
                    "se_gross_usd": se,
                    "ci95_lower_usd": float(sample["Avg_Gross_USD"].mean() - 1.96 * se),
                    "ci95_upper_usd": float(sample["Avg_Gross_USD"].mean() + 1.96 * se),
                }
            )
    group_summary = pd.DataFrame(groups)
    group_summary.to_csv(results / "production_group_summary.csv", index=False)

    style_rows = []
    for style, sample in production.groupby("Music_Style", observed=True):
        n = int(len(sample))
        style_rows.append(
            {
                "music_style": style,
                "n": n,
                "mean_gross_usd": (
                    float(sample["Avg_Gross_USD"].mean()) if n >= 3 else np.nan
                ),
                "mean_seats": float(np.exp(sample["log_seats"]).mean()) if n >= 3 else np.nan,
                "suppressed": n < 3,
            }
        )
    style_summary = pd.DataFrame(style_rows).sort_values("n", ascending=False)
    style_summary.to_csv(results / "production_style_summary.csv", index=False)

    plot_columns = [column for column in production if column.startswith("Plot_")]
    plot_summary = pd.DataFrame(
        {
            "plot_category": [column.removeprefix("Plot_") for column in plot_columns],
            "n": [int(production[column].sum()) for column in plot_columns],
            "share": [float(production[column].mean()) for column in plot_columns],
        }
    ).sort_values("n", ascending=False)
    plot_summary.to_csv(results / "plot_category_summary.csv", index=False)

    annual = (
        market.groupby("year", observed=True)
        .agg(
            observed_weeks=("week_ending", "size"),
            total_gross_usd=("market_gross_usd", "sum"),
            mean_weekly_gross_usd=("market_gross_usd", "mean"),
            median_weekly_gross_usd=("market_gross_usd", "median"),
            mean_weekly_attendance=("market_attendance", "mean"),
            mean_gross_per_attendee_usd=("gross_per_attendee_usd", "mean"),
            mean_capacity_pct=("capacity_pct", "mean"),
            unemployment_observed=("unemployment_rate_pct", "count"),
            holiday_weeks=("holiday_week", "sum"),
        )
        .reset_index()
    )
    annual["unemployment_missing"] = (
        annual["observed_weeks"] - annual["unemployment_observed"]
    )
    annual.to_csv(results / "market_annual_summary.csv", index=False)

    season = (
        market.groupby("season", observed=True)
        .agg(
            observed_weeks=("week_ending", "size"),
            total_gross_usd=("market_gross_usd", "sum"),
            mean_weekly_gross_usd=("market_gross_usd", "mean"),
            mean_weekly_attendance=("market_attendance", "mean"),
            mean_capacity_pct=("capacity_pct", "mean"),
            mean_gross_per_attendee_usd=("gross_per_attendee_usd", "mean"),
        )
        .reset_index()
        .sort_values("season")
    )
    season.to_csv(results / "market_season_summary.csv", index=False)

    quarterly_source = market.assign(
        quarter=market["week_ending"].dt.to_period("Q").astype(str)
    )
    quarter = (
        quarterly_source.groupby("quarter", observed=True)
        .agg(
            observed_weeks=("week_ending", "size"),
            mean_weekly_gross_usd=("market_gross_usd", "mean"),
            mean_weekly_attendance=("market_attendance", "mean"),
            mean_gross_per_attendee_usd=("gross_per_attendee_usd", "mean"),
        )
        .reset_index()
        .sort_values("quarter")
    )
    quarter.to_csv(results / "market_quarter_summary.csv", index=False)

    monthly = (
        market.groupby("month", observed=True)
        .agg(
            observed_weeks=("week_ending", "size"),
            mean_weekly_gross_usd=("market_gross_usd", "mean"),
            mean_weekly_attendance=("market_attendance", "mean"),
        )
        .reset_index()
        .sort_values("month")
    )
    monthly.to_csv(results / "market_monthly_summary.csv", index=False)

    holiday = (
        market.assign(holiday_group=np.where(market["holiday_week"].eq(1), "Holiday", "Other"))
        .groupby("holiday_group", observed=True)
        .agg(
            observed_weeks=("week_ending", "size"),
            mean_weekly_gross_usd=("market_gross_usd", "mean"),
            median_weekly_gross_usd=("market_gross_usd", "median"),
            mean_weekly_attendance=("market_attendance", "mean"),
        )
        .reset_index()
    )
    holiday.to_csv(results / "market_holiday_summary.csv", index=False)
    return group_summary, style_summary, plot_summary, annual, season, quarter, monthly, holiday


def run_pipeline(input_dir: str | Path, output_dir: str | Path = ".") -> dict[str, object]:
    output = Path(output_dir)
    results = output / "results"
    figures = output / "figures"
    results.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    production, market = load(input_dir)
    if production.shape != (67, 19):
        raise ValueError(f"Expected production shape (67, 19), got {production.shape}")
    if market.shape != (501, 21):
        raise ValueError(f"Expected market shape (501, 21), got {market.shape}")
    if int(market["unemployment_rate_pct"].isna().sum()) != 244:
        raise ValueError("Expected 244 missing market unemployment observations")

    production_fit = fit(production)
    computed = {
        "r_squared": production_fit.rsquared,
        "capacity": production_fit.params["log_seats"],
        "capacity_p": production_fit.pvalues["log_seats"],
        "adapted": production_fit.params["Adapted"],
    }
    comparison = pd.DataFrame(
        [
            {
                "metric": metric,
                "benchmark": benchmark,
                "computed": computed[metric],
                "difference": computed[metric] - benchmark,
                "passed": abs(computed[metric] - benchmark) < 1e-6,
            }
            for metric, benchmark in PRODUCTION_BENCHMARKS.items()
        ]
    )
    if not bool(comparison["passed"].all()):
        raise AssertionError("Production benchmark validation failed")
    comparison.to_csv(results / "paper_vs_python.csv", index=False)

    confidence = production_fit.conf_int()
    coefficients = pd.DataFrame(
        {
            "term": production_fit.params.index,
            "estimate": production_fit.params.values,
            "se_hc3": production_fit.bse.values,
            "p_hc3": production_fit.pvalues.values,
            "ci95_lower": confidence.iloc[:, 0].values,
            "ci95_upper": confidence.iloc[:, 1].values,
        }
    )
    coefficients.to_csv(results / "production_coefficients.csv", index=False)

    robustness_rows = []
    for name, sample in samples(production).items():
        sensitivity_fit = fit(sample)
        capacity_ci = sensitivity_fit.conf_int().loc["log_seats"]
        robustness_rows.append(
            {
                "sample": name,
                "n": int(sensitivity_fit.nobs),
                "r_squared": sensitivity_fit.rsquared,
                "adjusted_r_squared": sensitivity_fit.rsquared_adj,
                "capacity": sensitivity_fit.params["log_seats"],
                "ci95_lower": capacity_ci.iloc[0],
                "ci95_upper": capacity_ci.iloc[1],
                "p_hc3": sensitivity_fit.pvalues["log_seats"],
                "formula": formula(production),
            }
        )
    robustness = pd.DataFrame(robustness_rows)
    robustness.to_csv(results / "robustness_results.csv", index=False)

    missingness = (
        market.assign(missing=market["unemployment_rate_pct"].isna())
        .groupby("year", observed=True)["missing"]
        .agg(["sum", "count"])
    )
    missingness["rate"] = missingness["sum"] / missingness["count"]
    missingness.to_csv(results / "missingness_by_year.csv")

    qa = {
        "production_shape": list(production.shape),
        "market_shape": list(market.shape),
        "production_duplicates": int(production.duplicated().sum()),
        "market_duplicate_dates": int(market["week_ending"].duplicated().sum()),
        "log_gross_max_error": float(
            abs(np.log(production["Avg_Gross_USD"]) - production["log_gross"]).max()
        ),
        "seat_range": np.exp(production["log_seats"]).agg(["min", "max"]).to_dict(),
        "nonpositive_gross": int((market["market_gross_usd"] <= 0).sum()),
        "date_min": str(market["week_ending"].min().date()),
        "date_max": str(market["week_ending"].max().date()),
        "style_counts": production["Music_Style"].value_counts().to_dict(),
        "production_diagnostics": inspect(production_fit),
        "unemployment_missing": 244,
    }
    (results / "qa.json").write_text(
        json.dumps(qa, indent=2, default=_json_default), encoding="utf-8"
    )

    data_dictionary = pd.concat(
        [
            pd.DataFrame(
                {
                    "level": level,
                    "variable": data.columns,
                    "dtype": data.dtypes.astype(str).values,
                    "missing": data.isna().sum().values,
                }
            )
            for level, data in (("production", production), ("market", market))
        ],
        ignore_index=True,
    )
    data_dictionary.to_csv(results / "data_dictionary.csv", index=False)

    influence = production_fit.get_influence()
    pd.DataFrame(
        {
            "observation": np.arange(len(production)),
            "leverage": influence.hat_matrix_diag,
            "cooks_distance": influence.cooks_distance[0],
            "residual": production_fit.resid,
        }
    ).to_csv(results / "influence.csv", index=False)

    market_rows = []
    notes = model_notes()
    for key, (market_formula, market_fit) in models(market).items():
        diagnostics = inspect(market_fit)
        market_rows.append(
            {
                "model": key,
                "status": "Exploratory extension; not exact reproduction",
                "n": int(market_fit.nobs),
                "r_squared": market_fit.rsquared,
                "adjusted_r_squared": market_fit.rsquared_adj,
                "paper_n": PAPER_MARKET_N[key],
                "paper_r_squared": PAPER_MARKET_R2[key],
                "formula": market_formula,
                "identification_note": notes[key],
                **diagnostics,
                "full_rank": diagnostics["rank"] == diagnostics["columns"],
            }
        )
        market_ci = market_fit.conf_int()
        pd.DataFrame(
            {
                "term": market_fit.params.index,
                "estimate": market_fit.params.values,
                "se_hac8": market_fit.bse.values,
                "p_hac8": market_fit.pvalues.values,
                "ci95_lower": market_ci.iloc[:, 0].values,
                "ci95_upper": market_ci.iloc[:, 1].values,
            }
        ).to_csv(results / f"market_{key}_coefficients.csv", index=False)
    market_extensions = pd.DataFrame(market_rows)
    market_extensions.to_csv(results / "market_extensions.csv", index=False)
    if not bool(market_extensions["full_rank"].all()):
        raise AssertionError("A market extension remains rank deficient")

    aggregate_tables = _public_aggregates(production, market, results)
    (
        group_summary,
        style_summary,
        plot_summary,
        annual,
        season,
        quarter,
        monthly,
        holiday,
    ) = aggregate_tables

    dashboard = {
        "metrics": {
            "productions": int(len(production)),
            "market_weeks": int(len(market)),
            "production_r_squared": float(production_fit.rsquared),
            "capacity_elasticity": float(production_fit.params["log_seats"]),
            "capacity_p_hc3": float(production_fit.pvalues["log_seats"]),
            "unemployment_missing": 244,
        },
        "production_key_coefficients": _records(
            coefficients[
                coefficients["term"].isin(["log_seats", "Adapted", "Revival"])
            ]
        ),
        "robustness": _records(robustness.drop(columns=["formula"])),
        "market_models": _records(market_extensions.drop(columns=["formula"])),
        "production_groups": _records(group_summary),
        "production_styles": _records(style_summary),
        "plot_categories": _records(plot_summary),
        "market_annual": _records(annual),
        "market_season": _records(season),
        "market_quarter": _records(quarter),
        "market_monthly": _records(monthly),
        "market_holiday": _records(holiday),
        "unemployment_missingness": _records(missingness.reset_index()),
    }
    (results / "dashboard_data.json").write_text(
        json.dumps(dashboard, indent=2, default=_json_default, allow_nan=False),
        encoding="utf-8",
    )

    plt.scatter(np.exp(production["log_seats"]), production["Avg_Gross_USD"] / 1e6)
    plt.xlabel("Theatre seats (back-transformed)")
    plt.ylabel("Average weekly gross (million USD)")
    _save_figure(figures / "capacity.png")

    plt.hist(production["Avg_Gross_USD"] / 1e6, bins=15)
    plt.xlabel("Average weekly gross (million USD), N=67")
    plt.ylabel("Productions")
    _save_figure(figures / "gross_distribution.png")

    plt.bar(missingness.index.astype(str), missingness["sum"])
    plt.ylabel("Weeks missing unemployment")
    plt.xlabel("Year")
    plt.xticks(rotation=45)
    _save_figure(figures / "missingness.png")

    plt.scatter(production_fit.fittedvalues, production_fit.resid)
    plt.axhline(0, color="black", linewidth=1)
    plt.xlabel("Fitted log gross")
    plt.ylabel("Residual")
    _save_figure(figures / "residuals.png")

    plt.figure(figsize=(9, 9))
    plt.errorbar(
        coefficients["estimate"],
        range(len(coefficients)),
        xerr=[
            coefficients["estimate"] - coefficients["ci95_lower"],
            coefficients["ci95_upper"] - coefficients["estimate"],
        ],
        fmt="o",
    )
    plt.yticks(range(len(coefficients)), coefficients["term"])
    plt.axvline(0, color="gray", linewidth=1)
    plt.xlabel("OLS coefficient and HC3 95% interval")
    _save_figure(figures / "coefficients.png")

    plt.plot(season["season"], season["mean_weekly_gross_usd"] / 1e6, marker="o")
    plt.xlabel("Broadway season")
    plt.ylabel("Mean observed weekly market gross (million USD)")
    plt.xticks(rotation=45)
    _save_figure(figures / "market.png")

    plt.bar(
        range(len(group_summary)),
        group_summary["mean_gross_usd"] / 1e6,
        yerr=1.96 * group_summary["se_gross_usd"] / 1e6,
    )
    plt.xticks(
        range(len(group_summary)),
        [
            f"{row.variable}={row.value} n={row.n}"
            for row in group_summary.itertuples()
        ],
        rotation=15,
    )
    plt.ylabel("Mean gross (million USD); normal 95% intervals")
    _save_figure(figures / "groups.png")

    validation = {
        "status": "passed",
        "production_benchmarks_passed": bool(comparison["passed"].all()),
        "market_models_full_rank": bool(market_extensions["full_rank"].all()),
        "source_shapes": {"production": [67, 19], "market": [501, 21]},
        "generated_public_aggregate_tables": 8,
        "docs_preserved": True,
    }
    (results / "validation_summary.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )
    return {
        "production": production,
        "market": market,
        "production_fit": production_fit,
        "comparison": comparison,
        "robustness": robustness,
        "market_extensions": market_extensions,
        "validation": validation,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()
    run = run_pipeline(args.input_dir, args.output_dir)
    print(json.dumps(run["validation"], indent=2))


if __name__ == "__main__":
    main()
