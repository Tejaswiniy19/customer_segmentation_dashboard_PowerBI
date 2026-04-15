# Power BI Dashboard Setup Guide
## Customer Segmentation & RFM Analysis Dashboard

---

## TABLE OF CONTENTS
1. [Prerequisites](#prerequisites)
2. [Data Model Creation](#data-model-creation)
3. [Dashboard Pages](#dashboard-pages)
4. [Interactive Features](#interactive-features)
5. [Step-by-Step Implementation](#step-by-step-implementation)

---

## PREREQUISITES

### Required Knowledge
- Power BI Desktop (current version)
- DAX basics
- Data modeling concepts
- Basic SQL/Excel knowledge

### Files Required
- `Customers.csv` - Customer demographics and information
- `Transactions.csv` - Purchase transaction history
- `Products.csv` - Product catalog with pricing

---

## DATA MODEL CREATION

### Step 1: Import Data

1. **Open Power BI Desktop**
   - Create a new blank report

2. **Load Data Files**
   - Click "Get Data" → "Text/CSV"
   - Load all three CSV files:
     - Customers.csv
     - Transactions.csv
     - Products.csv

3. **Data Loading Options**
   - Use "Load" for simplicity initially
   - Use "Transform Data" if you need to clean columns

---

### Step 2: Create Table Relationships

#### Create Relationships Between Tables:

```
Customers (CustomerID) ←→ Transactions (CustomerID) [1:Many]
Products (ProductID) ←→ Transactions (ProductID) [1:Many]
```

**How to Create Relationships:**
1. Go to "Model" tab
2. Click "Manage Relationships"
3. Create relationships:
   - Customers[CustomerID] to Transactions[CustomerID]
   - Products[ProductID] to Transactions[ProductID]

---

### Step 3: Create Calculated Columns

**In the Customers Table:**

#### Age Calculation
```dax
Age = DATEDIFF(Customers[DateOfBirth], TODAY(), YEAR)
```

#### Customer Status
```dax
CustomerStatus = 
    IF (
        ISBLANK ( RELATED ( Transactions[TransactionID] ) ),
        "Inactive",
        "Active"
    )
```

---

### Step 4: Create Measures

**Create a new table called "Measures" for all DAX calculations:**

1. Right-click in the Fields pane
2. Select "New Table"
3. Enter: `Measures = ROW()`
4. Copy all formulas from `RFM_Calculations.md`
5. Copy all formulas from `CLV_Calculations.md`

---

## DASHBOARD PAGES

### Page 1: Executive Summary

**Visuals to Include:**

1. **Key Metrics (Card Visuals)**
   - Total Customers
   - Total Revenue (Sum of TotalMonetary)
   - Average CLV
   - Number of Transactions

2. **RFM Distribution (Pie Chart)**
   - By RFMSegment
   - Values: Count of Customers

3. **CLV Distribution (Bar Chart)**
   - By CLVTier
   - Values: Sum of TotalMonetary

4. **Top Customers (Table)**
   - Columns: CustomerName, TotalMonetary, PurchaseCount, RFMSegment
   - Sort: TotalMonetary (Descending)
   - Top 10 rows

---

### Page 2: RFM Segmentation

**Visuals to Include:**

1. **RFM Scatter Plot (Bubble Chart) - RECOMMENDED**
   - X-axis: RecencyScore
   - Y-axis: FrequencyScore
   - Bubble: Customers
   - Bubble Size: MonetaryScore (TotalMonetary)
   - Legend: RFMSegment
   - **Shows customer positions clearly**

2. **Segment Performance (Matrix)**
   - Rows: RFMSegment
   - Values: 
     - Count of Customers
     - Sum of TotalMonetary
     - Average Monetary
     - Average Purchase Frequency

3. **Segment Breakdown (Donut Chart)**
   - Legend: RFMSegment
   - Values: Count of Customers

4. **Customer List (Table)**
   - Columns: CustomerName, RFMSegment, RecencyScore, FrequencyScore, MonetaryScore, TotalMonetary
   - Filter by RFM Segment

---

### Page 3: Customer Lifetime Value

**Visuals to Include:**

1. **CLV by Tier (Column Chart)**
   - X-axis: CLVTier
   - Y-axis: Sum of TotalMonetary

2. **CLV Distribution (Histogram/Column)**
   - X-axis: CLV Ranges (bins)
   - Y-axis: Count of Customers

3. **CLV vs Purchase Frequency (Scatter)**
   - X-axis: PurchaseCount
   - Y-axis: TotalMonetary
   - Color: RFMSegment

4. **Customer Profitability (Table)**
   - Columns: CustomerName, TotalMonetary, CustomerGrossProfit, ReturnOnCustomer, CLVTier
   - Sort: CustomerGrossProfit (Descending)

---

### Page 4: Demographics Analysis

**Visuals to Include:**

1. **CLV by Age Group (Column Chart)**
   - X-axis: AgeGroup
   - Y-axis: Sum of TotalMonetary
   - Series: RFMSegment

2. **CLV by Location (Map or Table)**
   - Show: City, State, Count of Customers, Sum of TotalMonetary

3. **Revenue by Channel (Bar Chart)**
   - Y-axis: Channel (Online, In-Store, Phone)
   - X-axis: Sum of TotalAmount

4. **Customer Distribution (Pie)**
   - By Gender
   - Values: Count of Customers

5. **Referral Source Performance (Column)**
   - X-axis: ReferralSource
   - Y-axis: Count of Customers
   - Series: RFMSegment

---

### Page 5: Trend Analysis

**Visuals to Include:**

1. **Revenue Trend (Line Chart)**
   - X-axis: Month of TransactionDate
   - Y-axis: Sum of TotalAmount

2. **Customer Acquisition (Area Chart)**
   - X-axis: Month of JoinDate
   - Y-axis: Count of CustomerID (Cumulative)

3. **Purchase Frequency Over Time (Line)**
   - X-axis: Month of TransactionDate
   - Y-axis: Count of TransactionID

4. **Category Performance (Stacked Column)**
   - X-axis: Month
   - Y-axis: Sum of TotalAmount
   - Series: Category

---

### Page 6: Detailed Customer View

**Visuals to Include:**

1. **Customer Filter (Slicer)**
   - Options: CustomerName (optional - use for deep dive)

2. **Customer Profile Card**
   - Customer Name, Email, Phone, City, State
   - Join Date, Last Purchase Date, Tenure

3. **Customer Metrics (KPI Cards)**
   - Total Spent
   - Purchase Count
   - Average Order Value
   - Days Since Last Purchase

4. **Customer Segment Info (Card)**
   - RFM Segment
   - CLV Tier
   - Segment Recommendation

5. **Purchase History (Table)**
   - Date, Product, Quantity, Amount, Channel
   - Sorted by date descending

6. **Recommendations (Text Box)**
   - Use formula to show segment-based recommendation

---

## INTERACTIVE FEATURES

### Global Slicers (Add to All Pages)

1. **Time Slicer**
   - Field: TransactionDate (or JoinDate)
   - Type: Relative date filter

2. **RFM Segment Slicer**
   - Field: RFMSegment
   - Type: Buttons or Dropdown

3. **CLV Tier Slicer**
   - Field: CLVTier
   - Type: Dropdown

4. **Age Group Slicer**
   - Field: AgeGroup
   - Type: Buttons

5. **Location Slicer**
   - Field: State or City
   - Type: Dropdown or Multi-select

6. **Channel Slicer**
   - Field: Channel
   - Type: Buttons

---

## STEP-BY-STEP IMPLEMENTATION

### Implementation Sequence:

**Phase 1: Data Setup (Week 1)**
1. Import CSV files
2. Create relationships
3. Test data model

**Phase 2: Calculations (Week 1)**
1. Create calculated columns
2. Add RFM measures
3. Add CLV measures
4. Validate calculations

**Phase 3: Executive Summary (Week 2)**
1. Create dashboard page 1
2. Add KPI cards
3. Create visualizations
4. Format and align

**Phase 4: RFM Analysis (Week 2)**
1. Create RFM page
2. Add bubble chart (key visual)
3. Add segment table
4. Test interactions

**Phase 5: CLV Analysis (Week 2)**
1. Create CLV page
2. Add distribution visuals
3. Add profitability table
4. Format for readability

**Phase 6: Demographics (Week 3)**
1. Create demographics page
2. Add location-based visuals
3. Add demographic breakdowns
4. Format for business users

**Phase 7: Trends (Week 3)**
1. Create trend page
2. Add time-based visuals
3. Add cumulative metrics
4. Enable forecasting if needed

**Phase 8: Details & Polish (Week 3)**
1. Create detail page
2. Add customer profile visuals
3. Create recommendations logic
4. Final formatting and branding

---

## BEST PRACTICES

### Visual Design
- Use consistent color scheme
- Limit to 3-4 colors per page
- Blue for positive metrics, Red for risk
- Use light backgrounds for readability

### Performance
- Hide unused columns from model
- Use aggregations for large datasets
- Optimize DAX formulas
- Test with full dataset

### User Experience
- Add page navigation buttons
- Use tooltips for complex metrics
- Add titles and descriptions
- Provide export options (PDF, Excel)

### Data Refresh
- Set automated refresh on schedule
- Monitor refresh performance
- Keep historical snapshots
- Document data source updates

---

## SECURITY & SHARING

### Row-Level Security (RLS)
```dax
[Sales Territory] = USERNAME()
```

### Sharing Options
1. Publish to Power BI Service
2. Set refresh schedule (daily/weekly)
3. Configure user permissions
4. Set up alerts on key metrics

---

## COMMON ISSUES & SOLUTIONS

| Issue | Solution |
|-------|----------|
| Slow dashboard | Add aggregations, hide unused columns, optimize DAX |
| Incorrect RFM scores | Check date calculations, verify data quality |
| Missing relationships | Verify column names match exactly |
| Slicer interference | Use KEEPFILTERS() in formulas if needed |
| Data not updating | Check refresh schedule, verify data source |

---

## NEXT STEPS

1. **Advanced Analytics**
   - Add Python/R scripts for clustering
   - Implement ML predictions
   - Create churn prediction model

2. **Automation**
   - Create alerts for at-risk customers
   - Generate automated reports
   - Set up email subscriptions

3. **Integration**
   - Connect to CRM system
   - Link to marketing platform
   - Integrate with sales data

4. **Expansion**
   - Add product affinity analysis
   - Create campaign ROI tracking
   - Build customer journey visualization
