"""governance_app.py - Interactive governance intelligence dashboard.

Author: Sabriya Sowers
Date: 2026-11

Integrates signal design, anomaly detection, rolling monitoring,
drift detection, and an overall governance readiness assessment.

Uses synthetic healthcare metadata for educational purposes.

Run locally:
    uv run marimo run src/cintel/governance_app.py
"""

import marimo

__generated_with = "0.25.2"

app = marimo.App(width="full")


# === IMPORTS AND REUSABLE FUNCTIONS ===


@app.cell
async def _():
    from pathlib import Path
    import sys

    if sys.platform == "emscripten":
        import micropip

        await micropip.install("polars")

    import marimo as mo
    import polars as pl

    if sys.platform == "emscripten":
        # Browser: Marimo exports custom modules individually.
        from governance_intelligence import assess_governance  # ty: ignore[import-not-found]
        from utils_governance import (  # ty: ignore[import-not-found]
            compute_governance_drift,
            compute_governance_rolling,
            design_governance_signals,
            detect_governance_anomalies,
            load_governance_metrics,
        )
    else:
        # Local: Use the installed cintel package.
        from cintel.governance_intelligence import assess_governance
        from cintel.utils_governance import (
            compute_governance_drift,
            compute_governance_rolling,
            design_governance_signals,
            detect_governance_anomalies,
            load_governance_metrics,
        )

    metric_labels = {
        "Metadata completeness": "metadata_completeness_pct",
        "Ownership coverage": "ownership_pct",
        "Stewardship coverage": "stewardship_pct",
        "Documentation gaps": "documentation_gaps_pct",
    }

    return (
        Path,
        assess_governance,
        compute_governance_drift,
        compute_governance_rolling,
        design_governance_signals,
        detect_governance_anomalies,
        load_governance_metrics,
        metric_labels,
        mo,
        pl,
        sys,
    )


# === DASHBOARD INTRODUCTION ===


@app.cell
def _(mo):
    mo.md(
        """
        # Metadata Completeness & Governance Readiness Monitor

        ### Integrated Continuous Intelligence | Project 06

        Explore synthetic healthcare metadata using signal design,
        anomaly detection, rolling monitoring, and drift detection.

        **Purpose:** Understand governance readiness, identify
        unusual measurements, and distinguish improvements from
        potentially concerning changes.

        *All data and monitoring thresholds are illustrative.*
        """
    )


# === LOAD AND PREPARE GOVERNANCE DATA ===


@app.cell
def _(
    Path,
    design_governance_signals,
    detect_governance_anomalies,
    load_governance_metrics,
    mo,
    sys,
):
    filename = "governance_metrics_timeseries.csv"

    if sys.platform == "emscripten":
        from pyodide.http import open_url  # ty: ignore[import-not-found]

        notebook_location = mo.notebook_location()

        if notebook_location is None:
            raise RuntimeError("Unable to locate the notebook.")

        data_url = notebook_location / "public" / filename
        base_df = load_governance_metrics(open_url(str(data_url)))
    else:
        data_path = Path.cwd() / "data" / filename
        base_df = load_governance_metrics(data_path)

    base_df = design_governance_signals(base_df)
    base_df = detect_governance_anomalies(base_df)

    return (base_df,)


# === INTERACTIVE CONTROLS ===


@app.cell
def _(metric_labels, mo):
    metric_choice = mo.ui.dropdown(
        options=list(metric_labels.keys()),
        value="Metadata completeness",
        label="Governance metric",
    )

    rolling_window = mo.ui.slider(
        start=2,
        stop=8,
        value=5,
        step=1,
        label="Rolling window (weeks)",
    )

    drift_threshold = mo.ui.slider(
        start=5,
        stop=40,
        value=20,
        step=5,
        label="Drift threshold (percentage points)",
    )

    mo.vstack(
        [
            mo.md("## Explore Monitoring Settings"),
            mo.hstack(
                [metric_choice, rolling_window, drift_threshold],
                gap=2,
                justify="start",
            ),
        ]
    )

    return drift_threshold, metric_choice, rolling_window


# === CALCULATE INTERACTIVE RESULTS ===


@app.cell
def _(
    assess_governance,
    base_df,
    compute_governance_drift,
    compute_governance_rolling,
    drift_threshold,
    rolling_window,
):
    weekly_df = compute_governance_rolling(
        base_df,
        window_size=rolling_window.value,
    )

    drift_df = compute_governance_drift(
        weekly_df,
        reference_weeks=6,
        threshold_pp=float(drift_threshold.value),
    )

    assessment_df = assess_governance(weekly_df, drift_df)

    return assessment_df, drift_df, weekly_df


# === OVERALL GOVERNANCE ASSESSMENT ===


@app.cell
def _(assessment_df, mo):
    assessment = assessment_df.row(0, named=True)

    state = assessment["governance_state"]
    score = assessment["governance_readiness_score"]
    anomaly_count = assessment["current_anomaly_count"]
    drift_count = assessment["drift_metrics_flagged"]
    declining_count = assessment["declining_drift_count"]
    latest_week = assessment["latest_week"]

    mo.md(
        f"""
        ## Overall Governance Assessment

        ### **{state}**

        | Measurement | Result |
        |---|---:|
        | Latest observation | {latest_week} |
        | Governance readiness score | {score:.2f} / 100 |
        | Current threshold violations | {anomaly_count} |
        | Metrics flagged for drift | {drift_count} of 4 |
        | Meaningful declining drift | {declining_count} |

        **Interpretation:** The assessment considers current
        threshold violations and meaningful declining drift.
        A drift flag alone does not indicate poor performance.
        """
    )


# === INTERACTIVE TREND CHART ===


@app.cell
def _(metric_choice, metric_labels, mo, rolling_window, weekly_df):
    selected_metric = metric_labels[metric_choice.value]
    selected_label = metric_choice.value
    rolling_column = f"{selected_metric}_rolling_mean"

    weeks = weekly_df["week"].cast(str).to_list()
    actual_values = weekly_df[selected_metric].to_list()
    rolling_values = weekly_df[rolling_column].to_list()

    # Draw an SVG chart without requiring additional plotting packages.
    chart_width = 800
    chart_height = 350
    left_margin = 65
    top_margin = 25
    plot_width = 690
    plot_height = 260

    def x_position(index: int) -> float:
        return left_margin + (index / max(len(weeks) - 1, 1)) * plot_width

    def y_position(value: float) -> float:
        return top_margin + plot_height * (1 - value / 100)

    actual_points = " ".join(
        f"{x_position(i):.1f},{y_position(v):.1f}" for i, v in enumerate(actual_values)
    )

    rolling_pairs = [
        (i, value) for i, value in enumerate(rolling_values) if value is not None
    ]

    rolling_points = " ".join(
        f"{x_position(i):.1f},{y_position(v):.1f}" for i, v in rolling_pairs
    )

    grid_lines = "".join(
        (
            f'<line x1="65" y1="{y_position(v):.1f}" '
            f'x2="755" y2="{y_position(v):.1f}" '
            'stroke="#dbe2e9" stroke-dasharray="4 4"/>'
            f'<text x="53" y="{y_position(v) + 4:.1f}" '
            f'text-anchor="end" font-size="12" fill="#64748b">{v}%</text>'
        )
        for v in range(0, 101, 20)
    )

    x_labels = "".join(
        (
            f'<text x="{x_position(i):.1f}" y="310" '
            'text-anchor="middle" font-size="10" fill="#64748b">'
            f"{week[5:]}</text>"
        )
        for i, week in enumerate(weeks)
    )

    data_points = "".join(
        (
            f'<circle cx="{x_position(i):.1f}" '
            f'cy="{y_position(v):.1f}" r="4" '
            'fill="#2563eb">'
            f"<title>{weeks[i]}: {v:.2f}%</title></circle>"
        )
        for i, v in enumerate(actual_values)
    )

    svg_chart = f"""
    <div style="max-width:1000px;overflow-x:auto">
      <svg viewBox="0 0 {chart_width} {chart_height}"
           xmlns="http://www.w3.org/2000/svg"
           role="img"
           aria-label="Weekly governance metric and rolling average">
        <rect width="800" height="350" fill="white"/>
        {grid_lines}
        <polyline points="{actual_points}" fill="none"
                  stroke="#2563eb" stroke-width="3"
                  stroke-linejoin="round"/>
        <polyline points="{rolling_points}" fill="none"
                  stroke="#ea580c" stroke-width="3"
                  stroke-linejoin="round"/>
        {data_points}
        {x_labels}
        <line x1="65" y1="285" x2="755" y2="285"
              stroke="#64748b"/>
        <line x1="65" y1="25" x2="65" y2="285"
              stroke="#64748b"/>
        <line x1="160" y1="335" x2="190" y2="335"
              stroke="#2563eb" stroke-width="3"/>
        <text x="198" y="339" font-size="13"
              fill="#334155">Weekly value</text>
        <line x1="400" y1="335" x2="430" y2="335"
              stroke="#ea580c" stroke-width="3"/>
        <text x="438" y="339" font-size="13"
              fill="#334155">Rolling average</text>
      </svg>
    </div>
    """

    mo.vstack(
        [
            mo.md(
                f"## {selected_label}: Weekly Trend\n\n"
                f"Comparing weekly measurements with the "
                f"**{rolling_window.value}-week rolling average**."
            ),
            mo.Html(svg_chart),
        ]
    )


# === DRIFT RESULTS ===


@app.cell
def _(drift_df, drift_threshold, mo):
    mo.vstack(
        [
            mo.md(
                "## Historical vs. Current Drift\n\n"
                "The first six weeks are compared with the last six. "
                f"Changes greater than **{drift_threshold.value} "
                "percentage points** are flagged."
            ),
            mo.ui.table(drift_df),
            mo.md(
                "**Important:** Improving metrics may trigger drift "
                "flags. Drift indicates change, not necessarily risk."
            ),
        ]
    )


# === WEEKLY EVIDENCE ===


@app.cell
def _(mo, weekly_df):
    mo.vstack(
        [
            mo.md("## Weekly Governance Monitoring Data"),
            mo.ui.table(weekly_df),
        ]
    )


# === LIMITATIONS AND CLOSING ===


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ### Notes

        - Four governance metrics contribute equally to the readiness score.
        - Readiness thresholds are illustrative, not approved standards.
        - Rolling averages smooth short-term fluctuations.
        - Drift compares six historical and six current observations.
        - The overall state uses current anomalies and declining drift.

        **Data limitations:** All observations are synthetic.
        Results do not represent the performance of a real health system.

        **Source:** Continuous Intelligence Project 06 —
        Metadata Completeness & Governance Readiness Monitor.
        """
    )


if __name__ == "__main__":
    app.run()
