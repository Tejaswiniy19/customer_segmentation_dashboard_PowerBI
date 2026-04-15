# Customer Lifetime Value (CLV) - DAX Formulas

## Overview
Customer Lifetime Value represents the total revenue a business can expect from a customer during their entire relationship.

---

## 1. BASIC CLV CALCULATION

### Historical CLV (Actual)
```dax
HistoricalCLV = 
    [TotalMonetary]
```

### Average Purchase Frequency (Monthly)
```dax
AvgPurchaseFrequencyMonthly = 
    VAR FirstPurchaseDate = MIN ( Transactions[TransactionDate] )
    VAR LastPurchaseDate = MAX ( Transactions[TransactionDate] )
    VAR MonthsActive = 
        INT (
            ( LastPurchaseDate - FirstPurchaseDate ) / 30
        ) + 1
    VAR PurchaseCount = [PurchaseCount]
    RETURN
        IF (
            OR ( ISBLANK ( FirstPurchaseDate ), MonthsActive = 0 ),
            0,
            PurchaseCount / MonthsActive
        )
```

### Average Order Value (AOV)
```dax
AvgOrderValue = 
    IF (
        [PurchaseCount] = 0,
        0,
        [TotalMonetary] / [PurchaseCount]
    )
```

### Customer Tenure (Days)
```dax
CustomerTenure = 
    VAR FirstPurchaseDate = MIN ( Transactions[TransactionDate] )
    VAR MaxDate = MAX ( ALL ( Transactions[TransactionDate] ) )
    RETURN
        IF (
            ISBLANK ( FirstPurchaseDate ),
            0,
            MaxDate - FirstPurchaseDate
        )
```

---

## 2. PREDICTIVE CLV (Next 12 Months)

### Predicted CLV (Conservative Approach)
```dax
PredictedCLV_12Months = 
    VAR AvgFreqMonthly = [AvgPurchaseFrequencyMonthly]
    VAR AOV = [AvgOrderValue]
    VAR Months = 12
    RETURN
        IF (
            OR ( ISBLANK ( AvgFreqMonthly ), ISBLANK ( AOV ) ),
            0,
            AvgFreqMonthly * AOV * Months
        )
```

### Predicted CLV (With Retention Rate)
```dax
PredictedCLV_Adjusted = 
    VAR HistoricalCLV = [HistoricalCLV]
    VAR RecencyScore = [RecencyScore]
    VAR RetentionMultiplier = 
        SWITCH (
            RecencyScore,
            5, 1.2,   -- Recent customers: 20% growth
            4, 1.0,   -- Regular customers: maintain
            3, 0.8,   -- Declining customers: 20% decrease
            2, 0.5,   -- At-risk customers: 50% decrease
            1, 0.2,   -- Dormant customers: 80% decrease
            0
        )
    RETURN
        HistoricalCLV * RetentionMultiplier
```

---

## 3. CLV SEGMENT CLASSIFICATION

### CLV Tier
```dax
CLVTier = 
    VAR CLV = [HistoricalCLV]
    VAR P75 = PERCENTILE.INC ( ALL ( Customers[CustomerID] ), [HistoricalCLV], 0.75 )
    VAR P50 = PERCENTILE.INC ( ALL ( Customers[CustomerID] ), [HistoricalCLV], 0.50 )
    VAR P25 = PERCENTILE.INC ( ALL ( Customers[CustomerID] ), [HistoricalCLV], 0.25 )
    RETURN
        IF (
            ISBLANK ( CLV ),
            "Unknown",
            IF (
                CLV >= P75,
                "Tier 1 - High Value",
                IF (
                    CLV >= P50,
                    "Tier 2 - Medium-High",
                    IF (
                        CLV >= P25,
                        "Tier 3 - Medium-Low",
                        "Tier 4 - Low Value"
                    )
                )
            )
        )
```

### CLV Potential Score
```dax
CLVPotentialScore = 
    VAR CurrentCLV = [HistoricalCLV]
    VAR PredictedCLV = [PredictedCLV_Adjusted]
    VAR PotentialGrowth = 
        IF (
            CurrentCLV = 0,
            0,
            ( PredictedCLV - CurrentCLV ) / CurrentCLV
        )
    RETURN
        IF (
            PotentialGrowth < 0, "Declining",
            IF (
                PotentialGrowth < 0.1, "Stable",
                IF (
                    PotentialGrowth < 0.25, "Moderate Growth",
                    "High Growth Potential"
                )
            )
        )
```

---

## 4. ADVANCED CLV METRICS

### Customer Profit Margin
```dax
CustomerProfitMargin = 
    VAR TotalRevenue = [TotalMonetary]
    VAR TotalCost = 
        SUMX (
            Transactions,
            Transactions[Quantity] * RELATED ( Products[CostPrice] )
        )
    RETURN
        IF (
            TotalRevenue = 0,
            0,
            ( TotalRevenue - TotalCost ) / TotalRevenue
        )
```

### Gross Profit (Customer)
```dax
CustomerGrossProfit = 
    VAR TotalRevenue = [TotalMonetary]
    VAR TotalCost = 
        SUMX (
            Transactions,
            Transactions[Quantity] * RELATED ( Products[CostPrice] )
        )
    RETURN
        TotalRevenue - TotalCost
```

### Return on Customer (ROC)
```dax
ReturnOnCustomer = 
    VAR Profit = [CustomerGrossProfit]
    VAR AcquisitionCost = 50  -- Assumed value; adjust as needed
    RETURN
        IF (
            AcquisitionCost = 0,
            0,
            Profit / AcquisitionCost
        )
```

---

## 5. CLV BY DEMOGRAPHICS

### CLV by Age Group
```dax
CLVByAgeGroup = 
    VAR SelectedAgeGroup = SELECTEDVALUE ( Customers[AgeGroup] )
    RETURN
        CALCULATE (
            [HistoricalCLV],
            Customers[AgeGroup] = SelectedAgeGroup
        )
```

### CLV by Location
```dax
CLVByLocation = 
    VAR SelectedCity = SELECTEDVALUE ( Customers[City] )
    RETURN
        CALCULATE (
            [HistoricalCLV],
            Customers[City] = SelectedCity
        )
```

### CLV by Channel
```dax
CLVByChannel = 
    VAR SelectedChannel = SELECTEDVALUE ( Transactions[Channel] )
    RETURN
        CALCULATE (
            [HistoricalCLV],
            Transactions[Channel] = SelectedChannel
        )
```

---

## 6. SUMMARY METRICS

### Total CLV (All Customers)
```dax
TotalCLV = 
    SUMX (
        ALL ( Customers ),
        [HistoricalCLV]
    )
```

### Average CLV per Customer
```dax
AvgCLV = 
    AVERAGEX (
        SUMMARIZE ( Customers, Customers[CustomerID] ),
        [HistoricalCLV]
    )
```

### Median CLV
```dax
MedianCLV = 
    PERCENTILE.INC (
        ALL ( Customers[CustomerID] ),
        [HistoricalCLV],
        0.5
    )
```

### CLV Distribution
```dax
CLV_DistributionPercentage = 
    DIVIDE (
        [TotalCLV],
        CALCULATE ( [TotalCLV], ALL ( Customers ) ) * 100
    )
```

---

## 7. BENCHMARKING

### CLV vs Average
```dax
CLVvsAverage = 
    DIVIDE (
        [HistoricalCLV],
        [AvgCLV]
    )
```

### Percentile Rank
```dax
CLVPercentileRank = 
    PERCENTRANK.INC (
        ALL ( Customers[CustomerID] ),
        [HistoricalCLV]
    )
```
