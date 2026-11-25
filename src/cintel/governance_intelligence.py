"""governance_intelligence.py - Integrated governance monitoring pipeline.

Author: Sabriya Sowers
Date: 2026-11

Purpose:
Combine signal design, anomaly detection, rolling monitoring,
and drift detection into one governance readiness assessment.

Data is synthetic and intended for educational purposes.
"""

import logging
from pathlib import Path
from typing import Final

import polars as pl

from cintel.utils_governance import (
    METRICS,
    compute_governance_drift,
    compute_governance_rolling,
    design_governance_signals,
    detect_governance_anomalies,
    load_governance_metrics,
)

# === CONFIGURATION ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_FILE: Final[Path] = ROOT_DIR / "data" / "governance_metrics_timeseries.csv"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

WINDOW_SIZE: Final[int] = 5
REFERENCE_WEEKS: Final[int] = 6
DRIFT_THRESHOLD_PP: Final[float] = 20.0

LOG = logging.getLogger(__name__)


def assess_governance(
    weekly_df: pl.DataFrame,
    drift_df: pl.DataFrame,
) -> pl.DataFrame:
    """Assign a readiness classification using the latest observations.

    READY: No current threshold violations or declining flagged drift.
    NEEDS ATTENTION: One or two current threshold violations,
        or meaningful declining drift.
    AT RISK: Three or more current threshold violations.

    These rules are illustrative, not organizational standards.
    """
    latest = weekly_df.row(-1, named=True)

    anomaly_count = sum(bool(latest[f"{metric}_anomaly"]) for metric in METRICS)

    declining_drift_count = drift_df.filter(
        pl.col("drift_flag") & (pl.col("direction") == "DECLINING")
    ).height

    if anomaly_count >= 3:
        state = "AT RISK"
    elif anomaly_count >= 1 or declining_drift_count >= 1:
        state = "NEEDS ATTENTION"
    else:
        state = "READY"

    return pl.DataFrame(
        [
            {
                "latest_week": str(latest["week"]),
                "governance_readiness_score": latest["governance_readiness_score"],
                "current_anomaly_count": anomaly_count,
                "drift_metrics_flagged": drift_df.filter(pl.col("drift_flag")).height,
                "declining_drift_count": declining_drift_count,
                "governance_state": state,
            }
        ]
    )


def main() -> None:
    """Run the integrated governance intelligence pipeline."""
    logging.basicConfig(level=logging.INFO)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Load weekly governance metrics.
    LOG.info("STEP 1: Loading governance data")
    df = load_governance_metrics(DATA_FILE)

    # Step 2: Calculate a composite governance readiness signal.
    LOG.info("STEP 2: Designing governance signals")
    df = design_governance_signals(df)

    # Step 3: Detect threshold violations.
    LOG.info("STEP 3: Detecting governance anomalies")
    df = detect_governance_anomalies(df)

    # Step 4: Calculate rolling monitoring statistics.
    LOG.info("STEP 4: Calculating rolling averages")
    df = compute_governance_rolling(df, WINDOW_SIZE)

    # Step 5: Compare reference and current periods.
    LOG.info("STEP 5: Detecting governance drift")
    drift_df = compute_governance_drift(
        df,
        reference_weeks=REFERENCE_WEEKS,
        threshold_pp=DRIFT_THRESHOLD_PP,
    )

    # Step 6: Generate an overall assessment.
    LOG.info("STEP 6: Assessing governance readiness")
    assessment_df = assess_governance(df, drift_df)

    # Step 7: Save evidence artifacts.
    weekly_output = ARTIFACTS_DIR / "governance_integrated_weekly.csv"
    drift_output = ARTIFACTS_DIR / "governance_integrated_drift.csv"
    assessment_output = ARTIFACTS_DIR / "governance_integrated_assessment.csv"

    df.write_csv(weekly_output)
    drift_df.write_csv(drift_output)
    assessment_df.write_csv(assessment_output)

    print("\n=== INTEGRATED GOVERNANCE ASSESSMENT ===")
    print(assessment_df)
    print("\n=== GOVERNANCE DRIFT RESULTS ===")
    print(drift_df)
    print("\nWeekly observations processed:", df.height)
    print("Pipeline executed successfully!")


if __name__ == "__main__":
    main()
