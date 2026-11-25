# cintel-06-continuous-intelligence-sowers

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/ssowers2/cintel-06-continuous-intelligence-sowers/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/ssowers2/cintel-06-continuous-intelligence-sowers/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://ssowers2.github.io/cintel-06-continuous-intelligence-sowers/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Integrate anomaly detection, signal design, rolling monitoring, and drift detection to assess system performance and healthcare data governance readiness.

## Project Overview

**Author:** Sabriya Sowers

**Date:** November 2026

This project brings together techniques introduced throughout the Continuous Intelligence course, including signal design, anomaly detection, rolling monitoring, and drift detection.

The original example uses operational system measurements to identify unusual behavior and classify the overall system state as STABLE or DEGRADED.

### Custom Governance Application

This customization extends the Metadata Completeness & Governance Readiness Monitor developed in previous projects. The integrated Python pipeline is implemented and verified; the interactive dashboard is the next development stage.

The goal is to integrate multiple monitoring techniques into one continuous intelligence application using synthetic healthcare metadata.

The application will evaluate metrics such as:

- Metadata completeness
- Ownership coverage
- Stewardship coverage
- Documentation gaps

The integrated monitoring system will help identify unusual changes, evaluate trends, and generate an overall governance readiness assessment.

The project is configured in [pyproject.toml](pyproject.toml).

## Data

The example uses system metrics from `data/`.

Each observation includes:

- `requests` - number of requests handled.
- `errors` - number of failed requests.
- `total_latency_ms` - total response time in milliseconds.

The example uses stored observations to demonstrate
an integrated monitoring assessment.

## Approach

The pipeline uses Polars to:

1. Read system measurements.
2. Calculate error rate and average latency.
3. Identify signals exceeding defined thresholds.
4. Summarize system behavior.
5. Assign a system assessment based on the monitored signals.

Explore these project components:

- [pyproject.toml](pyproject.toml) - project configuration and dependencies.
- [src/cintel/continuous_intelligence.py](src/cintel/continuous_intelligence.py) - integrated monitoring pipeline.
- [data/](data/) - system measurements.
- [artifacts/](artifacts/) - generated system assessment.
- [tests/](tests/) - automated tests.
- [.github/workflows/](.github/workflows/) - automated checks and documentation deployment.
- [docs/](docs/) - project documentation.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
to set up your machine and project environment.

From a VS Code terminal in the project root:

```shell
uv run python -m cintel.continuous_intelligence
```

## Run the Reactive App

From a VS Code terminal in the project root
(hit CTRL + c to quit):

```shell
uv run marimo run  src/cintel/app.py
```

## Results

The pipeline summarizes the monitored signals
and writes `artifacts/system_assessment.csv`.
Review the resulting system assessment and explain
which signals support the reported state.

The original example uses a 40 ms latency threshold and classifies the overall system state as STABLE. The modified experiment uses a 30 ms threshold and produces a DEGRADED classification.

- **STABLE** - summary signals remain within the defined thresholds.
- **DEGRADED** - one or more summary signals exceed the defined thresholds.

Successful execution produces a terminal message:

```shell
========================
Pipeline executed successfully!
========================
```

A `project.log` file is created in the project root.

This confirms that the Python pipeline executes
and the logging system works.

## Technical Experiment: Adjusting the Latency Threshold

A controlled experiment was conducted to evaluate how changing a monitoring threshold affects the overall system assessment.

### Modification

Changed `MAX_AVG_LATENCY` in `src/cintel/continuous_intelligence.py` from 40.0 to 30.0 milliseconds. The underlying system measurements remained unchanged.

### Prediction

The system classification was expected to change from STABLE to DEGRADED because the average latency of 33.71 milliseconds exceeds the modified threshold of 30 milliseconds.

### Results

The pipeline executed successfully and confirmed the predicted change.

| Measurement | Original | Modified |
|---|---|---|
| Latency threshold | 40 ms | 30 ms |
| Average latency | 33.71 ms | 33.71 ms |
| System state | STABLE | DEGRADED |

Automated testing completed successfully with one passing test and 44.17% code coverage.

### Interpretation

The experiment demonstrates how monitoring thresholds influence system classifications without changing the underlying data. Selecting appropriate thresholds is important for producing meaningful assessments and avoiding unnecessary alerts.

The full experiment, including the methodology and interpretation, is documented on the [Project 06 Documentation Site](https://ssowers2.github.io/cintel-06-continuous-intelligence-sowers/).

[View Modified System Assessment](artifacts/system_assessment.csv)

## Integrated Governance Monitoring

The custom application applies continuous intelligence techniques to 12 weeks of synthetic healthcare metadata measurements.

### Techniques Applied

- **Signal design:** Calculates a composite governance readiness score using four equally weighted metrics.
- **Anomaly detection:** Identifies measurements that fall outside illustrative governance thresholds.
- **Rolling monitoring:** Calculates five-week rolling averages to identify trends.
- **Drift detection:** Compares six historical weeks with six current weeks using a 20-percentage-point threshold.
- **System assessment:** Combines current anomalies and declining drift to classify governance readiness.

The four governance metrics are metadata completeness, ownership coverage, stewardship coverage, and documentation gaps.

### Run the Governance Pipeline

From the project root in VS Code:

```powershell
uv run python -m cintel.governance_intelligence
```

The pipeline generates three CSV artifacts:

- `artifacts/governance_integrated_weekly.csv`
- `artifacts/governance_integrated_drift.csv`
- `artifacts/governance_integrated_assessment.csv`

### Verified Results

| Measurement | Result |
|---|---|
| Weekly observations | 12 |
| Latest observation | November 9, 2026 |
| Governance readiness score | 73.34 |
| Current threshold violations | 0 |
| Metrics flagged for drift | 3 of 4 |
| Declining drift | 0 |
| Overall governance state | READY |

Three governance metrics exceeded the drift threshold, but all four metrics improved between the reference and current periods.

The overall classification is READY because the latest measurements have no threshold violations and no meaningful declining drift.

These classifications and thresholds are illustrative and are not established healthcare governance standards.

### Automated Testing

Run:

```powershell
uv run pytest -v
```

Verification completed successfully with **7 passing tests and 53.21% overall code coverage**.

See the [Project Documentation](https://ssowers2.github.io/cintel-06-continuous-intelligence-sowers/) for the detailed analysis and interpretation.

## Verification

Run the automated tests:

```shell
uv run pytest
```

## Project Documentation

The [hosted documentation site](https://ssowers2.github.io/cintel-06-continuous-intelligence-sowers/)
is published using Zensical and GitHub Pages.

The documentation site is used to present the project report,
covering such sections as data, methods, results, visualizations,
interpretation, and conclusions.

## CI/CD and GitHub Actions

This project includes continuous integration and continuous deployment (CI/CD)
to check project files and publish the docs.
GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/ssowers2/cintel-06-continuous-intelligence-sowers/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/ssowers2/cintel-06-continuous-intelligence-sowers/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the
[Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
for **detailed instructions and troubleshooting**.

### Initialize and Update the Python Environment

With the project open in VS Code, open a VS Code terminal.
Paste each command and hit Enter or Return after to run it.

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

Set up and run the git hooks to perform
basic checks automatically before
any changes get pushed to GitHub.

In the VS Code terminal,
paste each command and hit Enter or Return after to run it.

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files
# repeat if changes were made
uvx prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and
build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git add-commit-push to GitHub

After making useful changes, save your work to GitHub.

```shell
git add -A
git commit -m "describe your changes in quotes"
git push -u origin main
```

## Developer Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Developer Tools

This project uses professional Python tools to support development,
testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) - Python environments and dependencies.
- [Ruff](https://docs.astral.sh/ruff/) - Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) - Python type checking.
- [pytest](https://docs.pytest.org/) - automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) - Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) - project documentation, configured in [zensical.toml](zensical.toml).

## Links

- [GitHub Repository](https://github.com/ssowers2/cintel-06-continuous-intelligence-sowers)
- [Hosted Documentation](https://ssowers2.github.io/cintel-06-continuous-intelligence-sowers/)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
