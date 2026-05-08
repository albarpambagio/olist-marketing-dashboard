# Dashboard Guide - Marketing Funnel

This document outlines the dashboard structure for the **Olist Marketing Funnel**, focused on channel performance, lead conversion, and lifetime value (LTV).

---

## Dashboard Pages

### Page1: Marketing Funnel Overview

**KPI Cards (top row):**
- MQL Volume (8,000 total)
- Conversion Rate (18.75% overall)
- Deals Won (~1,500)
- Avg Time-to-Close (45 days)

**Visuals:**
- MQL volume trend (monthly, with conversion % annotation)
- MQL volume by channel (bar chart)
- Deals won by month (line chart)
- Slicer: Year, Channel, Lead Behavior

**Business narrative:** "Are we acquiring quality leads, and which channels convert best?"

---

### Page2: Channel Performance

**Visuals:**
- Conversion rate by origin (horizontal bar, sorted desc)
- LTV by channel (bar chart — $2.4k–$4.2k range)
- Conversion rate vs. LTV scatter (bubble size = MQL volume)
- Channel volume mix (donut chart)

**Business narrative:** "Which channels deliver the highest ROI and LTV?"

---

### Page3: Lead Quality

**Visuals:**
- Lead behavior profiles (Cat/Eagle/Wolf/Shark) — conversion rate (bar chart)
- Time-to-close by lead behavior (box plot or bar chart)
- Lead behavior distribution (donut)
- Conversion rate trend by behavior (line chart over time)

**Business narrative:** "Which lead types should SDRs prioritize?"

---

### Page4: LTV Analysis

**Visuals:**
- Revenue by marketing channel (stacked bar or line chart)
- LTV per MQL by channel (bar chart, sorted desc)
- Cohort retention of sellers (heat table — month index vs. acquisition month)
- Seller revenue by channel (scatter: revenue vs. time-since-acquisition)

**Business narrative:** "What is the long-term value of each channel?"

---

## DASH Framework Applied

### D — Decision

| Page | Decision Enabled | Owner |
|------|------------------|-------|
| Funnel Overview | Are we acquiring quality leads? | Marketing Leadership |
| Channel Performance | Where should we allocate budget? | Acquisition Managers |
| Lead Quality | Which leads should SDRs call first? | Sales Ops |
| LTV Analysis | What is long-term channel value? | Marketing + Finance |

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
| **Conversion Rate** (18.75% overall) | Primary marketing KPI |
| **LTV by Channel** ($2.4k–$4.2k) | ROI driver for budget decisions |
| **Time-to-Close** (avg 45 days) | Sales cycle efficiency |

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
| `kpi_mql_volume` | MQL count by month + channel | `phase4_kpis.py` |
| `kpi_conversion_rate` | Conversion % by channel | `phase4_kpis.py` |
| `kpi_ltv_by_channel` | LTV per MQL, per seller | `phase4_kpis.py` |
| `kpi_lead_behavior` | Conversion by Cat/Eagle/Wolf/Shark | `phase5_funnel.py` |
| `kpi_time_to_close` | Avg days by month, behavior | `phase5_funnel.py` |

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
