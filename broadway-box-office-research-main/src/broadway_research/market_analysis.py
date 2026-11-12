"""Exploratory market-level time-series specifications.

The paper's complete design matrices are unavailable, so these models are
explicitly independent extensions. All samples are formed before Patsy builds
the design matrix. This prevents all-zero dummy columns for years that have no
complete macro observations.
"""

from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf

HAC_LAGS = 8


def _fit(data: pd.DataFrame, formula: str, required: list[str]):
    sample = data.dropna(subset=required).sort_values("week_ending").copy()
    return smf.ols(formula, sample).fit(
        cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS}
    )


def _specifications() -> dict[str, dict[str, object]]:
    return {
        "A": {
            "formula": "log_market_gross ~ holiday_week + C(month) + C(year)",
            "required": ["log_market_gross", "holiday_week", "month", "year"],
            "note": "Paper-aligned calendar extension; HAC(8).",
        },
        "B": {
            "formula": (
                "log_market_gross ~ holiday_week + C(month) + C(year) + "
                "unemployment_rate_pct + consumer_sentiment_monthly"
            ),
            "required": [
                "log_market_gross", "holiday_week", "month", "year",
                "unemployment_rate_pct", "consumer_sentiment_monthly",
            ],
            "note": "Complete-case macro extension; unused year levels removed; HAC(8).",
        },
        "C": {
            "formula": (
                "log_market_gross ~ holiday_week + C(month) + time_years + "
                "post_reopening + "
                "unemployment_rate_pct + consumer_sentiment_monthly + "
                "nyc_visitors_millions_annual"
            ),
            "required": [
                "log_market_gross", "holiday_week", "month", "time_years",
                "post_reopening",
                "unemployment_rate_pct", "consumer_sentiment_monthly",
                "nyc_visitors_millions_annual",
            ],
            "note": (
                "Rank-repaired tourism extension: a linear time trend replaces year fixed "
                "effects because annual tourism is collinear with year dummies; a coarse "
                "post-reopening indicator addresses the major structural break; HAC(8)."
            ),
        },
        "D": {
            "formula": (
                "log_market_gross ~ holiday_week + C(month) + C(year) + "
                "unemployment_rate_pct + consumer_sentiment_halfyear"
            ),
            "required": [
                "log_market_gross", "holiday_week", "month", "year",
                "unemployment_rate_pct", "consumer_sentiment_halfyear",
            ],
            "note": (
                "Complete-case semiannual sentiment extension; unused year levels "
                "removed; HAC(8)."
            ),
        },
    }


def models(market: pd.DataFrame):
    """Return transparent HAC extensions keyed A--D.

    A, B, and D retain the paper-aligned calendar structure. C replaces year
    fixed effects with a linear time trend because an annual tourism series is
    exactly collinear with year indicators. C therefore remains an independent
    extension and must not be described as an exact reproduction.
    """
    data = market.copy()
    data["time_years"] = (
        data["week_ending"] - data["week_ending"].min()
    ).dt.days / 365.25
    data["post_reopening"] = (
        data["week_ending"] >= pd.Timestamp("2021-09-14")
    ).astype(int)
    specs = _specifications()
    return {
        key: (spec["formula"], _fit(data, spec["formula"], spec["required"]))
        for key, spec in specs.items()
    }


def model_notes() -> dict[str, str]:
    return {key: str(spec["note"]) for key, spec in _specifications().items()}
