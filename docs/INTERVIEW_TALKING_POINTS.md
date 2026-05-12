# Interview Talking Points - Olist Marketing Funnel Dashboard

## Table of Contents
1. [Project Walkthrough](#project-walkthrough)
2. [Technical Decisions](#technical-decisions)
3. [Data Challenges](#data-challenges)
4. [Key Insights](#key-insights)
5. [Business Recommendations](#business-recommendations)
6. [What I'd Do Differently](#what-id-do-differently)
7. [Business Impact](#business-impact)
8. [Technical Deep-Dives](#technical-deep-dives)
9. [Behavioral Questions](#behavioral-questions)

---

## Project Walkthrough

**Question: "Walk me through this project"**

**Answer Structure:** Business Question → Data Model → KPIs → Insights → Recommendations

**Script:**
> "This project analyzes **8,000 Marketing Qualified Leads (MQLs)** from Olist (Jun 2017–Jun 2018) combined with **100,000 orders** to create a full-funnel view.
> 
> I started with **exec-level questions** — not analyst curiosity. For example: *'Should the VP of Marketing reallocate budget from Organic to Paid Search?'* and *'Should the Head of Sales Ops change SDR prioritization rules based on lead behavior?'* Every question maps to someone with budget authority.
> 
> I built a **combined star schema** in PostgreSQL with `fact_marketing` (MQLs + closed deals) joined to `fact_orders` via `seller_id`. This enabled LTV calculation by marketing channel.
> 
> I defined **KPIs** like Conversion Rate (10.5% overall), LTV by Channel ($17–$96/MQL), and Time-to-Close (24–44 days). Every metric is traceable to its SQL view — I learned this the hard way after discovering the original README had fabricated numbers.
> 
> **Key findings**: Paid Search leads in LTV/MQL ($95.61) but the gap to Organic ($89.32) is only ~7% — much narrower than the "12% vs 11% conversion" story suggested. Lead behavior profiles turned out to be deal-stage data, not MQL predictors. And the sales cycle was compressing (44→24 days), not lengthening.
> 
> My **recommendations** are conservative: ~$23K–$37K total, not $800K. I apply a 50% confidence discount and document every caveat. A $12K estimate you can defend beats a $453K one that collapses under one follow-up question."

---

## Technical Decisions

### "Why did you build a combined schema (Marketing + E-Commerce)?"

**Key Points:**
- **Full-funnel visibility**: MQL → Closed Deal → Seller → Orders → Revenue
- **LTV calculation**: Can't calculate without joining `fact_marketing` to `fact_orders` via `seller_id`
- **Cross-functional insights**: Marketing team sees revenue impact, not just leads
- **Industry practice**: Real marketing analytics always ties acquisition to revenue

**Follow-up:** "In production, I'd add Google Analytics/UTM parameters to track digital campaigns more granularly, but for this dataset, `origin` field provided channel attribution."

### "Why PostgreSQL over BigQuery/MySQL?"

**Answer:**
- **Local control**: Can run offline, full control over database
- **Cost**: Free, no cloud costs
- **PostgreSQL-specific**: GENERATE_SERIES for date spine, window functions for LTV calculation
- **Marketing analytics**: Complex JOINs (MQL → Deal → Seller → Orders) are cleaner in PostgreSQL

### "Why Python for loading marketing data?"

**Answer:**
- **Error handling**: Python's `try/except` better for debugging CSV loading issues
- **Flexibility**: Can add data validation (e.g., check `won_date >= first_contact_date`)
- **Automation ready**: Can be scheduled as cron job with email notifications for failed loads

---

## Data Challenges

### "What was the hardest data challenge?"

**Challenge1: Missing Seller_ID in Closed Deals**
> "About 20% of closed deals had `seller_id = NULL`, meaning I couldn't link them to orders for LTV calculation. I used LEFT JOINs and documented this as a data quality gap — in production, this would need engineering fix."

**Challenge2: Date Range Mismatch**
> "Marketing data is Jun 2017–Jun 2018, but e-commerce data is 2016–2018. LTV calculations only work for the overlapping period. I documented this scope limitation in the insights log."

**Challenge3: Lead Behavior Profiles — Stage Mismatch**
> "This was the most interesting data challenge. The lead behavior profiles (Cat/Eagle/Wolf/Shark) are **only recorded in the closed_deals table**, not in the MQL table. So they describe the seller's profile after conversion, not the lead's profile during qualification. This meant the original 'Cat leads convert at 15%' narrative was wrong — that was actually '15% of closed deals have the Cat profile.' I had to rewrite the analysis to reflect this limitation."

**Challenge4: Conversion Rate Calculation**
> "Conversion = Closed Deals / Total MQLs. But some MQLs have multiple deals — I had to use `COUNT(DISTINCT mql_id)` to avoid double-counting."

---

## Key Insights

### "What did you find? (Memorize These Numbers)"

| Insight | Value | Business Meaning |
|---------|-------|------------------|
| Total MQLs | 8,000 | Top-of-funnel volume |
| Closed Deals | 842 (10.5% conversion) | Successfully acquired sellers |
| Top Channel (Conversion) | Paid Search: 12.3% | Higher but gap to Organic (11.8%) is only ~7% |
| Top Channel (LTV) | Paid Search: $95.61/MQL | Not the fabricated $4,200 — corrected with LEFT JOIN |
| Social (Problem) | 1,350 MQLs at 5.56% conversion | High volume, low conversion — biggest drag |
| Time-to-Close Trend | 44 → 24 days (compressing) | Opposite of fabricated narrative — cycle is improving |

### "Tell me something surprising you found"

> "The most surprising finding was that **the original README numbers were fabricated**. The LTV figure was $4,200/seller — which is suspiciously round. When I actually ran the corrected query (switching from INNER JOIN to LEFT JOIN to include non-converting MQLs), the real LTV/MQL was $95.61. That's a 98% difference. It taught me to always, always trace every number back to its SQL source.
>
> "Another surprise: the sales cycle wasn't lengthening at all. It was compressing from 44 to 24 days. The fabricated '38→52 days' trend would have sent the team investigating a problem that didn't exist."
>
> "And the lead behavior profiles — I assumed they predicted conversion, but they're only recorded at deal stage. 'Cat leads convert at 15%' is actually 'Cat leads make up 48% of closed deals.' Two completely different stories."

---

## Business Recommendations

### "What recommendations did you make?"

1. **Fix Social Channel Conversion** (Medium Impact)
   - Target: Social has 1,350 MQLs (16.9% of volume) but 5.56% conversion
   - Action: Audit lead quality, add scoring before SDR handoff
   - Expected Impact: ~$15K–$25K if conversion improves to match Organic

2. **Incrementally Increase Paid Search** (Low-Medium Impact)
   - Target: Increase Paid Search budget by 10–15%
   - Action: A/B test ad copy targeting seller segments
   - Expected Impact: ~$8K–$12K (not $453K — the real LTV gap is too small for aggressive reallocation)

3. **Maintain Sales Cycle Efficiency** (Informational)
   - Target: Cycle is compressing (44→24 days) — just monitor
   - Action: Track monthly as leading indicator; investigate if >45 days

### "How would you prioritize these recommendations?"

> "I'd start with budget reallocation because:
> 1. Paid Search has proven 12% conversion vs. 11% for Organic — clear ROI
> 2. The data shows LTV = $4,200 vs. $3,200 — 31% higher return
> 3. Quick wins: Increase Paid Search budget = more high-LTV MQLs within days
> 
> Then tackle lead prioritization because "Cat" leads are 2.5× more likely to convert.
> 
> Sales cycle optimization is longer-term — requires process changes (SLAs, training)."

---

## What I'd Do Differently

### "What would you do differently if you could redo this?"

**1. Add UTM Parameter Tracking**
> "The `origin` field is limited (Organic, Paid, Social, Direct). In reality, I'd want UTM parameters (source, medium, campaign) to calculate ROI by specific ad campaigns and keywords."

**2. Add Cost Data per Channel**
> "I calculated LTV but not CAC (Customer Acquisition Cost). In production, I'd need marketing spend per channel to calculate ROAS (Return on Ad Spend) = LTV / CAC."

**3. Predictive Lead Scoring**
> "With lead behavior profiles and conversion history, I could build a model to predict which MQLs will convert *before* SDRs call them — saving hundreds of hours of wasted outreach."

**4. Use dbt for Data Transformations**
> "Instead of raw SQL views, I'd use dbt (data build tool) for version-controlled, tested, documented data transformations. It's becoming the industry standard for marketing analytics engineering."

---

## Business Impact

### "What do these recommendations mean for the business?"

**Social Channel Conversion Fix**
- Current: 1,350 MQLs at 5.56% conversion = 75 deals
- If matched to 11.80% (Organic benchmark): +84 deals × $578.59 LTV = ~$48K gross
- **Conservative:** ~$15K–$25K (50% confidence discount)
- *Caveat: Social lead quality may be fundamentally different; process change risk*

**Paid Search Incremental Budget**
- Current: 1,586 MQLs at 12.30% conversion = 195 deals
- Target: +200 MQLs at same rate = +25 deals × $777.65 LTV = ~$19K gross
- **Conservative:** ~$8K–$12K (50% saturation discount)
- *Caveat: Higher spend may attract lower-quality traffic*

**Combined 1-Year Impact:**
> "Conservatively, these improvements could drive **~$23K–$37K** in additional LTV. That's intentionally conservative. The previous $800K figure was built on fabricated numbers: $4,200 LTV, 1,500 deals, and a falsified sales cycle trend. I'd rather defend a $12K estimate with real SQL queries than try to explain how I got $453K from data that doesn't exist."

---

## Technical Deep-Dives

### "Explain your LTV calculation by channel — and the bug you fixed"

> "The original LTV calculation had a bug: it used `INNER JOIN` between MQLs, closed deals, sellers, and orders. This meant the `COUNT(DISTINCT mql.mql_id)` denominator only counted MQLs that had already closed a deal and had orders — inflating LTV/MQL dramatically.
>
> I fixed it by switching to `LEFT JOIN`, so non-converting MQLs are included in the denominator:
>
> ```sql
> SELECT origin,
>     ROUND(SUM(fo.revenue)::NUMERIC / COUNT(DISTINCT mql.mql_id), 2) AS ltv_per_mql
> FROM olist.marketing_qualified_leads mql
> LEFT JOIN olist.closed_deals cd USING (mql_id)
> LEFT JOIN olist.sellers s ON cd.seller_id = s.seller_id
> LEFT JOIN olist.fact_orders fo ON s.seller_id = fo.seller_id
> GROUP BY 1
> ```
> 
> **Impact**: Paid Search went from $4,200 LTV/MQL (fabricated) to $95.61 (real). The 31% 'Paid Search vs Organic advantage' collapsed from $4,200 vs $3,200 (fabricated) to $95.61 vs $89.32 (real) — a much narrower gap."

### "These LTV numbers look suspiciously round — are they real?"

> "Great catch. That was actually a bug I found during my data audit. The original `kpi_ltv_by_channel` view used `INNER JOIN`, which only counted MQLs that had already converted — meaning the denominator was wrong and LTV was inflated. Numbers like `$4,200` are suspiciously round because they were fabricated for the README, not pulled from queries.
>
> I fixed it by switching to `LEFT JOIN` so `ltv_per_mql = revenue ÷ ALL MQLs` in each channel (including non-converting leads). The corrected LTV will be lower but real. I also added a [Data Traceability](#data-traceability) section to the README that links every metric to its SQL source view and line number. Any number in the report can be reproduced with one `psql` command."

### "How did you calculate funnel conversion?"

> "Conversion Rate = Closed Deals / Total MQLs:
> 
> ```sql
> SELECT origin,
>     COUNT(DISTINCT cd.mql_id) * 100.0 / COUNT(DISTINCT mql.mql_id) AS conversion_rate_pct
> FROM olist.marketing_qualified_leads mql
> LEFT JOIN olist.closed_deals cd USING (mql_id)
> GROUP BY 1
> ```
> 
> **Finding**: Paid Search = 12.0%, Direct = 11.0%, Organic = 11.0%. Despite Organic having 35% more volume, it converts same as Direct traffic."

### "Why did you create `fact_marketing` view?"

> "I needed a combined view that joins MQLs → Closed Deals → Sellers → Orders:
> 
> ```sql
> CREATE VIEW fact_marketing AS
> SELECT dm.mql_id, dm.origin, cd.won_date, fo.revenue
> FROM dim_marketing dm
> LEFT JOIN closed_deals cd USING (mql_id)
> LEFT JOIN sellers s ON cd.seller_id = s.seller_id
> LEFT JOIN fact_orders fo ON s.seller_id = fo.seller_id
> ```
> 
> This enables full-funnel analysis: MQL → Deal → Revenue in one view."

---

## Behavioral Questions

### "Tell me about a time you found a marketing inefficiency"

> "For this project, I discovered that **Social generates 1,350 MQLs (16.9% of total) but converts at only 5.56%** — the lowest among major channels. Meanwhile, Paid Search converts at 12.30% with 1,586 MQLs.
> 
> I quantified it: if Social converted at the same rate as Organic (11.80%), it would generate ~159 deals instead of 75 — that's +84 additional sellers.
> 
> This is a bigger opportunity than the typical 'shift budget from Organic to Paid Search' story. Social has high volume but terrible conversion — the fix might be lead quality, not budget allocation."

### "How do you prioritize marketing channels?"

> "I look at conversion × LTV together, not in isolation. For this analysis:
> - **Highest conversion**: Paid Search (12.30%) and Organic (11.80%) — but the gap is only 7%, much smaller than the fabricated numbers suggested
> - **Highest LTV/MQL**: Paid Search ($95.61) and Organic ($89.32) — similar gap
> - **Biggest opportunity**: Social (5.56% conversion with 1,350 MQLs) — fixing this has higher upside than budget reallocation between close-performing channels
> - **Lowest priority**: Email (3.04%) and Other (2.67%) — too small to optimize"

### "How do you ensure data quality for marketing analytics?"

> "I use the CLEAN framework — and I have a particularly good story here because I found my own fabricated data:
> 1. **Conceptualize**: Grain = one MQL, metrics = conversion/LTV, dimensions = channel/behavior
> 2. **Locate**: Missing seller_id in 20% of closed deals; also found the original README had fabricated LTV numbers ($4,200 vs actual $95.61)
> 3. **Evaluate**: INNER JOIN bug inflated LTV denominator; lead behavior profiles are deal-stage only, not MQL-stage
> 4. **Augment**: Added `days_to_close = won_date - first_contact_date`; added cross-tab view; created monthly trend view
> 5. **Note**: Every issue logged, and the README now has a Data Traceability section linking every metric to its SQL view. If a hiring manager asks 'where does $95.61 come from?', I can show them the exact query and row output."

---

## Quick Reference Card

**Memorize These 5 Things:**

1. **MQLs**: 8,000 leads, 842 closed deals, 10.5% conversion (not the fabricated 18.75%)
2. **Conversion**: Paid Search 12.3% vs. Organic 11.8% (narrow gap, not the claimed 20% better)
3. **LTV**: Paid Search $95.61/MQL — corrected from fabricated $4,200 via LEFT JOIN fix
4. **Lead Behavior**: Profiles are deal-stage only — 48% Cat, 15% Eagle, 11% Wolf, 3% Shark of closed deals
5. **Key lesson**: Every number must be traceable to its SQL source; fabricated numbers collapse under scrutiny

**One-Sentence Project Summary:**
> "I built a marketing funnel dashboard for Olist using PostgreSQL and Python ETL, finding Paid Search slightly leads in LTV/MQL ($95.61 vs $89.32) but the biggest opportunity is fixing Social's 5.56% conversion — and I documented every data limitation so the numbers can survive an interview."

---

*File created for interview preparation. Review before your interview!*
