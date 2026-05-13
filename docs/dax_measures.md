# DAX Measures — Marketing Funnel Dashboard

## Bulk-Loading Measures

You have **two options** — both create identical measures:

| Method | External Tool? | Naming | Speed |
|--------|:-:|--------|-------|
| **TMDL View** (native in PBI) | ❌ No | Uses underscores → rename in UI after apply | 1 min |
| **Tabular Editor** (free ext. tool) | ✅ Install once | Spaces in names, formatting in one shot | 30 sec |

### Method A — TMDL View (Native, No Installation)

1. **Modeling → New Table** → `Measures = DATATABLE("x", INTEGER, {{1}})` → Delete column `"x"`
2. **Model view** → Click **TMDL icon** in the ribbon
3. Open `docs/bulk_measures.csl` → **Select All → Copy** → Paste into TMDL editor
4. Click **Apply** (top-left corner)
5. Go back to Report view — rename measures: double-click each, replace `_` with ` `
   - `MQL_Count` → `MQL Count`
   - `Deals_Won` → `Deals Won`
   - `Conversion_Rate` → `Conversion Rate`
   - `Total_Revenue` → `Total Revenue`
   - `Total_Orders` → `Total Orders`
   - `Avg_Review_Score` → `Avg Review Score`
   - `Late_Delivery_Percentage` → `Late Delivery %`
   - `Repeat_Customer_Percentage` → `Repeat Customer %`
   - `Avg_Days_to_Close` → `Avg Days to Close`
   - `Unique_Sellers` → `Unique Sellers`

### Method B — Tabular Editor (Recommended for Nice Names)

1. Install [Tabular Editor](https://tabulareditor.com/)
2. In PBI Desktop: **External Tools → Tabular Editor**
3. **Advanced Scripting** tab → open `docs/bulk_measures.cs` → **Ctrl+A → F5**
4. All 13 measures created with spaces in names, formatting, and display folders — done.

---

## Funnel KPIs

### MQL Count
```dax
MQL Count = COUNTROWS(dim_marketing)
```
Uses `dim_marketing` to avoid double-counting MQLs that expanded to multiple order rows in `fact_marketing`.

### Deals Won
```dax
Deals Won = COUNTROWS(FILTER(dim_marketing, dim_marketing[seller_id] <> BLANK()))
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
Total Revenue = SUM(fact_marketing[revenue])
```

### Total Orders
```dax
Total Orders = COUNTROWS(fact_marketing)
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
Avg Review Score = AVERAGE(fact_marketing[review_score])
```

### Late Delivery %
```dax
Late Delivery % = 
DIVIDE(
    COUNTROWS(FILTER(fact_marketing, fact_marketing[is_late] = 1)),
    [Total Orders],
    0
)
```

### Repeat Customer %
```dax
Repeat Customer % = 
DIVIDE(
    COUNTROWS(FILTER(fact_marketing, fact_marketing[is_repeat_customer] = 1)),
    [Total Orders],
    0
)
```

### Avg Days to Close
```dax
Avg Days to Close = AVERAGE(fact_marketing[days_to_close])
```

---

## Counts

### Unique Sellers
```dax
Unique Sellers = COUNTROWS(dim_seller)
```

---

## Standard Slicers

| Slicer | Table | Field |
|--------|-------|-------|
| Year | `dim_date` | `year` |
| Channel | `dim_channel` | `channel_name` |
| Lead Behavior | `dim_marketing` | `lead_behaviour_profile` |
| Seller State | `dim_seller` | `seller_state` |
| Seller City | `dim_seller` | `seller_city` |

---

## Relationship Reference

| From | To | Cardinality | Key |
|------|----|-------------|-----|
| `dim_marketing` | `fact_marketing` | 1:* | `mql_id` |
| `dim_channel` | `fact_marketing` | 1:* | `origin` (`channel_id`) |
| `dim_date` | `fact_marketing` | 1:* | `lead_date` → `date_key` |
| `fact_marketing` | `dim_seller` | *:1 | `seller_id` |
| `dim_seller` | `fact_orders` | 1:* | `seller_id` |

> Only import `fact_orders` if you need drill-through to individual order details. For dashboard-level KPIs, all measures come from `fact_marketing` + `dim_marketing` + `dim_seller`.
