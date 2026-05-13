# Olist Marketing Funnel: Key Insights Log

> **Data Audit Note (2026-05-12):** The `kpi_ltv_by_channel` view previously used `INNER JOIN` which excluded non-converting MQLs from the denominator, inflating LTV/MQL. Fixed to `LEFT JOIN`. See `sql/phase5_funnel.py:67` for the fix.
>
> **Traceability:** Every metric below is traceable to its SQL view. See README [Data Traceability](#) section for the full mapping.

## Data Overview

### Marketing Funnel Summary
- **MQLs**: 8,000 (Jun 2017–Jun 2018)
- **Closed Deals**: 842 (10.53% conversion)
- **Top Channel (Volume)**: Organic Search (2,296, 28.7%)
- **Top Channel (Conversion)**: Paid Search (12.30%)
- **LTV/MQL Leader**: Paid Search ($95.61)
- **Data Issue**: 1,159 MQLs (14.5%) have Unknown/NaN origin — excluded from channel-level analysis

### SQL Used:
```sql
SELECT COUNT(*) FROM olist.marketing_qualified_leads;     -- 8,000
SELECT COUNT(*) FROM olist.closed_deals;                   -- 842
```

---

## SCAN Framework

### S — Stakeholder Goals
- **VP Marketing**: Channel ROI, budget allocation (should we shift 30% Organic budget to Paid Search?)
- **Head of Acquisition**: Channel quality, lead behavior profiles (what drives Social's low conversion?)
- **VP Sales**: Sales cycle efficiency (is 44→24 day compression sustainable?)

### C — Columns and Coverage
- **Data Available**: 2 marketing tables (MQLs + deals), 9 e-commerce tables (orders, sellers)
- **Can Answer**: Conversion rate by channel, LTV by channel, lead behavior distribution, time-to-close
- **Cannot Answer (Gaps)**: Ad spend data (no cost per click), post-purchase behavior of converted sellers, competitor channels

### A — Aggregates and Anomalies
| Metric | Value | Insight |
|--------|-------|---------|
| Total MQLs | 8,000 | Top-of-funnel volume baseline |
| Closed Deals | 842 | 10.53% overall conversion |
| LTV/MQL (Top) | $95.61 (Paid Search) | $6.29 gap to Organic ($89.32) |
| LTV/MQL (Bottom) | $17.21 (Email) | 5.6× gap from leader — lowest ROI |
| Avg Time-to-Close | 23–44 days (2018) | Compressing — improving efficiency |
| Shark Deals | 24 (2.9%) | Rare profile — not actionable at channel level |

### N — Notable Segments
- **Wolf-profile deals**: Social's 17.3% Wolf rate is nearly double other channels — structural drag on conversion
- **Shark deals by channel**: Paid Search highest (4.6% of deals, n=9) — reverses the hypothesis that Organic attracts low-quality leads, but sample too small for confidence
- **Cat dominates**: 48.3% of closed deals are Cat (stable, reliable) — the most common seller profile
- **Time compression**: Jan 2018 (43.7 days) → Apr 2018 (23.8 days) — 45% reduction in 4 months

---

## North Star Deep Dive

### North Star Metric: LTV/MQL ($95.61 at Paid Search)
### North Star Dimensions: Channel Origin, Lead Behavior, Time

#### Decomposition: Revenue per Channel = MQLs × Conv. Rate × LTV/Seller
- **Paid Search**: 1,586 MQLs × 12.30% = 195 sellers × $777.65 = $151,642
- **Organic Search**: 2,296 MQLs × 11.80% = 271 sellers × $756.74 = $205,076
- **Social**: 1,350 MQLs × 5.56% = 75 sellers × $578.59 = $43,394

#### Cross-Tabulation Findings:
| Dimension Combination | Finding | Impact |
|----------------------|---------|--------|
| Channel × Lead Behavior | Social 17.3% Wolf vs 9.6–10.8% others | Structural conversion drag |
| Channel × LTV | Paid Search $95.61 vs Social $32.14 | 3× LTV/MQL gap |
| Time × Time-to-Close | 44→24 days in 4 months | Sales cycle efficiency improving |
| Lead Behavior × Deals | Cat 48%, Wolf 11%, Shark 3% | Most sellers are low-maintenance |

---

## Marketing Funnel Performance

### MQL Volume by Channel

| Channel | MQLs | % of Total |
|---------|------|-----------|
| Organic Search | 2,296 | 28.7% |
| Paid Search | 1,586 | 19.8% |
| Social | 1,350 | 16.9% |
| Unknown | 1,099 | 13.7% |
| Direct Traffic | 499 | 6.2% |
| Email | 493 | 6.2% |
| Referral | 284 | 3.6% |
| Other | 150 | 1.9% |
| Display | 118 | 1.5% |
| Other Publicities | 65 | 0.8% |
| NaN (data issue) | 60 | 0.8% |

*Source: `olist.kpi_mql_volume` in `sql/phase5_funnel.py:36`.*

### Conversion Rate by Channel

| Channel | MQLs | Closed Deals | Conversion Rate |
|---------|------|-------------|----------------|
| Paid Search | 1,586 | 195 | **12.30%** |
| Organic Search | 2,296 | 271 | **11.80%** |
| Direct Traffic | 499 | 56 | **11.22%** |
| Referral | 284 | 24 | 8.45% |
| Social | 1,350 | 75 | 5.56% |
| Display | 118 | 6 | 5.08% |
| Other Publicities | 65 | 3 | 4.62% |
| Email | 493 | 15 | 3.04% |
| Other | 150 | 4 | 2.67% |

*Source: `olist.kpi_conversion_rate` in `sql/phase5_funnel.py:52`.*

**Finding:** Paid Search (12.3%) edges Organic (11.8%) and Direct (11.2%) for conversion. Social's 5.56% on 1,350 MQLs is the largest volume-efficiency gap.

---

### LTV by Channel

| Channel | MQLs | Sellers w/ Orders | Total Revenue | LTV/MQL | LTV/Seller |
|---------|------|------------------|--------------|---------|------------|
| Organic Search | 2,296 | 271 | $205,076 | $89.32 | $756.74 |
| Paid Search | 1,586 | 195 | $151,642 | **$95.61** | **$777.65** |
| Social | 1,350 | 75 | $43,394 | $32.14 | $578.59 |
| Direct Traffic | 499 | 56 | $21,853 | $43.79 | $390.23 |
| Referral | 284 | 24 | $16,578 | $58.37 | $690.76 |
| Email | 493 | 15 | $8,485 | $17.21 | $565.67 |

*Source: `olist.kpi_ltv_by_channel` in `sql/phase5_funnel.py:71`.*
*Uses LEFT JOIN (all MQLs in denominator, including non-converting). Excludes Unknown/NaN origin MQLs.*

**Finding:** Paid Search leads in LTV/MQL ($95.61) and LTV/Seller ($777.65). The gap to Organic ($89.32 / $756.74) is only ~7%. Previously reported $4,200+ figures were inflated by INNER JOIN bug.

---

### Lead Behavior Profiles

| Profile | Definition | Closed Deals | % of Total |
|---------|-----------|-------------|-----------|
| **Cat** | Stable, reliable, low-maintenance | 407 | 48.3% |
| **Eagle** | Fast, decisive, high-value | 123 | 14.6% |
| **Wolf** | Aggressive, high-maintenance | 95 | 11.3% |
| **Shark** | Predatory, high-risk | 24 | 2.9% |
| Unassigned | No profile recorded | 193 | 22.9% |

*Source: `olist.kpi_lead_behavior` in `sql/phase5_funnel.py:90`.*

**Finding:** Cat leads dominate (48%). Profiles are assigned at deal stage — they describe closed deal composition, not MQL conversion likelihood.

---

### Channel × Lead Behavior Cross-Tabulation

| Channel | MQLs | Conv% | Cat | Eagle | Wolf | Shark | Unassigned |
|---------|------|-------|-----|-------|------|-------|------------|
| Organic Search | 2,296 | 11.80% | 130 (48.0%) | 38 (14.0%) | 26 (9.6%) | 4 (1.5%) | 73 (26.9%) |
| Paid Search | 1,586 | 12.30% | 94 (48.2%) | 34 (17.4%) | 21 (10.8%) | **9 (4.6%)** | 37 (19.0%) |
| Social | 1,350 | 5.56% | 31 (41.3%) | 14 (18.7%) | **13 (17.3%)** | 4 (5.3%) | 13 (17.3%) |
| Direct Traffic | 499 | 11.22% | 26 (46.4%) | 5 (8.9%) | 8 (14.3%) | 1 (1.8%) | 16 (28.6%) |
| Email | 493 | 3.04% | 9 (60.0%) | 2 (13.3%) | 3 (20.0%) | 0 (0%) | 1 (6.7%) |
| Referral | 284 | 8.45% | 15 (62.5%) | 3 (12.5%) | 1 (4.2%) | 0 (0%) | 5 (20.8%) |

*Source: `olist.kpi_channel_lead_behavior` in `sql/phase5_funnel.py:137`.*

**Finding 1 — Shark reversal:** Paid Search has highest Shark concentration (4.6%), not Organic (1.5%). But n=9 vs n=4 — too small to act on.

**Finding 2 — Wolf explains Social's conversion gap:** Social's 17.3% Wolf rate is nearly double Organic (9.6%) and Paid (10.8%). Channels with higher Wolf rates consistently show lower conversion. This is a **structural channel characteristic** — Social attracts sellers that are inherently harder to close.

**Practical implication:** The fix isn't "audit lead quality" on Social — it's "build Wolf-specific closing capabilities."

---

### Time-to-Close Trend

| Month | Avg Days | Deals Won |
|-------|----------|-----------|
| 2017-12 | 122.4 | 11 |
| 2018-01 | 43.7 | 152 |
| 2018-02 | 42.3 | 149 |
| 2018-03 | 37.6 | 167 |
| 2018-04 | 23.8 | 183 |
| 2018-05 | 32.8 | 130 |

*Source: `olist.kpi_time_to_close` in `sql/phase5_funnel.py:121`.*

**Finding:** Time-to-close decreased 45% from Jan 2018 (43.7 days) to Apr 2018 (23.8 days). Dec 2017's 122-day avg is a small-sample anomaly (11 deals). The compression trend suggests improving sales efficiency.

---

## Data Quality Issues Found

| Issue | Impact | Resolution |
|-------|--------|------------|
| LTV view used `INNER JOIN` | Denominator excluded non-converting MQLs — inflated LTV/MQL ($4,200→$95) | Fixed to `LEFT JOIN` in `phase5_funnel.py:67` |
| Lead behavior profiles deal-stage only | Cannot predict MQL conversion likelihood by profile | Documented — profiles describe deal composition, not MQL quality |
| 1,159 MQLs (14.5%) with Unknown/NaN origin | Cannot attribute 1 in 7 MQLs to a channel | Excluded from channel-level LTV/conversion analysis |
| ~20% of closed deals missing `seller_id` | Cannot link those deals to revenue for LTV | LEFT JOIN preserves deals as $0 revenue contributors |
| `kpi_lead_behavior` view excludes NULL profiles | Undercounts total deals shown (665 vs 842) | Tracked separately: 177 NULL-profile deals (21.0%) |

### Key SQL Views for Marketing Dashboard

| View | Purpose | Source File |
|------|---------|-------------|
| `kpi_mql_volume` | MQL count by month + channel | `phase5_funnel.py:36` |
| `kpi_conversion_rate` | Conversion % by channel | `phase5_funnel.py:52` |
| `kpi_ltv_by_channel` | LTV per MQL + per seller (LEFT JOIN fix applied) | `phase5_funnel.py:71` |
| `kpi_lead_behavior` | Distribution of Cat/Eagle/Wolf/Shark profiles | `phase5_funnel.py:90` |
| `kpi_time_to_close` | Avg days to close by month | `phase5_funnel.py:121` |
| `kpi_channel_lead_behavior` | Channel × Lead Behavior cross-tab | `phase5_funnel.py:137` |
| `kpi_monthly_trend` | Monthly volume × conversion × close time | `phase5_funnel.py:200` |

---

## Business Recommendations (Marketing Funnel)

### 1. Fix Social Channel Conversion (Medium-High Impact)
- **Target**: Social has 1,350 MQLs (16.9%) at 5.56% conversion — worst among major channels; 17.3% Wolf-profile deal mix is structural drag
- **Action**: Build Wolf-specific SDR playbook; add behavioral lead scoring; set 2-quarter benchmark (target ~8% conversion)
- **Derivation**: +33 deals × $578.59 LTV = $19K gross → 50% confidence discount
- **Conservative Estimate**: ~$7K–$12K

### 2. Incrementally Increase Paid Search (Low Impact)
- **Target**: Paid Search leads LTV/MQL ($95.61) but gap to Organic ($89.32) is only ~7%
- **Action**: Increase budget 10–15%; A/B test ad copy targeting Cat-profile sellers
- **Derivation**: +200 MQLs × 12.30% = +25 deals × $777.65 = $19K → 50% saturation discount
- **Conservative Estimate**: ~$8K–$12K

### 3. No Action Needed on Sales Cycle
- Time-to-close compressed 44→24 days. Monitor monthly; investigate if >45 days.

### Combined 1-Year Impact:
| Initiative | Estimate | Confidence |
|------------|----------|------------|
| Social Conversion Fix | ~$7K–$12K | Medium — Wolf-profile data grounded |
| Paid Search Incremental | ~$8K–$12K | Low — volume saturation unknown |
| **Total Conservative** | **~$15K–$24K** | |

---

## Interview-Ready Summary

**One-Sentence Project Summary:**
> "I built a marketing funnel dashboard for Olist (Brazilian e-commerce) using PostgreSQL and Python, finding that Paid Search slightly leads in LTV/MQL ($95.61 vs $89.32 Organic) but Social's 5.56% conversion on 1,350 MQLs is the bigger opportunity — with every metric traceable to its SQL source."

**5 Numbers to Memorize:**
1. **MQLs**: 8,000 (Jun 2017–Jun 2018), 842 closed deals (10.5% conversion)
2. **LTV/MQL**: Paid Search $95.61, Organic $89.32 (corrected via LEFT JOIN fix — was $4,200/$3,200)
3. **Problem**: LTV denominator bug (INNER JOIN → LEFT JOIN) inflated numbers 44×
4. **Key Insight**: Social's 17.3% Wolf-profile deal mix explains its low conversion — not lead quality
5. **Differentiator**: Data traceability — every number linked to its SQL view and line number

---

*Log created: 2026-05-07*
*Last updated: 2026-05-13*
