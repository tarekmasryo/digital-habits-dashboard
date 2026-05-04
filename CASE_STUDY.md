# Case Study — Health Intelligence Platform

## Problem
Behavioral and wellbeing datasets often get presented as static charts that don’t help decisions. The goal was a single interactive dashboard that answers practical questions fast:

- Which digital behavior signals correlate most with wellbeing outcomes (stress/anxiety/focus/productivity)?
- How do patterns differ by demographic/segment slices?
- Which cohorts should be prioritized for review under a transparent scoring policy?
- Can we explore tradeoffs and thresholds without writing new code each time?

## Approach
- Streamlit UI for fast exploration with a clean, decision-first layout.
- Plotly for interactive insights (filters, hover, zoom, segment comparison).
- Feature views that connect behavior → outcomes (screen time, sleep, activity, social, work patterns).
- Organized as a reproducible project with a production-friendly package structure and clear runtime dependencies.

## Key Decisions
- **Decision-ready KPIs:** small set of stable KPIs (sleep, activity, screen time, stress/anxiety proxies) to anchor every view.
- **Slice-first workflow:** filters drive every metric (segment comparison is a first-class citizen).
- **Transparent scoring:** scoring-policy output built from simulated behavioral and wellbeing inputs, designed to be explainable and adjustable.
- **Guardrails:** deterministic synthetic generation, filtered-state handling, and tested scoring/metrics functions.
- **Export-friendly:** keep all derived fields in a single enriched table for easy downstream use.

## Results
A decision-friendly platform that supports:
- KPI overview + distribution views
- Correlation and segment comparison (who differs and why)
- Wellbeing risk scoring with threshold exploration
- Policy insights with “what moves the needle” signals
- Data explorer for debugging and exporting filtered slices

## Next Steps
- Add a lightweight validation panel (missingness/outliers/duplicates) and a data-quality score.
- Add an optional model baseline (LogReg / RF) with calibration + monitoring metrics if a real labeled dataset is introduced.
- Add exports to `artifacts/` (filtered snapshots + charts + score tables).
- Add privacy-minded notes and schema contracts before adapting the workflow to real user data.
