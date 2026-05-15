# DAX Measures — Marketing Funnel Dashboard

## Load Measures — TMDL View (Native, No Installation)

1. **Modeling → New Table** → `Measures = DATATABLE("x", INTEGER, {{1}})` → Delete the column `"x"` (keep the empty table)
2. **Model View** → Click the **TMDL icon** in the ribbon
3. **Copy the TMDL script below** → Paste into the TMDL editor
4. Click **Apply** (top-left corner of TMDL editor)
5. All 13 measures are created, formatted, and grouped — **no renaming needed** (names already have spaces)

```tmdl
createOrReplace

  table 'Measures'

    /// Total number of marketing qualified leads
    measure 'MQL Count' = CALCULATE(
        DISTINCTCOUNT('olist fact_marketing'[mql_id]),
        AND('olist fact_marketing'[origin] <> "unknown", NOT ISBLANK('olist fact_marketing'[origin]))
    )
        formatString: #,##0

    /// MQLs that converted into a seller (have non-null seller_id)
    measure 'Deals Won' = CALCULATE(
        DISTINCTCOUNT('olist fact_marketing'[mql_id]),
        AND('olist fact_marketing'[origin] <> "unknown", NOT ISBLANK('olist fact_marketing'[origin])),
        NOT ISBLANK('olist fact_marketing'[seller_id])
    )
        formatString: #,##0

    /// Percentage of MQLs that became deals
    measure 'Conversion Rate' = DIVIDE([Deals Won], [MQL Count], 0)
        formatString: 0.00%

    /// Total revenue from converted leads
    measure 'Total Revenue' = SUM('olist fact_marketing'[revenue])
        formatString: $ #,##0.00

    /// Total number of orders placed
    measure 'Total Orders' = COUNTROWS('olist fact_marketing')
        formatString: #,##0

    /// Average revenue per order
    measure 'AOV' = DIVIDE([Total Revenue], [Total Orders], 0)
        formatString: $ #,##0.00

    /// Lifetime value per marketing qualified lead
    measure 'LTV per MQL' = DIVIDE([Total Revenue], [MQL Count], 0)
        formatString: $ #,##0.00

    /// Average revenue per acquired seller
    measure 'LTV per Seller' = DIVIDE([Total Revenue], [Deals Won], 0)
        formatString: $ #,##0.00

    /// Average customer review score per deal
    /// Uses AVERAGEX at mql_id level to avoid duplicate counting from LEFT JOIN with fact_orders
    measure 'Avg Review Score' = AVERAGEX(
        VALUES('olist fact_marketing'[mql_id]),
        CALCULATE(AVERAGE('olist fact_marketing'[review_score]))
    )
        formatString: 0.0

    /// Percentage of orders delivered late
    measure 'Late Delivery %' = DIVIDE(COUNTROWS(FILTER('olist fact_marketing', 'olist fact_marketing'[is_late] = 1)), [Total Orders], 0)
        formatString: 0.00%

    /// Percentage of orders from repeat customers
    measure 'Repeat Customer %' = DIVIDE(COUNTROWS(FILTER('olist fact_marketing', 'olist fact_marketing'[is_repeat_customer] = 1)), [Total Orders], 0)
        formatString: 0.00%

    /// Average days to close a deal from first contact
    /// Uses AVERAGEX at mql_id level to avoid duplicate counting from LEFT JOIN with fact_orders
    measure 'Avg Days to Close' = AVERAGEX(
        VALUES('olist fact_marketing'[mql_id]),
        CALCULATE(MIN('olist fact_marketing'[days_to_close]))
    )
        formatString: 0.0

    /// Count of unique sellers in the marketplace
    measure 'Unique Sellers' = COUNTROWS('olist dim_seller')
        formatString: #,##0
```

---

## Funnel KPIs

### MQL Count
```dax
MQL Count = CALCULATE(
    DISTINCTCOUNT('olist fact_marketing'[mql_id]),
    AND('olist fact_marketing'[origin] <> "unknown", NOT ISBLANK('olist fact_marketing'[origin]))
)
```
Filters out unknown/blank origins.

### Deals Won
```dax
Deals Won = CALCULATE(
    DISTINCTCOUNT('olist fact_marketing'[mql_id]),
    AND('olist fact_marketing'[origin] <> "unknown", NOT ISBLANK('olist fact_marketing'[origin])),
    NOT ISBLANK('olist fact_marketing'[seller_id])
)
```
Uses `olist.dim_marketing` with filter to exclude Unknown/NaN origins (matches SQL view logic).

### Deals Won
```dax
Deals Won = CALCULATE(DISTINCTCOUNT('olist fact_marketing'[mql_id]), FILTER('olist fact_marketing', 'olist fact_marketing'[seller_id] <> BLANK()))
```
MQLs that converted into a seller (have a non-null `seller_id` from `closed_deals`).

### Conversion Rate
```dax
Conversion Rate = DIVIDE([Deals Won], [MQL Count], 0)
```

---

## Revenue & Orders

### Total Revenue
```dax
Total Revenue = SUM('olist fact_marketing'[revenue])
```

### Total Orders
```dax
Total Orders = COUNTROWS('olist fact_marketing')
```
Each row is one MQL x Order combination.

### AOV (Average Order Value)
```dax
AOV = DIVIDE([Total Revenue], [Total Orders], 0)
```

### LTV per MQL
```dax
LTV per MQL = DIVIDE([Total Revenue], [MQL Count], 0)
```

### LTV per Seller
```dax
LTV per Seller = DIVIDE([Total Revenue], [Deals Won], 0)
```

---

## Quality Metrics

### Avg Review Score
```dax
Avg Review Score = AVERAGEX(
    VALUES('olist fact_marketing'[mql_id]),
    CALCULATE(AVERAGE('olist fact_marketing'[review_score]))
)
```

### Late Delivery %
```dax
Late Delivery % =
DIVIDE(
    COUNTROWS(FILTER('olist fact_marketing', 'olist fact_marketing'[is_late] = 1)),
    [Total Orders],
    0
)
```

### Repeat Customer %
```dax
Repeat Customer % =
DIVIDE(
    COUNTROWS(FILTER('olist fact_marketing', 'olist fact_marketing'[is_repeat_customer] = 1)),
    [Total Orders],
    0
)
```

### Avg Days to Close
```dax
Avg Days to Close = AVERAGEX(
    VALUES('olist fact_marketing'[mql_id]),
    CALCULATE(MIN('olist fact_marketing'[days_to_close]))
)
```
> **Important:** Must use `AVERAGEX` at `mql_id` level. The `fact_marketing` view uses `LEFT JOIN` with `fact_orders`, creating multiple rows per deal. Using plain `AVERAGE` would count duplicate days_to_close values multiple times, skewing results lower.

---

## Counts

### Unique Sellers
```dax
Unique Sellers = COUNTROWS('olist dim_seller')
```

---

## Standard Slicers

| Slicer | Table | Field |
|--------|-------|-------|
| Year | `olist dim_date` | `year` |
| Channel | `olist dim_channel` | `channel_name` |
| Lead Behavior | `olist dim_marketing` | `lead_behaviour_profile` |
| Seller State | `olist dim_seller` | `seller_state` |
| Seller City | `olist dim_seller` | `seller_city` |

---

## Relationship Reference

| From | To | Cardinality | Key |
|------|----|-------------|-----|
| `olist dim_marketing` | `olist fact_marketing` | 1:* | `mql_id` |
| `olist dim_channel` | `olist fact_marketing` | 1:* | `origin` (`channel_id`) |
| `olist dim_date` | `olist fact_marketing` | 1:* | `lead_date` → `date_key` |
| `olist fact_marketing` | `olist dim_seller` | *:1 | `seller_id` |
| `olist dim_seller` | `olist fact_orders` | 1:* | `seller_id` |

> Only import `olist fact_orders` if you need drill-through to individual order details. For dashboard-level KPIs, all measures come from `olist fact_marketing` + `olist dim_marketing` + `olist dim_seller`.
