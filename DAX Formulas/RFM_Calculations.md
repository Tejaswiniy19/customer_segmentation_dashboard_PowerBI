# RFM Analysis - DAX Formulas

## Overview
RFM stands for Recency, Frequency, and Monetary value. These three metrics help segment customers based on their purchasing behavior.

---

## 1. RECENCY - Days Since Last Purchase

### Days Since Last Purchase (RFM Table)
```dax
DaysSinceLastPurchase = 
    VAR LastTransactionDate = MAX ( Transactions[TransactionDate] )
    VAR MaxDate = MAX ( ALL ( Transactions[TransactionDate] ) )
    RETURN
        IF (
            ISBLANK ( LastTransactionDate ),
            BLANK (),
            MaxDate - LastTransactionDate
        )
```

### Recency Score (1-5 scale, where 1 = longest ago, 5 = most recent)
```dax
RecencyScore = 
    VAR DaysSinceLast = [DaysSinceLastPurchase]
    VAR MaxDays = MAXX ( ALL ( Customers ), [DaysSinceLastPurchase] )
    RETURN
        IF (
            ISBLANK ( DaysSinceLast ),
            1,
            INT (
                5 - ( DaysSinceLast / MaxDays ) * 4
            )
        )
```

**Better Version (Using Percentiles):**
```dax
RecencyScore = 
    VAR DaysSinceLast = [DaysSinceLastPurchase]
    RETURN
        IF (
            ISBLANK ( DaysSinceLast ),
            1,
            IF (
                DaysSinceLast <= 30, 5,
                IF ( DaysSinceLast <= 60, 4,
                IF ( DaysSinceLast <= 90, 3,
                IF ( DaysSinceLast <= 180, 2, 1 )
                )
                )
            )
        )
```

---

## 2. FREQUENCY - Number of Purchases

### Purchase Count (Customer Level)
```dax
PurchaseCount = 
    COUNTA ( Transactions[TransactionID] )
```

### Frequency Score (1-5 scale)
```dax
FrequencyScore = 
    VAR PurchaseFreq = [PurchaseCount]
    VAR AvgFreq = AVERAGE ( 
        CALCULATETABLE ( 
            SUMMARIZE ( Transactions, Customers[CustomerID], "Count", COUNTA ( Transactions[TransactionID] ) ),
            ALL ( Transactions )
        )
    )
    RETURN
        IF (
            ISBLANK ( PurchaseFreq ),
            1,
            IF (
                PurchaseFreq <= 1, 1,
                IF ( PurchaseFreq <= 2, 2,
                IF ( PurchaseFreq <= 4, 3,
                IF ( PurchaseFreq <= 7, 4, 5 )
                )
                )
            )
        )
```

---

## 3. MONETARY - Total Spending

### Total Amount Spent
```dax
TotalMonetary = 
    SUM ( Transactions[TotalAmount] )
```

### Average Order Value
```dax
AverageOrderValue = 
    IF (
        [PurchaseCount] = 0,
        0,
        [TotalMonetary] / [PurchaseCount]
    )
```

### Monetary Score (1-5 scale)
```dax
MonetaryScore = 
    VAR TotalSpent = [TotalMonetary]
    VAR AvgMonetary = AVERAGE (
        CALCULATETABLE (
            SUMMARIZE ( Transactions, Customers[CustomerID], "Total", SUM ( Transactions[TotalAmount] ) ),
            ALL ( Transactions )
        )
    )
    RETURN
        IF (
            ISBLANK ( TotalSpent ),
            1,
            IF (
                TotalSpent <= 100, 1,
                IF ( TotalSpent <= 300, 2,
                IF ( TotalSpent <= 700, 3,
                IF ( TotalSpent <= 1500, 4, 5 )
                )
                )
            )
        )
```

---

## 4. RFM SEGMENT CLASSIFICATION

### RFM Combined Score
```dax
RFMScore = 
    [RecencyScore] & [FrequencyScore] & [MonetaryScore]
```

### RFM Segment
```dax
RFMSegment = 
    VAR R = [RecencyScore]
    VAR F = [FrequencyScore]
    VAR M = [MonetaryScore]
    RETURN
        IF (
            OR ( ISBLANK ( R ), ISBLANK ( F ), ISBLANK ( M ) ),
            "Unknown",
            IF (
                AND ( R >= 4, F >= 4, M >= 4 ),
                "Champions",
                IF (
                    AND ( R >= 4, F >= 3, M >= 3 ),
                    "Loyal Customers",
                    IF (
                        AND ( R >= 3, F >= 4, M >= 4 ),
                        "Can't Lose Them",
                        IF (
                            AND ( R >= 4, F = 1, M >= 1 ),
                            "At Risk - New",
                            IF (
                                AND ( R <= 2, F >= 3, M >= 3 ),
                                "At Risk - Lost",
                                IF (
                                    AND ( R <= 2, F >= 4, M >= 4 ),
                                    "About to Sleep",
                                    IF (
                                        AND ( M >= 4, F >= 1 ),
                                        "Potential Loyalists",
                                        IF (
                                            AND ( R <= 3, F = 1, M <= 2 ),
                                            "New or Sleeping",
                                            "General"
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
```

---

## 5. SEGMENT DESCRIPTIONS

| Segment | Criteria | Strategy |
|---------|----------|----------|
| **Champions** | R≥4, F≥4, M≥4 | Reward loyalty, early access to new products, VIP treatment |
| **Loyal Customers** | R≥4, F≥3, M≥3 | Up-sell premium products, personalized offers |
| **Can't Lose Them** | R≥3, F≥4, M≥4 | Win-back campaigns, special offers to reactivate |
| **At Risk - New** | R≥4, F=1, M≥1 | Onboarding campaigns, encourage repeat purchase |
| **At Risk - Lost** | R≤2, F≥3, M≥3 | Win-back campaigns, special discounts |
| **About to Sleep** | R≤2, F≥4, M≥4 | Re-engagement campaigns, exclusive offers |
| **Potential Loyalists** | M≥4, F≥1 | Cross-sell, encourage repeat purchase |
| **New or Sleeping** | R≤3, F=1, M≤2 | Welcome campaigns, first purchase incentive |
| **General** | Others | Standard marketing campaigns |
