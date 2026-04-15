# Customer Segmentation Dashboard - Complete Setup Guide

## 📋 Complete Process Overview

### Phase 1: Power BI Desktop Setup
### Phase 2: Data Import & Modeling
### Phase 3: DAX Measures Creation
### Phase 4: Dashboard Development
### Phase 5: Advanced Features & Testing

---

## Phase 1: Power BI Desktop Setup

### Step 1.1: Launch Power BI Desktop
1. Open Power BI Desktop application
2. Create a new blank report
3. Save the file as `Customer_Segmentation_Dashboard.pbix` in your BI2 folder

### Step 1.2: Set Theme & Page Setup
1. Go to View → Themes → Import theme
2. Choose a professional theme (Corporate or Executive)
3. Set page size to 16:9 ratio
4. Rename Page 1 to "Executive Summary"

---

## Phase 2: Data Import & Modeling

### Step 2.1: Import CSV Files
1. Click "Get Data" → "Text/CSV"
2. Import each CSV file:
   - `Data/Customers.csv`
   - `Data/Products.csv`
   - `Data/Transactions.csv`

### Step 2.2: Data Cleaning & Transformation
1. **Customers Table:**
   - Change DateOfBirth and JoinDate to Date format
   - Create Age column: `=Date.From(DateTime.LocalNow()) - [DateOfBirth]`
   - Extract age in years: `=Number.From([Age])/365.25`

2. **Transactions Table:**
   - Ensure TransactionDate is Date format
   - Verify numeric columns (Quantity, UnitPrice, TotalAmount)

3. **Products Table:**
   - Ensure UnitPrice and CostPrice are numeric

### Step 2.3: Create Data Model Relationships
1. Create relationships:
   - Customers[CustomerID] → Transactions[CustomerID] (One-to-Many)
   - Products[ProductID] → Transactions[ProductID] (One-to-Many)

2. Set cross-filter direction to "Both" for all relationships

---

## Phase 3: DAX Measures Creation

### Step 3.1: Basic Measures (Transactions Table)

```dax
// Transaction Metrics
TotalRevenue = SUM(Transactions[TotalAmount])

TotalQuantity = SUM(Transactions[Quantity])

TransactionCount = COUNTROWS(Transactions)

AverageOrderValue = [TotalRevenue] / [TransactionCount]

// Customer Metrics
UniqueCustomers = DISTINCTCOUNT(Transactions[CustomerID])

AverageRevenuePerCustomer = [TotalRevenue] / [UniqueCustomers]
```

### Step 3.2: RFM Analysis Measures

```dax
// Recency Measures
DaysSinceLastPurchase =
VAR LastPurchase = MAXX(
    FILTER(
        Transactions,
        Transactions[CustomerID] = MAX(Customers[CustomerID])
    ),
    Transactions[TransactionDate]
)
VAR Today = MAX(Transactions[TransactionDate])
RETURN
    IF(ISBLANK(LastPurchase), BLANK(), Today - LastPurchase)

RecencyScore =
VAR Days = [DaysSinceLastPurchase]
RETURN
    IF(ISBLANK(Days), 1,
        IF(Days <= 30, 5,
        IF(Days <= 60, 4,
        IF(Days <= 90, 3,
        IF(Days <= 180, 2, 1)))))

// Frequency Measures
PurchaseCount = COUNTROWS(Transactions)

FrequencyScore =
VAR Freq = [PurchaseCount]
VAR AvgFreq = AVERAGEX(ALL(Customers), [PurchaseCount])
RETURN
    IF(ISBLANK(Freq), 1,
        IF(Freq >= AvgFreq * 2, 5,
        IF(Freq >= AvgFreq * 1.5, 4,
        IF(Freq >= AvgFreq, 3,
        IF(Freq >= AvgFreq * 0.5, 2, 1)))))

// Monetary Measures
TotalMonetary = SUM(Transactions[TotalAmount])

MonetaryScore =
VAR Monetary = [TotalMonetary]
VAR AvgMonetary = AVERAGEX(ALL(Customers), [TotalMonetary])
RETURN
    IF(ISBLANK(Monetary), 1,
        IF(Monetary >= AvgMonetary * 2, 5,
        IF(Monetary >= AvgMonetary * 1.5, 4,
        IF(Monetary >= AvgMonetary, 3,
        IF(Monetary >= AvgMonetary * 0.5, 2, 1)))))
```

### Step 3.3: RFM Segmentation

```dax
// RFM Score Combination
RFMScore = [RecencyScore] * 100 + [FrequencyScore] * 10 + [MonetaryScore]

// Customer Segment Classification
CustomerSegment =
VAR Score = [RFMScore]
RETURN
    IF(Score >= 555, "Champions",
    IF(Score >= 445, "Loyal Customers",
    IF(Score >= 334, "Potential Loyalists",
    IF(Score >= 223, "Promising",
    IF(Score >= 112, "Needs Attention",
    "At Risk")))))
```

### Step 3.4: CLV Calculations

```dax
// Customer Lifetime Value
CustomerLifetimeValue = [TotalMonetary]

AvgOrderValue = [TotalMonetary] / [PurchaseCount]

PurchaseFrequency =
VAR FirstPurchase = MINX(
    FILTER(Transactions, Transactions[CustomerID] = MAX(Customers[CustomerID])),
    Transactions[TransactionDate]
)
VAR LastPurchase = MAXX(
    FILTER(Transactions, Transactions[CustomerID] = MAX(Customers[CustomerID])),
    Transactions[TransactionDate]
)
VAR DaysActive = LastPurchase - FirstPurchase
RETURN
    IF(DaysActive = 0, 0, [PurchaseCount] / (DaysActive / 30))

PredictedCLV =
VAR AOV = [AvgOrderValue]
VAR Frequency = [PurchaseFrequency]
VAR Tenure = 12  // Assumed 12 months average customer lifespan
RETURN
    AOV * Frequency * Tenure
```

### Step 3.5: Demographic Analysis

```dax
// Age Group Analysis
AgeGroupRevenue = [TotalRevenue]

AgeGroupCount = DISTINCTCOUNT(Customers[CustomerID])

AvgRevenueByAge = [AgeGroupRevenue] / [AgeGroupCount]

// Geographic Analysis
RevenueByCity = [TotalRevenue]

RevenueByState = [TotalRevenue]

CustomerCountByLocation = DISTINCTCOUNT(Customers[CustomerID])

// Channel Analysis
RevenueByChannel = [TotalRevenue]

OrdersByChannel = [TransactionCount]

AvgOrderByChannel = [RevenueByChannel] / [OrdersByChannel]
```

---

## Phase 4: Dashboard Development

### Step 4.1: Create Executive Summary Page

#### Key Metrics Cards (Top Row):
1. Total Revenue Card
2. Total Customers Card
3. Average Order Value Card
4. Total Transactions Card

#### RFM Segmentation Chart (Middle):
- Donut Chart: Customer Segments
- Use CustomerSegment as Legend
- Count of customers as Values

#### Revenue Trends (Bottom):
- Line Chart: Revenue by Month
- X-axis: Month-Year
- Y-axis: Total Revenue

### Step 4.2: Create RFM Analysis Page

#### RFM Scatter Plot:
- X-axis: Frequency Score
- Y-axis: Monetary Score
- Bubble Size: Recency Score
- Color: Customer Segment

#### RFM Score Distribution:
- Bar Chart: Count by Recency Score
- Bar Chart: Count by Frequency Score
- Bar Chart: Count by Monetary Score

#### Segment Performance:
- Table: Segment | Customer Count | Revenue | Avg Order Value

### Step 4.3: Create CLV Analysis Page

#### CLV Distribution:
- Histogram: Customer Lifetime Value
- Scatter Plot: CLV vs Purchase Frequency

#### High-Value Customers Table:
- Filter: CLV > Average CLV
- Columns: Customer Name, CLV, Total Orders, Last Purchase Date

#### CLV by Demographics:
- Bar Chart: Average CLV by Age Group
- Bar Chart: Average CLV by Location

### Step 4.4: Create Geographic Analysis Page

#### Map Visualization:
- Use Customer City/State for location
- Bubble size: Revenue or Customer Count
- Color: Customer Segment

#### Revenue by Location:
- Bar Chart: Revenue by State
- Bar Chart: Revenue by City (Top 10)

### Step 4.5: Create Channel Analysis Page

#### Channel Performance:
- Pie Chart: Revenue by Channel
- Bar Chart: Orders by Channel
- Line Chart: Revenue Trend by Channel

#### Channel Demographics:
- Stacked Bar: Customer Age Groups by Channel
- Matrix: Channel vs Customer Segments

---

## Phase 5: Advanced Features & Testing

### Step 5.1: Add Slicers & Filters

#### Global Filters:
1. Date Range Slicer (Transaction Date)
2. Customer Age Group Slicer
3. Location Slicer (State/City)
4. Channel Slicer
5. Product Category Slicer

#### Cross-Page Filters:
- Enable "Sync slicers" across pages
- Set default selections for better UX

### Step 5.2: Custom Tooltips

#### Enhanced Tooltips:
1. Customer Details Tooltip:
   - Customer Name
   - Total Revenue
   - Last Purchase Date
   - Customer Segment
   - CLV Value

2. Segment Details Tooltip:
   - Segment Name
   - Customer Count
   - Average Revenue
   - Average Recency

### Step 5.3: Conditional Formatting

#### Table Formatting:
- Revenue columns: Data bars
- Growth metrics: Color scales (Green for positive, Red for negative)
- Customer segments: Custom colors

#### Chart Formatting:
- Consistent color scheme across all visuals
- Segment colors: Champions (Gold), Loyal (Green), etc.

### Step 5.4: Drillthrough Pages

#### Customer Details Drillthrough:
1. Create new page: "Customer Details"
2. Add drillthrough fields: CustomerID
3. Include detailed customer metrics and transaction history

#### Segment Details Drillthrough:
1. Create new page: "Segment Analysis"
2. Add drillthrough fields: CustomerSegment
3. Show segment-specific insights

### Step 5.5: Testing & Validation

#### Data Validation:
1. Check all measures calculate correctly
2. Verify RFM scores are distributed properly
3. Ensure CLV calculations are accurate
4. Test all slicers and filters

#### Performance Optimization:
1. Check query performance in Performance Analyzer
2. Optimize DAX measures for better performance
3. Consider creating summary tables for large datasets

#### User Experience Testing:
1. Test all interactions and drillthroughs
2. Verify mobile responsiveness
3. Check accessibility features

---

## Phase 6: Publishing & Sharing

### Step 6.1: Final Polish
1. Add company logo and branding
2. Create navigation buttons between pages
3. Add report description and instructions
4. Set default view and filters

### Step 6.2: Publish to Power BI Service
1. Click "Publish" in Power BI Desktop
2. Select destination workspace
3. Set data refresh schedule if needed

### Step 6.3: Share Dashboard
1. Set appropriate permissions
2. Create direct links for stakeholders
3. Schedule automated email reports

---

## 📊 Expected Dashboard Features

✅ RFM Segmentation (Recency, Frequency, Monetary)
✅ Customer Lifetime Value calculations
✅ Interactive filtering by Age, Location, Channel
✅ Geographic analysis with maps
✅ Channel performance analysis
✅ Customer segment insights
✅ Drillthrough capabilities
✅ Custom tooltips and formatting
✅ Mobile-responsive design

---

## 🎯 Success Metrics

- Accurate RFM scoring and segmentation
- Clear identification of high-value customers
- Actionable insights for marketing strategies
- Intuitive user interface
- Fast loading and interaction times
- Comprehensive customer behavior analysis

This complete guide will transform your CSV data into a powerful customer segmentation dashboard that provides deep insights into customer behavior and supports data-driven marketing decisions.