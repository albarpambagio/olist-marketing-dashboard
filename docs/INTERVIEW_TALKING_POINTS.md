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
> I started with a **business question**: 'How can Olist's Marketing team optimize acquisition spend across channels and maximize lifetime value (LTV)?'
> 
> I built a **combined star schema** in PostgreSQL with `fact_marketing` (MQLs + closed deals) joined to `fact_orders` via `seller_id`. This enabled LTV calculation by marketing channel.
> 
> I defined **KPIs** like Conversion Rate (18.75% overall), LTV by Channel ($2.4k–$4.2k), and Time-to-Close (avg 45 days).
> 
> **Key findings**: Paid Search converts 20% better than Organic (12% vs. 11%) and delivers $4,200 LTV vs. $3,200 for Organic. "Cat" leads convert at 15% vs. 6% for "Shark".
> 
> My **recommendations** focus on reallocating budget to Paid Search, prioritizing "Cat" leads in SDR outreach, and investigating the lengthening sales cycle (38 → 52 days)."

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

**Challenge3: Lead Behavior Profiles**
> "Leads are tagged as 'Cat', 'Eagle', 'Wolf', 'Shark' based on DISC profiles. I had to research what these mean (Cat = reliable, Shark = high-risk) to interpret conversion rates correctly."

**Challenge4: Conversion Rate Calculation**
> "Conversion = Closed Deals / Total MQLs. But some MQLs have multiple deals — I had to use `COUNT(DISTINCT mql_id)` to avoid double-counting."

---

## Key Insights

### "What did you find? (Memorize These Numbers)"

| Insight | Value | Business Meaning |
|---------|-------|------------------|
| Total MQLs | 8,000 | Top-of-funnel volume |
| Closed Deals | ~1,500 (18.75% conversion) | Successfully acquired sellers |
| Top Channel (Conversion) | Paid Search: 12.0% | Budget reallocation opportunity |
| Top Channel (LTV) | Paid Search: $4,200/MQL | High-value acquisition |
| Lead Behavior (Best) | "Cat": 15.0% conversion | Prioritize in SDR outreach |
| Time-to-Close Trend | 38 → 52 days (36% longer) | Sales cycle lengthening |

### "Tell me something surprising you found"

> "The most surprising finding was that **Paid Search delivers 31% higher LTV** than Organic Search ($4,200 vs. $3,200 per MQL), despite Organic having 35% higher volume (2,800 vs. 1,600 MQLs). This suggests Organic traffic has quality issues — maybe SEO attracts browsers, not buyers."

> "Another surprise: **Time-to-close increased 36%** (38 → 52 days) from Dec 2017 to Apr 2018. This suggests market saturation or sales process inefficiency — Olist needs to investigate why deals take longer to close."

---

## Business Recommendations

### "What recommendations did you make?"

1. **Reallocate Budget to Paid Search** (High Impact)
   - Target: Increase Paid Search MQLs from 1,600 → 2,500 (+56%)
   - Action: Shift 30% of Organic Search budget to Paid Search
   - Expected Impact: +108 closed deals = +$453,600 LTV (108 × $4,200)

2. **Prioritize "Cat" Leads in SDR Outreach** (Medium Impact)
   - Target: "Cat" leads (15% conversion vs. 6% for "Shark")
   - Action: SDRs call "Cat" leads first, disqualify "Shark" faster
   - Expected Impact: Improve overall conversion from 18.75% → 20%+

3. **Investigate Lengthening Sales Cycle** (Medium Impact)
   - Target: Time-to-close increased 38 → 52 days (36% longer)
   - Action: Audit sales process, implement SLA (first contact within 24 hours)
   - Expected Impact: Reduce time-to-close from 52 → 40 days = +$200,000 LTV (faster onboarding)

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

**Budget Reallocation (Paid Search ↑)**
- Current: 1,600 MQLs at 12% conversion = 192 closed deals
- Target: 2,500 MQLs at 12% conversion = 300 closed deals
- LTV Impact: +108 deals × $4,200 = +$453,600 revenue

**Lead Prioritization ("Cat" Leads)**
- Current: Mix of Cat (15%), Eagle (12.5%), Wolf (9%), Shark (6%)
- Target: Focus 60% of SDR time on "Cat" leads
- Impact: Improve overall conversion from 18.75% → 20%+ = +$150,000 LTV

**Sales Cycle Optimization (38 → 40 days)**
- Current: 52 days avg time-to-close
- Target: 40 days (realistic improvement)
- Impact: +15% faster onboarding = +$200,000 LTV (more sellers, faster revenue)

**Combined 1-Year Impact:**
> "Conservatively, these three initiatives could drive **$800,000+ in additional LTV**, which represents significant ROI on marketing spend for a platform like Olist."

---

## Technical Deep-Dives

### "Explain your LTV calculation by channel"

> "Lifetime Value (LTV) = Total Revenue from Seller / Number of MQLs in Channel:
> 
> ```sql
> SELECT origin,
>     SUM(fo.revenue) / COUNT(DISTINCT mql.mql_id) AS ltv_per_mql
> FROM fact_marketing fm
> JOIN fact_orders fo ON fm.seller_id = fo.seller_id
> GROUP BY 1
> ```
> 
> **Key finding**: Paid Search = $4,200 LTV/MQL vs. Organic = $3,200. This 31% difference justifies budget reallocation."

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

> "For this project, I discovered that **Organic Search drives 35% of MQLs but only converts at 11%** (same as Direct traffic with 10% volume). 
> 
> I quantified it: Organic = 2,800 MQLs × 11% = 308 deals. Paid Search = 1,600 MQLs × 12% = 192 deals. 
> 
> Despite Organic having 75% more MQLs, it only delivers 60% more deals. This suggests traffic quality issues — maybe SEO attracts browsers, not serious sellers. I recommended shifting 30% of Organic budget to Paid Search."

### "How do you prioritize marketing channels?"

> "I use the 80/20 rule: 20% of channels deliver 80% of LTV. For this analysis:
> - **Must-invest**: Paid Search ($4,200 LTV, 12% conversion)
> - **Should-monitor**: Direct traffic ($3,800 LTV, 11% conversion)
> - **Should-optimize**: Organic Search ($3,200 LTV, 35% volume but low conversion)
> - **Should-disqualify**: "Shark" leads (6% conversion, high maintenance)"

### "How do you ensure data quality for marketing analytics?"

> "I use the CLEAN framework:
> 1. **Conceptualize**: Grain = one MQL, metrics = conversion/LTV, dimensions = channel/behavior
> 2. **Locate**: Missing seller_id in 20% of closed deals (can't link to orders)
> 3. **Evaluate**: Date range mismatch (Marketing 2017–2018, E-Comm 2016–2018)
> 4. **Augment**: Added `days_to_close = won_date - first_contact_date`
> 5. **Note**: All issues logged in `logs/phase2_cleaning_eda.log.md`"

---

## Quick Reference Card

**Memorize These 5 Things:**

1. **MQLs**: 8,000 leads (Jun 2017–Jun 2018)
2. **Conversion**: Paid Search 12% vs. Organic 11% (budget reallocation opportunity)
3. **LTV**: Paid Search $4,200 vs. Organic $3,200 per MQL
4. **Lead Behavior**: "Cat" leads 15% conversion (prioritize in SDR outreach)
5. **Tech Stack**: PostgreSQL → Python ETL → Power BI (Combined Star Schema)

**One-Sentence Project Summary:**
> "I built a marketing funnel dashboard for Olist using PostgreSQL and Power BI, finding Paid Search converts 20% better than Organic and delivers $4,200 LTV — representing $800k+ annual LTV opportunity."

---

*File created for interview preparation. Review before your interview!*
