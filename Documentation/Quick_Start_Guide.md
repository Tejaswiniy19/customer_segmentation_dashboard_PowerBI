# 🚀 Customer Segmentation Dashboard - Quick Start Guide

## ⚡ 15-Minute Setup Process

### Step 1: Open Power BI Desktop (2 minutes)
1. Launch Power BI Desktop
2. Create new blank report
3. Save as `Customer_Segmentation_Dashboard.pbix` in your BI2 folder

### Step 2: Import Data (3 minutes)
1. Click **"Get Data"** → **"Text/CSV"**
2. Import all three CSV files:
   - `Data/Customers.csv`
   - `Data/Products.csv`
   - `Data/Transactions.csv`
3. Click **"Load"** (don't transform yet)

### Step 3: Create Data Model (2 minutes)
1. Go to **Model** view (bottom left)
2. Create relationships:
   - Customers[CustomerID] ↔ Transactions[CustomerID]
   - Products[ProductID] ↔ Transactions[ProductID]
3. Set both relationships to **"Both"** cross-filter direction

### Step 4: Copy Essential DAX Measures (5 minutes)
1. Open `DAX Formulas/Complete_DAX_Measures.txt`
2. Copy and paste these measures into Power BI:

#### Required Measures (Copy these first):
```dax
// Basic Metrics
TotalRevenue = SUM(Transactions[TotalAmount])
TransactionCount = COUNTROWS(Transactions)
UniqueCustomers = DISTINCTCOUNT(Transactions[CustomerID])
AverageOrderValue = DIVIDE([TotalRevenue], [TransactionCount])

// RFM Analysis
DaysSinceLastPurchase =
VAR LastPurchase = MAXX(
    FILTER(Transactions, Transactions[CustomerID] = MAX(Customers[CustomerID])),
    Transactions[TransactionDate]
)
VAR Today = MAX(Transactions[TransactionDate])
RETURN IF(ISBLANK(LastPurchase), BLANK(), Today - LastPurchase)

RecencyScore = IF(ISBLANK([DaysSinceLastPurchase]), 1,
    IF([DaysSinceLastPurchase] <= 30, 5,
    IF([DaysSinceLastPurchase] <= 60, 4,
    IF([DaysSinceLastPurchase] <= 90, 3,
    IF([DaysSinceLastPurchase] <= 180, 2, 1)))))

PurchaseCount = COUNTROWS(Transactions)

FrequencyScore =
VAR Freq = [PurchaseCount]
VAR AvgFreq = AVERAGEX(ALL(Customers), [PurchaseCount])
RETURN IF(ISBLANK(Freq), 1,
    IF(Freq >= AvgFreq * 2, 5,
    IF(Freq >= AvgFreq * 1.5, 4,
    IF(Freq >= AvgFreq, 3,
    IF(Freq >= AvgFreq * 0.5, 2, 1)))))

TotalMonetary = SUM(Transactions[TotalAmount])

MonetaryScore =
VAR Monetary = [TotalMonetary]
VAR AvgMonetary = AVERAGEX(ALL(Customers), [TotalMonetary])
RETURN IF(ISBLANK(Monetary), 1,
    IF(Monetary >= AvgMonetary * 2, 5,
    IF(Monetary >= AvgMonetary * 1.5, 4,
    IF(Monetary >= AvgMonetary, 3,
    IF(Monetary >= AvgMonetary * 0.5, 2, 1)))))

RFMScore = [RecencyScore] * 100 + [FrequencyScore] * 10 + [MonetaryScore]

CustomerSegment = IF([RFMScore] >= 555, "Champions",
    IF([RFMScore] >= 445, "Loyal Customers",
    IF([RFMScore] >= 334, "Potential Loyalists",
    IF([RFMScore] >= 223, "Promising",
    IF([RFMScore] >= 112, "Needs Attention", "At Risk")))))
```

### Step 5: Create Your First Visualization (3 minutes)
1. Go to **Report** view
2. Add a **Donut Chart**:
   - **Values**: CustomerSegment (Count)
   - **Legend**: CustomerSegment
3. Rename page to "Executive Summary"

### Step 6: Add Key Metrics Cards (2 minutes)
1. Add 4 **Card** visuals:
   - Total Revenue
   - Unique Customers
   - Average Order Value
   - Transaction Count
2. Format cards with currency/number formatting

### Step 7: Add Filters (2 minutes)
1. Add **Slicer** visuals for:
   - Customers[AgeGroup]
   - Customers[State]
   - Transactions[Channel]
2. Arrange at top of page

---

## 🎯 What You'll Have After 15 Minutes

✅ **Working Dashboard** with:
- RFM customer segmentation
- Key performance metrics
- Interactive filters
- Professional visualization

✅ **Data Model** properly configured
✅ **Essential DAX measures** implemented
✅ **Interactive filtering** by demographics and channels

---

## 🚀 Next Steps (Optional Advanced Features)

### Add More Pages (15 minutes each):
1. **RFM Analysis Page**: Scatter plot with RFM scores
2. **CLV Analysis Page**: Customer lifetime value insights
3. **Geographic Page**: Map visualization
4. **Channel Analysis Page**: Channel performance breakdown

### Advanced Features (30 minutes):
1. **Drillthrough**: Click segments to see customer details
2. **Custom Tooltips**: Enhanced hover information
3. **Conditional Formatting**: Color-code based on performance
4. **Time Intelligence**: Month-over-month growth analysis

---

## 📊 Expected Results

After completing the quick start, you'll have:

- **6 Customer Segments**: Champions, Loyal, Potential, Promising, Needs Attention, At Risk
- **Revenue Insights**: Total $45K+ across 1,200+ customers
- **Behavioral Analysis**: Purchase patterns and frequency
- **Interactive Filters**: By age, location, and channel
- **Professional Dashboard**: Ready for business presentations

---

## 🔧 Troubleshooting

### Common Issues:
1. **Relationships not working**: Check data types match (CustomerID should be text)
2. **Blank RFM scores**: Ensure TransactionDate is Date type
3. **Performance slow**: Add indexes to large tables or use summarized tables

### Data Quality Checks:
1. Verify all CustomerIDs exist in both tables
2. Check for null values in key columns
3. Ensure dates are in correct format

---

## 📈 Dashboard Impact

This dashboard will help you:
- **Identify** high-value customers (Champions segment)
- **Target** marketing efforts to at-risk customers
- **Optimize** channel strategies based on performance
- **Predict** customer lifetime value
- **Segment** customers for personalized campaigns

**Ready to start? Open Power BI Desktop and follow the 15-minute guide above!**
    VAR F = [FrequencyScore]
    VAR M = [MonetaryScore]
    RETURN
        IF(AND(R >= 4, F >= 4, M >= 4), "Champions",
        IF(AND(R >= 4, F >= 3, M >= 3), "Loyal Customers",
        IF(AND(R >= 3, F >= 4, M >= 4), "Can't Lose Them",
        IF(AND(R >= 4, F = 1, M >= 1), "At Risk - New",
        IF(AND(R <= 2, F >= 3, M >= 3), "At Risk - Lost",
        IF(AND(R <= 2, F >= 4, M >= 4), "About to Sleep",
        IF(AND(M >= 4, F >= 1), "Potential Loyalists",
        IF(AND(R <= 3, F = 1, M <= 2), "New or Sleeping", "General"))))))))
```

### Most Important CLV Formulas

#### CLV Basics
```dax
HistoricalCLV = SUM(Transactions[TotalAmount])

PurchaseCount = COUNTA(Transactions[TransactionID])

AverageOrderValue = IF([PurchaseCount] = 0, 0, [HistoricalCLV] / [PurchaseCount])

CustomerTenure = IF(ISBLANK(FirstPurchaseDate), 0, MaxDate - FirstPurchaseDate)
```

#### CLV Tier
```dax
CLVTier = 
    VAR CLV = [HistoricalCLV]
    VAR P75 = PERCENTILE.INC(ALL(Customers[CustomerID]), [HistoricalCLV], 0.75)
    VAR P50 = PERCENTILE.INC(ALL(Customers[CustomerID]), [HistoricalCLV], 0.50)
    VAR P25 = PERCENTILE.INC(ALL(Customers[CustomerID]), [HistoricalCLV], 0.25)
    RETURN
        IF(ISBLANK(CLV), "Unknown",
        IF(CLV >= P75, "Tier 1 - High Value",
        IF(CLV >= P50, "Tier 2 - Medium-High",
        IF(CLV >= P25, "Tier 3 - Medium-Low", "Tier 4 - Low Value"))))
```

---

## 📈 DASHBOARD PAGES - QUICK BUILD

### Page 1: Executive Summary (10 minutes)
1. **Cards**: Total Customers, Total Revenue, Avg CLV, # Transactions
2. **Pie Chart**: Count of Customers by RFMSegment
3. **Bar Chart**: Sum of TotalMonetary by CLVTier
4. **Table**: Top 10 Customers by Revenue

### Page 2: RFM Analysis (15 minutes)
1. **Bubble Chart** (MUST HAVE):
   - X-Axis: RecencyScore
   - Y-Axis: FrequencyScore
   - Size: Sum(TotalMonetary)
   - Color: RFMSegment
   - Tooltip: CustomerName, RFMSegment, Score

2. **Matrix Table**:
   - Rows: RFMSegment
   - Columns: Count, Sum(Monetary), Avg Frequency

3. **Donut Chart**: Count of Customers by RFMSegment

### Page 3: CLV Analysis (15 minutes)
1. **Column Chart**: Sum(TotalMonetary) by CLVTier
2. **Scatter**: PurchaseCount vs TotalMonetary (colored by RFMSegment)
3. **Table**: Customer, CLV, Profit, ROI, CLVTier

### Page 4: Demographics (10 minutes)
1. **Column Chart**: Sum(TotalMonetary) by AgeGroup
2. **Map/Table**: Revenue by City/State
3. **Bar Chart**: Count by Channel
4. **Pie**: Gender Distribution

### Page 5: Trends (10 minutes)
1. **Line Chart**: Sum(TotalAmount) by Month(TransactionDate)
2. **Area Chart**: Cumulative Count of Customers
3. **Stacked Column**: Sum by Month and Category

### Page 6: Customer Detail (5 minutes)
1. **Filter**: CustomerName (optional)
2. **Cards**: Basic customer info
3. **Table**: Transaction history
4. **Text Box**: Segment recommendation

---

## 🎨 FORMATTING TIPS

### Color Scheme (Professional)
- **Champions**: Dark Green (#107C10)
- **Loyal Customers**: Light Green (#70AD47)
- **Can't Lose Them**: Orange (#FF8C00)
- **At Risk**: Red (#E74C3C)
- **Potential/New**: Blue (#4472C4)

### Layout Best Practices
- 1 main chart per section (focus)
- Supporting metrics in cards
- Filter at top of page
- Summary metrics on left
- Details on right

### Font & Size
- Title: 16-18pt, Bold
- Subtitle: 12-14pt, Regular
- Labels: 10-11pt, Regular
- Axis labels: 9-10pt

---

## ⚡ COMMON MISTAKES TO AVOID

| Mistake | Solution |
|---------|----------|
| Calculating RFM on individual transactions instead of per customer | Create RFM measures on Customer level, not Transaction level |
| Including "Unknown" values in segment calculations | Add BLANK() or filter out NULL records |
| Not establishing relationships | Must have proper relationships for RELATED() to work |
| Forgetting ALL() in aggregations | Use ALL() when calculating percentiles or totals |
| Slow performance on large datasets | Hide unused columns, create aggregations |
| Wrong date baseline for Recency | Use MAX(ALL Transactions) as reference date |

---

## 🧪 TESTING CHECKLIST

Before publishing:

- [ ] **Data Validation**
  - [ ] Total transactions = 40
  - [ ] Total customers = 20
  - [ ] No blank RFM scores
  - [ ] Sum of CLV > 0

- [ ] **Calculations**
  - [ ] RecencyScore ranges 1-5
  - [ ] FrequencyScore ranges 1-5
  - [ ] MonetaryScore ranges 1-5
  - [ ] All segments populated
  - [ ] CLV Tiers have data

- [ ] **Visuals**
  - [ ] All charts display data
  - [ ] Slicers interact correctly
  - [ ] Drill-through works (if used)
  - [ ] Tooltips appear
  - [ ] Colors are consistent

- [ ] **Performance**
  - [ ] Dashboard loads < 3 seconds
  - [ ] Slicers respond < 1 second
  - [ ] Sorting works smoothly
  - [ ] No error messages

---

## 🚨 TROUBLESHOOTING

### Problem: RFM Scores all showing 1
**Solution**: Check that RecencyScore, FrequencyScore, MonetaryScore are creating scores 1-5 correctly. Verify helper columns exist.

### Problem: Blank segments
**Solution**: Add error handling using IFERROR() or IF(ISBLANK()) in formulas.

### Problem: Sales not matching
**Solution**: Check relationships are correct. Verify no data type mismatches (CustomerID should be same type in both tables).

### Problem: Slow dashboards
**Solution**: 
- Remove duplicate slicers
- Hide unused columns
- Update to latest Power BI version
- Consider aggregations for 100K+ rows

### Problem: Slicers not filtering
**Solution**: 
- Check visual level filters are configured
- Verify measure uses correct context
- Confirm relationship cardinality is correct

---

## 📞 HELP RESOURCES

### Reference Files
1. **Project_Overview.md** - Business context and segment definitions
2. **RFM_Calculations.md** - All RFM formula details
3. **CLV_Calculations.md** - All CLV formula details
4. **Dashboard_Setup_Guide.md** - Complete step-by-step guide

### Quick Links
- Power BI Documentation: www.docs.microsoft.com/power-bi
- DAX Function Reference: www.dax.guide
- Online Community: www.pbicommunity.com

---

## 📋 NEXT STEPS

### Once Dashboard is Complete:
1. ✓ Test with your actual data
2. ✓ Enable auto-refresh schedule
3. ✓ Publish to Power BI Service
4. ✓ Share with stakeholders
5. ✓ Gather feedback
6. ✓ Iterate and improve

### Month 1 Enhancements:
- [ ] Add field parameters for flexible selection
- [ ] Implement bookmarks for different views
- [ ] Create mobile-optimized version
- [ ] Set up alerts for critical segments

### Month 2+ Features:
- [ ] Machine learning predictions
- [ ] Automated email campaigns
- [ ] CRM integration
- [ ] Real-time data feeds

---

## ✅ SUCCESS CRITERIA

Dashboard is ready for production when:

✓ All RFM segments have customers assigned  
✓ CLV calculations validated against sample data  
✓ All 6 pages load without errors  
✓ Slicers work cross-page  
✓ Color scheme is consistent  
✓ No #Error values visible  
✓ Performance meets standards  
✓ Users find insights actionable  

---

**Version**: 1.0  
**Last Updated**: April 2026  
**Status**: Ready to Use ✓
