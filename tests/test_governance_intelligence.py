"""Automated tests for the integrated governance intelligence project.

Author: Sabriya Sowers
Date: 2026-11

Tests use synthetic governance data and verify:
- Data loading
- Signal design
- Anomaly detection
- Rolling monitoring
- Drift detection
- Overall governance assessment
"""

from pathlib import Path

import polars as pl

from cintel.governance_intelligence import assess_governance
from cintel.utils_governance import (
    compute_governance_drift,
    compute_governance_rolling,
    design_governance_signals,
    detect_governance_anomalies,
    load_governance_metrics,
)

DATA_FILE = Path("data/governance_metrics_timeseries.csv")


def test_load_governance_metrics() -> None:
    """Verify that all 12 weekly observations are loaded."""
    df = load_governance_metrics(DATA_FILE)

    assert df.height == 12
    assert "metadata_completeness_pct" in df.columns
    assert "ownership_pct" in df.columns
    assert "stewardship_pct" in df.columns
    assert "documentation_gaps_pct" in df.columns


def test_governance_readiness_score() -> None:
    """Verify that the composite readiness score is calculated."""
    df = load_governance_metrics(DATA_FILE)
    df = design_governance_signals(df)

    assert "governance_readiness_score" in df.columns
    assert df["governance_readiness_score"].null_count() == 0
    assert abs(df["governance_readiness_score"][-1] - 73.34) < 0.01


def test_governance_anomaly_detection() -> None:
    """Verify that low ownership coverage triggers an anomaly."""
    df = pl.DataFrame(
        {
            "metadata_completeness_pct": [85.0],
            "ownership_pct": [60.0],
            "stewardship_pct": [80.0],
            "documentation_gaps_pct": [20.0],
        }
    )

    result = detect_governance_anomalies(df)

    assert result["ownership_pct_anomaly"][0] == True
    assert result["metadata_completeness_pct_anomaly"][0] == False
    assert result["stewardship_pct_anomaly"][0] == False
    assert result["documentation_gaps_pct_anomaly"][0] == False


def test_governance_rolling_average() -> None:
    """Verify that five-week rolling averages are calculated."""
    df = load_governance_metrics(DATA_FILE)
    result = compute_governance_rolling(df, window_size=5)

    column = "metadata_completeness_pct_rolling_mean"

    assert column in result.columns
    assert result[column].null_count() == 4
    assert result[column][-1] is not None


def test_governance_drift_detection() -> None:
    """Verify drift flags and favorable change directions."""
    df = load_governance_metrics(DATA_FILE)

    result = compute_governance_drift(
        df,
        reference_weeks=6,
        threshold_pp=20.0,
    )

    assert result.height == 4
    assert result.filter(pl.col("drift_flag")).height == 3
    assert result.filter(pl.col("direction") == "IMPROVING").height == 4


def test_governance_ready_assessment() -> None:
    """Verify that improving metrics produce a READY assessment."""
    df = load_governance_metrics(DATA_FILE)
    df = design_governance_signals(df)
    df = detect_governance_anomalies(df)

    drift = compute_governance_drift(df)

    result = assess_governance(df, drift)

    assert result["governance_state"][0] == "READY"
    assert result["current_anomaly_count"][0] == 0
    assert result["drift_metrics_flagged"][0] == 3
    assert result["declining_drift_count"][0] == 0
