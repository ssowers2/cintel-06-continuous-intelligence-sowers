"""utils_governance.py - Shared governance monitoring functions.

Author: Sabriya Sowers
Date: 2026-11

Purpose:
Provide reusable functions for an integrated continuous intelligence
application focused on synthetic healthcare metadata governance.

Techniques:
- Signal design
- Anomaly detection
- Rolling monitoring
- Drift detection

All percentage-based metrics use a 0-100 scale.
"""

from pathlib import Path
from typing import IO, cast

import polars as pl

# === GOVERNANCE METRICS ===

METRICS = [
    "metadata_completeness_pct",
    "ownership_pct",
    "stewardship_pct",
    "documentation_gaps_pct",
]

# Illustrative readiness thresholds.
# These are educational settings, not organizational standards.

THRESHOLDS = {
    "metadata_completeness_pct": 60.0,
    "ownership_pct": 75.0,
    "stewardship_pct": 70.0,
    "documentation_gaps_pct": 35.0,
}

# Higher is better except for documentation gaps.

HIGHER_IS_BETTER = {
    "metadata_completeness_pct": True,
    "ownership_pct": True,
    "stewardship_pct": True,
    "documentation_gaps_pct": False,
}


# === LOAD WEEKLY GOVERNANCE DATA ===


def load_governance_metrics(data_file: Path | IO[str]) -> pl.DataFrame:
    """Load and sort weekly governance measurements."""
    return pl.read_csv(data_file, try_parse_dates=True).sort("week")


# === SIGNAL DESIGN ===


def design_governance_signals(df: pl.DataFrame) -> pl.DataFrame:
    """Add an overall governance readiness score.

    Invert documentation gaps so that all four components
    have the same direction: higher values mean better readiness.
    Each metric receives equal weight.
    """
    return df.with_columns(
        (
            (
                pl.col("metadata_completeness_pct")
                + pl.col("ownership_pct")
                + pl.col("stewardship_pct")
                + (100 - pl.col("documentation_gaps_pct"))
            )
            / 4
        )
        .round(2)
        .alias("governance_readiness_score")
    )


# === ANOMALY DETECTION ===


def detect_governance_anomalies(df: pl.DataFrame) -> pl.DataFrame:
    """Flag weekly measurements outside readiness thresholds."""
    expressions = []

    for metric in METRICS:
        threshold = THRESHOLDS[metric]

        if HIGHER_IS_BETTER[metric]:
            condition = pl.col(metric) < threshold
        else:
            condition = pl.col(metric) > threshold

        expressions.append(condition.alias(f"{metric}_anomaly"))

    return df.with_columns(expressions)


# === ROLLING MONITORING ===


def compute_governance_rolling(
    df: pl.DataFrame,
    window_size: int = 5,
) -> pl.DataFrame:
    """Calculate rolling averages for governance measurements."""
    if window_size < 1:
        raise ValueError("Window size must be at least 1.")

    return df.sort("week").with_columns(
        [
            pl.col(metric)
            .rolling_mean(window_size=window_size)
            .round(2)
            .alias(f"{metric}_rolling_mean")
            for metric in METRICS
        ]
    )


# === DRIFT DETECTION ===


def compute_governance_drift(
    df: pl.DataFrame,
    reference_weeks: int = 6,
    threshold_pp: float = 20.0,
) -> pl.DataFrame:
    """Compare reference and current periods.

    Drift indicates a meaningful change, not necessarily
    a negative outcome.
    """
    df = df.sort("week")

    if reference_weeks < 1 or reference_weeks >= df.height:
        raise ValueError("Reference period must leave current observations.")

    if threshold_pp < 0:
        raise ValueError("Drift threshold cannot be negative.")

    reference = df.head(reference_weeks)
    current = df.slice(reference_weeks)

    results = []

    for metric in METRICS:
        reference_mean_value = reference[metric].mean()
        current_mean_value = current[metric].mean()

        if reference_mean_value is None or current_mean_value is None:
            raise ValueError(f"Missing values prevent comparison: {metric}")

        reference_mean = cast(float, reference_mean_value)
        current_mean = cast(float, current_mean_value)
        difference = current_mean - reference_mean

        if difference == 0:
            direction = "UNCHANGED"
        elif (difference > 0 and HIGHER_IS_BETTER[metric]) or (
            difference < 0 and not HIGHER_IS_BETTER[metric]
        ):
            direction = "IMPROVING"
        else:
            direction = "DECLINING"

        results.append(
            {
                "metric": metric,
                "reference_mean_pct": round(reference_mean, 2),
                "current_mean_pct": round(current_mean, 2),
                "difference_pp": round(difference, 2),
                "threshold_pp": threshold_pp,
                "drift_flag": abs(difference) > threshold_pp,
                "direction": direction,
            }
        )

    return pl.DataFrame(results)
