# Case Study — Health Intelligence Platform

## Problem
Behavioral and wellbeing datasets often get presented as static charts that don’t help decisions. The goal was a single interactive dashboard that answers practical questions fast:

- Which digital behavior signals correlate most with wellbeing outcomes (stress/anxiety/focus/productivity)?
- How do patterns differ by demographic/segment slices?
- Which users look “high risk” (or “low wellbeing”) under a transparent scoring rule?
- Can we explore tradeoffs and thresholds without writing new code each time?

## Approach
- Streamlit UI for fast exploration with a clean, decision-first layout.
- Plotly for interactive insights (filters, hover, zoom, segment comparison).
- Feature views that connect behavior → outcomes (screen time, sleep, activity, social, work patterns).
- Organized as a reproducible project with pinned dependencies and production-friendly structure.

## Key Decisions
- **Decision-ready KPIs:** small set of stable KPIs (sleep, activity, screen time, stress/anxiety proxies) to anchor every view.
- **Slice-first workflow:** filters drive every metric (segment comparison is a first-class citizen).
- **Transparent scoring:** simple risk/wellbeing score built from normalized inputs (easy to explain and adjust).
- **Guardrails:** required-column checks + graceful handling of missing values instead of crashing.
- **Export-friendly:** keep all derived fields in a single enriched table for easy downstream use.

## Results
A decision-friendly platform that supports:
- KPI overview + distribution views
- Correlation and segment comparison (who differs and why)
- Risk / wellbeing scoring with threshold exploration
- Insights tab with “what moves the needle” signals
- Data explorer for debugging and exporting filtered slices

## Next Steps
- Add a lightweight validation panel (missingness/outliers/duplicates) and a data-quality score.
- Add model baseline (LogReg / RF) with calibration + monitoring metrics.
- Add exports to `artifacts/` (filtered snapshots + charts + score tables).
- Add privacy-minded notes and schema contract for safer reuse.
