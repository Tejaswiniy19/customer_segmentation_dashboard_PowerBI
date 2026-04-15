# Advanced Scenarios & Custom Analysis

## 1. ADVANCED RFM SCENARIOS

### Custom RFM Scoring with Weighted Factors

```dax
WeightedRFMScore = 
    VAR R_Weight = 0.25  -- Recency 25% importance
    VAR F_Weight = 0.35  -- Frequency 35% importance
    VAR M_Weight = 0.40  -- Monetary 40% importance
    VAR WeightedScore = 
        ([RecencyScore] * R_Weight) +
        ([FrequencyScore] * F_Weight) +
        ([MonetaryScore] * M_Weight)
    RETURN
        ROUND(WeightedScore, 2)
```

### Dynamic RFM Thresholds (Quarterly)

```dax
DynamicRecencyThreshold = 
    VAR Q = QUARTER(TODAY())
    RETURN
        SWITCH(Q,
            1, 45,  -- Q1: 45 days
            2, 50,  -- Q2: 50 days
            3, 60,  -- Q3: 60 days
            4, 90,  -- Q4: 90 days (holiday season)
            30
        )
```

### Multi-Channel RFM

```dax
RFMByChannel = 
    VAR CurrentChannel = SELECTEDVALUE(Transactions[Channel])
    VAR ChannelFreq = 
        CALCULATE(
            COUNTA(Transactions[TransactionID]),
            Transactions[Channel] = CurrentChannel
        )
    RETURN
        SWITCH(ChannelFreq,
            0, "Offline Only",
            1-5, "Multi-Channel New",
            6-15, "Multi-Channel Regular",
            "Multi-Channel Heavy"
        )
```

---

## 2. ADVANCED CLV SCENARIOS

### CLV with Customer Acquisition Cost

```dax
CLVWithAcquisitionCost = 
    VAR HistoricalRevenue = [HistoricalCLV]
    VAR AcquisitionCost = 
        SWITCH(
            [ReferralSource],
            "Paid Search", 50,
            "Social Media", 30,
            "Referral", 10,
            "Organic", 5,
            "Online Search", 25,
            40  -- default
        )
    VAR COGS = 
        SUMX(
            RELATEDTABLE(Transactions),
            Transactions[Quantity] * RELATED(Products[CostPrice])
        )
    VAR NetProfit = HistoricalRevenue - COGS
    RETURN
        IF(NetProfit > AcquisitionCost, NetProfit - AcquisitionCost, 0)
```

### Predictive CLV with Seasonality

```dax
PredictiveCLV_Seasonal = 
    VAR CurrentMonth = MONTH(TODAY())
    VAR BaselineCLV = [HistoricalCLV]
    VAR SeasonalFactor = 
        SWITCH(CurrentMonth,
            11, 1.5,  -- November (Black Friday)
            12, 1.8,  -- December (Holiday)
            1, 0.9,   -- January (Post-holiday)
            2, 0.85,  -- February (Slowest)
            3, 1.0,   -- March (Spring recovery)
            1.1       -- Default (10% growth)
        )
    RETURN
        BaselineCLV * SeasonalFactor
```

### CLV Cohort Analysis

```dax
CLVByCohort = 
    VAR JoinMonth = MONTH([JoinDate])
    VAR CustomerAge = DATEDIFF([JoinDate], TODAY(), MONTH)
    RETURN
        IF(
            CustomerAge < 3, "0-3 Months",
            IF(
                CustomerAge < 6, "3-6 Months",
                IF(
                    CustomerAge < 12, "6-12 Months",
                    IF(
                        CustomerAge < 24, "1-2 Years",
                        "2+ Years"
                    )
                )
            )
        )
```

---

## 3. CHURN PREDICTION

### Churn Risk Score

```dax
ChurnRiskScore = 
    VAR DaysSincePurchase = [DaysSinceLastPurchase]
    VAR AvgDaysBetweenPurchase = 
        CALCULATE(
            AVERAGEX(
                SUMMARIZE(
                    Transactions,
                    Transactions[CustomerID],
                    "Interval", 
                    AVERAGE(
                        DATEDIFF([TransactionDate], TODAY(), DAY)
                    )
                ),
                [Interval]
            )
        )
    VAR RiskFactor = 
        IF(
            AvgDaysBetweenPurchase = 0, 0,
            DaysSincePurchase / AvgDaysBetweenPurchase
        )
    RETURN
        ROUND(RiskFactor * 100, 0)
```

### Churn Status Classification

```dax
ChurnStatus = 
    VAR DaysSince = [DaysSinceLastPurchase]
    VAR AvgDays = [AvgDaysBetweenPurchase]
    RETURN
        IF(
            ISBLANK(DaysSince), "New",
            IF(
                DaysSince <= AvgDays * 1.2, "Active",
                IF(
                    DaysSince <= AvgDays * 2, "At Risk",
                    IF(
                        DaysSince <= AvgDays * 3, "Churned",
                        "Dormant"
                    )
                )
            )
        )
```

---

## 4. NET PROMOTER SCORE (NPS) SIMULATION

```dax
NPSBySegment = 
    SWITCH(
        [RFMSegment],
        "Champions", 75-90,
        "Loyal Customers", 60-75,
        "Can't Lose Them", 40-60,
        "Potential Loyalists", 30-50,
        "At Risk - New", 20-40,
        "New or Sleeping", 10-30,
        0
    )
```

---

## 5. MARKET BASKET ANALYSIS

### Product Affinity (which products sell together)

```dax
ProductsPerTransaction = 
    AVERAGE(
        SUMMARIZE(
            Transactions,
            Transactions[TransactionID],
            "Count", COUNTA(Transactions[ProductID])
        )
    )
```

### Cross-Sell Opportunity Score

```dax
CrossSellScore = 
    VAR ProductsOwned = 
        DISTINCTCOUNT(
            FILTER(
                Transactions,
                Transactions[CustomerID] = SELECTEDVALUE(Customers[CustomerID])
            ),
            Transactions[ProductID]
        )
    VAR AvgProductsPerCustomer = 
        AVERAGE(
            SUMMARIZE(
                Transactions,
                Transactions[CustomerID],
                "Count", DISTINCTCOUNT(Transactions[ProductID])
            )
        )
    RETURN
        ROUND(
            (AvgProductsPerCustomer - ProductsOwned) / AvgProductsPerCustomer * 100,
            0
        )
```

---

## 6. CUSTOMER JOURNEY ANALYSIS

### Stage in Lifecycle

```dax
LifecycleStage = 
    VAR Tenure = [CustomerTenure]
    VAR Frequency = [PurchaseCount]
    VAR Recency = [RecencyScore]
    RETURN
        IF(
            Tenure <= 90, "Acquisition",
            IF(
                Frequency <= 2, "Onboarding",
                IF(
                    Recency >= 4, "Active",
                    IF(
                        Recency <= 2, "Churn",
                        "Engagement"
                    )
                )
            )
        )
```

### Lifecycle Revenue Contribution

```dax
LifecycleRevenueContribution = 
    DIVIDE(
        CALCULATE([TotalMonetary], ALL(Customers)),
        SUMX(ALL(Customers), [TotalMonetary])
    ) * 100
```

---

## 7. ADVANCED SEGMENTATION

### Behavioral Segment Matrix

```dax
BehavioralSegment = 
    VAR AOV = [AverageOrderValue]
    VAR Freq = [PurchaseCount]
    VAR AvgAOV = AVERAGE(ALL(Customers), [AverageOrderValue])
    VAR AvgFreq = AVERAGE(ALL(Customers), [PurchaseCount])
    RETURN
        IF(
            AOV > AvgAOV,
            IF(
                Freq > AvgFreq, "Premium High-Frequency",
                "Premium Low-Frequency"
            ),
            IF(
                Freq > AvgFreq, "Budget High-Frequency",
                "Budget Low-Frequency"
            )
        )
```

### Demographic Segment

```dax
DemographicSegment = 
    VAR Age = [Age]
    VAR State = [State]
    RETURN
        IF(
            Age < 30,
            "Young Professional",
            IF(
                Age < 50,
                "Mid-Career",
                "Established"
            )
        ) & " - " &
        SWITCH(
            [State],
            "CA", "Tech Hub",
            "TX", "Growth Market",
            "NY", "Premium Market",
            "Standard"
        )
```

---

## 8. PERFORMANCE METRICS

### Year-over-Year (YoY) Comparison

```dax
YoYRevenue = 
    DIVIDE(
        CALCULATE(
            [TotalMonetary],
            DATEADD(Transactions[TransactionDate], -1, YEAR)
        ),
        [TotalMonetary]
    ) - 1
```

### Month-over-Month (MoM) Growth

```dax
MoMGrowth = 
    DIVIDE(
        [TotalMonetary],
        CALCULATE(
            [TotalMonetary],
            DATEADD(Transactions[TransactionDate], -1, MONTH)
        )
    ) - 1
```

### Customer Growth Rate

```dax
MonthlyCustomerGrowth = 
    DIVIDE(
        [TotalCustomers],
        CALCULATE(
            [TotalCustomers],
            DATEADD(Customers[JoinDate], -1, MONTH)
        )
    ) - 1
```

---

## 9. CUSTOM FILTERS & PARAMETERS

### Field Parameter (for dynamic measures)

```
Create in Power BI:
1. Modeling → New Parameters → Create new parameter
2. Name: "Measure Selection"
3. Add fields: RecencyScore, FrequencyScore, MonetaryScore, TotalMonetary
4. Create corresponding parameter table
5. Use in slicer for dynamic analysis
```

### Top N Dynamic Customers

```dax
TopNCustomers = 
    VAR TopNValue = 10
    VAR Rank = RANKX(
        ALL(Customers),
        [TotalMonetary],
        ,
        DESC
    )
    RETURN
        IF(Rank <= TopNValue, [TotalMonetary], BLANK())
```

---

## 10. DASHBOARD BOOKMARKS

### Recommendation: Create bookmarks for quick navigation

**Bookmark 1: Executive View**
- All pages visible
- No filters
- Summary focus

**Bookmark 2: RFM Deep Dive**
- RFM page shown
- At Risk segments filtered
- Drill-down enabled

**Bookmark 3: High-Value Focus**
- CLV page shown
- Tier 1-2 filtered
- Profitability view

**Bookmark 4: At-Risk Alert**
- RFM page shown
- At-Risk segments highlighted
- Red color scheme
- Action items visible

---

## 11. DATA QUALITY & VALIDATION

### Audit Columns

```dax
DataQualityScore = 
    VAR HasPhone = IF(ISBLANK(Customers[Phone]), 0, 1)
    VAR HasEmail = IF(ISBLANK(Customers[Email]), 0, 1)
    VAR HasAddress = IF(ISBLANK(Customers[Address]), 0, 1)
    VAR HasTrans = IF([PurchaseCount] > 0, 1, 0)
    RETURN
        (HasPhone + HasEmail + HasAddress + HasTrans) / 4 * 100
```

### Missing Data Alert

```dax
DataCompleteness = 
    IF(
        OR(
            ISBLANK(Customers[Phone]),
            ISBLANK(Customers[Email]),
            ISBLANK(Customers[Address])
        ),
        "Incomplete",
        "Complete"
    )
```

---

## 12. INTEGRATION EXAMPLES

### Power Query M Query (in Power BI)

```m
// Add calculated column for age from DateOfBirth
let
    Source = Customers,
    AddedAge = Table.AddColumn(Source, "Age", 
        each Date.Year(DateTime.LocalNow()) - Date.Year([DateOfBirth]), 
        Int64.Type)
in
    AddedAge
```

### Excel Integration Formula

```excel
=POWER_BI_MEASURE("RFMSegment", "Champions")
```

---

## RECOMMENDATIONS MATRIX

Create recommendations based on segment:

```dax
SegmentRecommendation = 
    SWITCH(
        [RFMSegment],
        "Champions", "🏆 VIP Program: Exclusive benefits, early access to new products",
        "Loyal Customers", "⭐ Upsell: Recommend premium products, cross-sell opportunities",
        "Can't Lose Them", "🔄 Win-Back: Special offers, limited-time discounts",
        "At Risk - New", "👋 Onboarding: Welcome series, first repeat incentive",
        "At Risk - Lost", "🚨 Emergency: Aggressive campaigns, understand reason for departure",
        "About to Sleep", "⏰ Re-engagement: Exclusive offers, survey for feedback",
        "Potential Loyalists", "💡 Growth: Cross-sell, loyalty program enrollment",
        "New or Sleeping", "🌟 Welcome: First purchase follow-up, product recommendations",
        "Standard marketing"
    )
```

---

**Advanced Scenarios Version**: 1.0  
**Last Updated**: April 2026
