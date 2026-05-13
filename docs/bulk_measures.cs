// Bulk Measures — Marketing Funnel Dashboard
// Open Tabular Editor -> Advanced Scripting -> Paste -> F5

var measureTable = Model.Tables["Measures"];
if (measureTable == null) {
    measureTable = Model.AddTable("Measures");
    measureTable.Description = "Dashboard measures — right-click to manage";
}

// Helper
Measure NewMeasure(string name, string dax, string format = "", int decimals = 2, string desc = "") {
    var m = measureTable.AddMeasure(name);
    m.Expression = dax;
    m.Description = desc;
    if (format == "$") { m.FormatString = "$#,#0.00"; }
    else if (format == "%") { m.FormatString = "0.00%"; }
    else if (format == "#") { m.FormatString = "#,#0"; }
    else if (format == "0.0") { m.FormatString = "0.0"; }
    else { m.FormatString = "0.00"; }
    m.DisplayFolder = desc; // groups measures visually
    return m;
}

// === Funnel KPIs ===
NewMeasure("MQL Count", "COUNTROWS(dim_marketing)", "#", 0, "Funnel");
NewMeasure("Deals Won", "COUNTROWS(FILTER(dim_marketing, dim_marketing[seller_id] <> BLANK()))", "#", 0, "Funnel");
NewMeasure("Conversion Rate", "DIVIDE([Deals Won], [MQL Count], 0)", "%", 2, "Funnel");

// === Revenue & Orders ===
NewMeasure("Total Revenue", "SUM(fact_marketing[revenue])", "$", 2, "Revenue");
NewMeasure("Total Revenue (M)", "DIVIDE([Total Revenue], 1000000)", "$", 2, "Revenue");
NewMeasure("Total Orders", "COUNTROWS(fact_marketing)", "#", 0, "Revenue");
NewMeasure("AOV", "DIVIDE([Total Revenue], [Total Orders], 0)", "$", 2, "Revenue");
NewMeasure("LTV per MQL", "DIVIDE([Total Revenue], [MQL Count], 0)", "$", 2, "Revenue");
NewMeasure("LTV per Seller", "DIVIDE([Total Revenue], [Deals Won], 0)", "$", 2, "Revenue");

// === Quality ===
NewMeasure("Avg Review Score", "AVERAGE(fact_marketing[review_score])", "0.0", 1, "Quality");
NewMeasure("Late Delivery %", "DIVIDE(COUNTROWS(FILTER(fact_marketing, fact_marketing[is_late] = 1)), [Total Orders], 0)", "%", 2, "Quality");
NewMeasure("Repeat Customer %", "DIVIDE(COUNTROWS(FILTER(fact_marketing, fact_marketing[is_repeat_customer] = 1)), [Total Orders], 0)", "%", 2, "Quality");
NewMeasure("Avg Days to Close", "AVERAGE(fact_marketing[days_to_close])", "0.0", 1, "Quality");

// === Counts ===
NewMeasure("Unique Sellers", "COUNTROWS(dim_seller)", "#", 0, "Counts");

// Confirm
Info("Created " + measureTable.Measures.Count + " measures in " + measureTable.Name + " table.");
