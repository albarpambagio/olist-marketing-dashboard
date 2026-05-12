# Dashboard Guide - Marketing Funnel

This document outlines the dashboard structure for the **Olist Marketing Funnel**, focused on channel performance, lead conversion, and lifetime value (LTV).

---

## Dashboard Pages

### Page1: Marketing Funnel Overview

**KPI Cards (top row):**
- MQL Volume (8,000 total)
- Conversion Rate (10.5% overall)
- Deals Won (842)
- Avg Time-to-Close (24–44 days)

**Visuals:**
- MQL volume trend (monthly, with conversion % annotation)
- MQL volume by channel (bar chart)
- Deals won by month (line chart)
- Slicer: Year, Channel, Lead Behavior

**Business narrative:** "Should the VP of Marketing reallocate budget from low-converting channels to high-LTV channels?"

---

### Page2: Channel Performance

**Visuals:**
- Conversion rate by origin (horizontal bar, sorted desc)
- LTV by channel (bar chart — $17–$96/MQL range)
- Conversion rate vs. LTV scatter (bubble size = MQL volume)
- Channel volume mix (donut chart)

**Business narrative:** "Should the Head of Acquisition shift budget from Organic to Paid Search based on conversion and LTV data?"

---

### Page3: Lead Quality

**Visuals:**
- Lead behavior profiles (Cat/Eagle/Wolf/Shark) — distribution within closed deals (bar chart) — note: profiles are deal-stage only, not MQL predictors
- Time-to-close by lead behavior (box plot or bar chart)
- Lead behavior distribution (donut)
- Conversion rate trend by behavior (line chart over time)
- Channel × Lead Behavior Cross-Tab (heatmap matrix — rows = channel, columns = behavior, fill = profile distribution %)

**Business narrative:** "Which channels produce which seller profiles — and does Social's Wolf-heavy mix (17.3%) explain its conversion gap?"

---

### Page4: LTV Analysis

**Visuals:**
- Revenue by marketing channel (stacked bar or line chart)
- LTV per MQL by channel (bar chart, sorted desc)
- Cohort retention of sellers (heat table — month index vs. acquisition month)
- Seller revenue by channel (scatter: revenue vs. time-since-acquisition)

**Business narrative:** "Which channels deliver the highest LTV/MQL after correcting the denominator bug — and does the gap justify budget shifts?"

---

## DASH Framework Applied

### D — Decision

| Page | Decision Enabled | Owner |
|------|------------------|-------|
| Funnel Overview | Should the VP of Marketing reallocate budget across channels? | VP Marketing |
| Channel Performance | Should the Head of Acquisition shift spend from Organic to Paid Search? | Head of Acquisition |
| Lead Quality | Should the Head of Sales Ops change SDR prioritization rules? | Head of Sales Ops |
| LTV Analysis | Should VP Marketing + VP Finance adjust channel investment based on true LTV/MQL? | VP Marketing & Finance |

---

### A — Audience

| Audience | Needs | Implication |
|----------|-------|--------------|
| Marketing Leadership | Channel ROI, budget allocation | KPI callouts, conversion rates, LTV |
| Acquisition Managers | Channel performance, lead quality | Channel breakdowns, lead behavior |
| Sales Ops | Deal closing time, lead-to-seller conversion | Funnel visualization, time-to-close |

---

### S — Signal

| Metric | Why It's Included |
|--------|-------------------|
| **MQL Volume** (8,000) | Top-of-funnel health indicator |
| **Conversion Rate** (10.5% overall) | Primary marketing KPI (corrected from fabricated 18.75%) |
| **LTV by Channel** ($17–$96/MQL) | ROI driver for budget decisions (LEFT JOIN fix applied) |
| **Time-to-Close** (24–44 days) | Sales cycle efficiency (compressing, not lengthening) |

**Excluded from executive page:**
- Seller-specific metrics (belongs on LTV page only)
- Lead behavior details (belongs on Lead Quality page)

---

### H — Hierarchy

```
┌─────────────────────────────────────────────────┐
│  PAGE TITLE (One-sentence "so what?")          │
├─────────────────────────────────────────────────┤
│  [KPI Card1] [KPI Card2] [KPI Card3] [KPI Card4] │ ← Top: Key numbers
├─────────────────────────────────────────────────┤
│  [Trend Line Chart]    [Bar Chart]       │ ← Middle: Visual trends
├─────────────────────────────────────────────────┤
│  [Scatter Plot]    [Cohort Heat Table]        │ ← Bottom: Deep dive
├─────────────────────────────────────────────────┤
│  Slicers: [Year] [Channel] [Lead Behavior]      │ ← Filters (always visible)
└─────────────────────────────────────────────────┘
```

---

## Key SQL Views for Marketing Dashboard

| View | Purpose | Source File |
|------|---------|-------------|
| `kpi_mql_volume` | MQL count by month + channel | `phase5_funnel.py:36` |
| `kpi_conversion_rate` | Conversion % by channel | `phase5_funnel.py:52` |
| `kpi_ltv_by_channel` | LTV per MQL, per seller (LEFT JOIN fix applied) | `phase5_funnel.py:71` |
| `kpi_lead_behavior` | Conversion by Cat/Eagle/Wolf/Shark | `phase5_funnel.py:90` |
| `kpi_time_to_close` | Avg days by month | `phase5_funnel.py:121` |
| `kpi_channel_lead_behavior` | Channel × Lead Behavior cross-tab | `phase5_funnel.py:137` |

---

## Color Palette

- **Primary:** `#1f77b4` (blue) — Paid Search, positive metrics
- **Secondary:** `#ff7f0e` (orange) — Organic Search, warnings
- **Neutral:** `#2ca02c` (green) — Direct traffic, positive conversion
- **Text:** `#333333` (dark gray) — all labels and titles

---

## Dashboard Design Checklist

- [ ] Consistent color palette across all pages (pick 2-3 colors max)
- [ ] All axis labels readable (font size ≥ 11pt)
- [ ] No chart titles that restate the chart type
- [ ] KPI cards show comparison context (vs. prior period)
- [ ] Slicers clearly labeled and visible on all pages
- [ ] No chart uses more than 6 colors at once
- [ ] Remove all gridlines except necessary reference lines
- [ ] Page navigation buttons between pages
- [ ] A text box on each page with a 1-sentence "so what"

---

*Dashboard framework based on DASH methodology for marketing funnel dashboards.*
