// ==========================================
// Bulk DAX Measures — Marketing Funnel Dashboard
// Script Version: 1.1 (simplified for wider TE compatibility)
// ==========================================
// PREREQUISITES:
//   - Power BI Desktop with Marketing model open
//   - Tabular Editor 2.x (External Tools)
//
// STEPS:
//   1. In Power BI Desktop:
//        Modeling → New Table → paste:
//          Measures = DATATABLE("placeholder", INTEGER, {{1}})
//        Delete the "placeholder" column (keep the table)
//   2. Click anywhere in the model
//   3. External Tools → Tabular Editor  (wait for it to load)
//   4. Advanced Scripting tab (C# icon) → paste all of this
//   5. Press F5 (Run) → Close Tabular Editor
//   6. All 13 measures appear in "Measures" table with formatting & folders
// ==========================================

// --- Find or fail-fast on Measures table ---
var t = Model.Tables["Measures"];
if (t == null) {
    Error("No table named 'Measures' found. Create it first: Modeling → New Table → Measures = {{1}}");
    return;
}

// --- Helper: create + format a measure ---
void AddM(string name, string dax, string folder, string fmt)
{
    var m = t.AddMeasure(name, dax, folder);
    m.FormatString = fmt;
}

// === FUNNEL ===
AddM("MQL Count",         "COUNTROWS(dim_marketing)",                    "Funnel",   "#,#0");
AddM("Deals Won",         "COUNTROWS(FILTER(dim_marketing, dim_marketing[seller_id] <> BLANK()))", "Funnel", "#,#0");
AddM("Conversion Rate",   "DIVIDE([Deals Won], [MQL Count], 0)",         "Funnel",   "0.00%");

// === REVENUE ===
AddM("Total Revenue",     "SUM(fact_marketing[revenue])",                "Revenue",  "$#,##0.00");
AddM("Total Orders",      "COUNTROWS(fact_marketing)",                   "Revenue",  "#,#0");
AddM("AOV",               "DIVIDE([Total Revenue], [Total Orders], 0)",  "Revenue",  "$#,##0.00");
AddM("LTV per MQL",       "DIVIDE([Total Revenue], [MQL Count], 0)",     "Revenue",  "$#,##0.00");
AddM("LTV per Seller",    "DIVIDE([Total Revenue], [Deals Won], 0)",     "Revenue",  "$#,##0.00");

// === QUALITY ===
AddM("Avg Review Score",  "AVERAGE(fact_marketing[review_score])",       "Quality",  "0.0");
AddM("Late Delivery %",   "DIVIDE(COUNTROWS(FILTER(fact_marketing, fact_marketing[is_late] = 1)), [Total Orders], 0)", "Quality", "0.00%");
AddM("Repeat Customer %", "DIVIDE(COUNTROWS(FILTER(fact_marketing, fact_marketing[is_repeat_customer] = 1)), [Total Orders], 0)", "Quality", "0.00%");
AddM("Avg Days to Close", "AVERAGE(fact_marketing[days_to_close])",      "Quality",  "0.0");

// === COUNTS ===
AddM("Unique Sellers",    "COUNTROWS(dim_seller)",                       "Counts",   "#,#0");

// --- Confirm ---
Info("13 measures loaded into Measures table.");