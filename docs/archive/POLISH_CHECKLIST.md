# Portfolio Polish Checklist - Marketing Dashboard

## Integration Status (Completed 2026-05-12)

- [x] Fix 0: LTV denominator bug fixed (INNER JOIN → LEFT JOIN in phase5_funnel.py)
- [x] Fix A: Business questions rewritten as exec-level VP questions
- [x] Fix B: Channel × Lead Behavior cross-tab view added (kpi_channel_lead_behavior)
- [x] Fix C: Conservative estimates with caveats replacing fabricated numbers
- [x] Data traceability section in README linking every metric to its SQL source
- [x] Interview talking points updated with defensibility narrative
- [x] Database pipeline: marketing data loaded (8,000 MQLs, 842 deals)
- [x] All views created and verified: kpi_mql_volume, kpi_conversion_rate, kpi_ltv_by_channel, kpi_lead_behavior, kpi_time_to_close, kpi_channel_lead_behavior, kpi_monthly_trend
- [x] Business scenario frame added to README (Q2 2018 Marketing Review)
- [x] Time-series trend view (kpi_monthly_trend) with monthly MQL volume × conversion × close-time
- [x] README fabricated numbers replaced with real query outputs
- [x] Lead behavior analysis corrected: profiles are deal-stage data, not MQL predictors

- [x] README with marketing focus (Background, Data Structure, Executive Summary, Insights Deep Dive, Recommendations)
- [x] North Star Metrics section (Lead Conversion Rate, Marketing Qualified Leads)
- [x] Stakeholder Levers table added (lead sources, conversion funnel, campaign performance)
- [x] Funnel analysis concept added (lead → opportunity → closed deal)
- [x] Metrics prioritization framework added
- [x] CLEAN Framework in `logs/phase2_cleaning_eda.log.md`
- [x] SCAN Framework + North Star in `logs/insights.md`
- [x] DASH Framework in `docs/dash_framework.md`
- [x] SQL scripts in `sql/` (phase2-6)
- [x] Lead-to-deal conversion funnel working
- [x] Marketing qualified lead analysis by origin created

## Dashboard Design Checklist

- [ ] Consistent color palette across all pages (pick 2-3 colors max)
- [ ] All axis labels are readable (font size ≥ 11pt)
- [ ] No chart titles that restate the chart type
- [ ] KPI cards show comparison context (vs. prior period)
- [ ] Slicers are clearly labeled and visible
- [ ] No chart uses more than 6 colors at once
- [ ] Remove all gridlines except necessary reference lines
- [ ] Page navigation buttons between pages
- [ ] A text box on each page with a 1-sentence "so what"

## GitHub Repo Checklist

- [x] README.md structured as stakeholder report (5 sections, marketing focus)
- [x] `sql/` folder with all SQL scripts
- [ ] `screenshots/` folder with dashboard page images (POWER BI - BY USER)
- [ ] `.pbix` file available (POWER BI - BY USER)
- [x] Data source clearly credited (Olist via Kaggle)
- [x] Insights visible within 1 click of landing on the repo

## Portfolio Ready Checklist

- [x] SQL data pipeline automated (Python scripts)
- [x] Star schema designed and implemented
- [x] Lead conversion funnel analysis working
- [x] Marketing qualified lead by origin analysis working
- [x] KPIs defined with formulas (funnel metrics)
- [x] DAX measures documented
- [x] README tells a story (5 sections, marketing insights categorized)
- [ ] Dashboard screenshots added (POWER BI - BY USER)
- [ ] `.pbix` file available (POWER BI - BY USER)

---
**Status:** Ready for Power BI dashboard build and screenshots!