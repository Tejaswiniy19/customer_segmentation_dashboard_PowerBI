# Power BI Dashboard Layout Guide

## 📊 EXECUTIVE SUMMARY PAGE

### TOP ROW - Key Metrics Cards (4 cards across)
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Total Revenue   │ │ Total Customers │ │ Avg Order Value│ │ Total Orders    │
│ $45,678.90      │ │ 1,247           │ │ $127.45        │ │ 3,456           │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### MIDDLE ROW - Main Visualizations
```
┌─────────────────────────────────────────────────┐ ┌─────────────────────┐
│              RFM Customer Segments              │ │  Revenue Trend      │
│                                                 │ │                     │
│  Champions: 15% (187 customers)                 │ │  ┌─────────────────┐ │
│  Loyal Customers: 22% (274 customers)           │ │  │     /\          │ │
│  Potential Loyalists: 18% (224 customers)       │ │  │    /  \         │ │
│  Promising: 20% (249 customers)                 │ │  │   /    \        │ │
│  Needs Attention: 15% (187 customers)           │ │  │  /      \       │ │
│  At Risk: 10% (125 customers)                   │ │  │ /        \      │ │
│                                                 │ │  └─────────────────┘ │
└─────────────────────────────────────────────────┘ └─────────────────────┘
```

### BOTTOM ROW - Geographic & Channel Analysis
```
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│        Revenue by State             │ │       Revenue by Channel           │
│                                     │ │                                     │
│  CA: $12,345 (27%)                  │ │  Online: $28,901 (63%)             │
│  NY: $9,876 (22%)                   │ │  In-Store: $11,234 (25%)           │
│  TX: $7,654 (17%)                   │ │  Phone: $5,544 (12%)               │
│  FL: $5,432 (12%)                   │ │                                     │
│  Other: $10,372 (22%)               │ │                                     │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## 📈 RFM ANALYSIS PAGE

### RFM SCATTER PLOT (Main Visualization)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                          RFM Customer Analysis                          │
│                                                                         │
│  Monetary Score                                                         │
│     5 ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ │
│       ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│     4 ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│       ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│     3 ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│       ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│     2 ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│       ■ ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● │
│     1 ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ │
│         1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16 │
│                           Frequency Score                               │
│                                                                         │
│  ■ Champions    ● Loyal Customers    ● Potential Loyalists             │
│  ● Promising    ● Needs Attention    ● At Risk                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### RFM SCORE DISTRIBUTION
```
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│   Recency Scores    │ │  Frequency Scores  │ │  Monetary Scores    │
│                     │ │                     │ │                     │
│  5: ▓▓▓▓▓▓▓▓▓▓ 234 │ │  5: ▓▓▓▓▓▓▓▓ 187  │ │  5: ▓▓▓▓▓▓▓▓▓ 221  │
│  4: ▓▓▓▓▓▓▓▓▓ 198  │ │  4: ▓▓▓▓▓▓▓▓▓ 203 │ │  4: ▓▓▓▓▓▓▓▓▓▓ 245 │
│  3: ▓▓▓▓▓▓▓▓ 176   │ │  3: ▓▓▓▓▓▓▓▓▓▓ 267 │ │  3: ▓▓▓▓▓▓▓▓▓▓ 278 │
│  2: ▓▓▓▓▓▓ 145     │ │  2: ▓▓▓▓▓▓▓▓▓▓▓ 312 │ │  2: ▓▓▓▓▓▓▓▓▓▓ 301 │
│  1: ▓▓▓▓ 98        │ │  1: ▓▓▓▓▓▓▓▓▓▓▓▓ 278 │ │  1: ▓▓▓▓▓▓▓▓▓ 202 │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

### SEGMENT PERFORMANCE TABLE
```
┌─────────────────────────────────────────────────────────────────────┐
│                    Customer Segment Performance                      │
├─────────────────────┬─────────────┬──────────────┬──────────────────┤
│ Segment             │ Customers   │ Revenue      │ Avg Order Value  │
├─────────────────────┼─────────────┼──────────────┼──────────────────┤
│ Champions           │ 187 (15%)   │ $18,765 (41%)│ $234.56          │
│ Loyal Customers     │ 274 (22%)   │ $12,345 (27%)│ $187.65          │
│ Potential Loyalists │ 224 (18%)   │ $8,765 (19%) │ $145.67          │
│ Promising           │ 249 (20%)   │ $3,456 (8%)  │ $98.76           │
│ Needs Attention     │ 187 (15%)   │ $1,567 (3%)  │ $76.54           │
│ At Risk             │ 125 (10%)   │ $765 (2%)    │ $54.32           │
└─────────────────────┴─────────────┴──────────────┴──────────────────┘
```

---

## 💰 CLV ANALYSIS PAGE

### CLV DISTRIBUTION & HIGH-VALUE CUSTOMERS
```
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│      CLV Distribution                │ │    Top 10 High-Value Customers    │
│                                     │ │                                     │
│  $0-$500: ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 623     │ │  1. John Smith          $2,345.67 │
│  $500-$1000: ▓▓▓▓▓▓▓▓▓▓▓▓ 445      │ │  2. Sarah Johnson       $2,123.45 │
│  $1000-$2000: ▓▓▓▓▓▓▓▓▓ 312        │ │  3. Michael Brown       $1,987.65 │
│  $2000-$5000: ▓▓▓▓▓▓ 187           │ │  4. Jennifer Williams   $1,876.54 │
│  $5000+: ▓▓▓ 78                     │ │  5. Robert Davis       $1,765.43 │
│                                     │ │  6. Emily Martinez      $1,654.32 │
│                                     │ │  7. David Wilson        $1,543.21 │
│                                     │ │  8. Jessica Anderson    $1,432.10 │
│                                     │ │  9. James Taylor        $1,321.09 │
│                                     │ │  10. Maria Garcia       $1,210.98 │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
```

### CLV BY DEMOGRAPHICS
```
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│     Average CLV by Age Group        │ │     Average CLV by Location        │
│                                     │ │                                     │
│  18-24: $345.67                     │ │  California: $567.89               │
│  25-34: $456.78                     │ │  New York: $498.76                 │
│  35-44: $567.89                     │ │  Texas: $445.67                    │
│  45-54: $678.90                     │ │  Florida: $387.65                  │
│  55+: $789.01                       │ │  Other: $298.76                    │
│                                     │ │                                     │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## 🗺️ GEOGRAPHIC ANALYSIS PAGE

### INTERACTIVE MAP & LOCATION BREAKDOWN
```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Revenue by Location                            │
│                                                                         │
│  [Interactive Map with bubbles sized by revenue, colored by segments]  │
│                                                                         │
│  ■ Large bubbles = High revenue    ● Medium bubbles = Medium revenue   │
│  ■ Small bubbles = Low revenue     ▲ At Risk customers                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### LOCATION PERFORMANCE TABLES
```
┌─────────────────────┐ ┌─────────────────────┐
│   Top 10 Cities     │ │   Revenue by State  │
│                     │ │                     │
│  1. LA     $8,765   │ │  CA: $12,345 (27%)  │
│  2. NYC    $7,654   │ │  NY: $9,876 (22%)   │
│  3. Houston $5,432  │ │  TX: $7,654 (17%)   │
│  4. Miami  $4,321   │ │  FL: $5,432 (12%)   │
│  5. Dallas $3,210   │ │  IL: $4,321 (9%)    │
│  6. Phoenix$2,109   │ │  AZ: $3,210 (7%)    │
│  7. Chicago$1,008   │ │  PA: $2,109 (5%)    │
│  8. Philly $907     │ │  Other: $765 (2%)   │
│  9. Austin $806     │ │                     │
│  10. Denver$705     │ │                     │
└─────────────────────┘ └─────────────────────┘
```

---

## 📱 CHANNEL ANALYSIS PAGE

### CHANNEL PERFORMANCE METRICS
```
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ Revenue by Channel  │ │ Orders by Channel   │ │ Avg Order by Channel│
│                     │ │                     │ │                     │
│  Online: $28,901    │ │  Online: 2,345      │ │  Online: $145.67    │
│  (63%)              │ │  (68%)              │ │                     │
│                     │ │                     │ │                     │
│  In-Store: $11,234  │ │  In-Store: 987      │ │  In-Store: $123.45  │
│  (25%)              │ │  (28%)              │ │                     │
│                     │ │                     │ │                     │
│  Phone: $5,544      │ │  Phone: 124         │ │  Phone: $98.76      │
│  (12%)              │ │  (4%)               │ │                     │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

### CHANNEL DEMOGRAPHICS & TRENDS
```
┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
│   Customer Age Groups by Channel    │ │     Channel Revenue Trends        │
│                                     │ │                                     │
│  Online:                            │ │  ┌─────────────────────────────┐ │
│  18-24: 35%    25-34: 28%           │ │  │         /\                  │ │
│  35-44: 22%    45-54: 10%           │ │  │        /  \                 │ │
│  55+: 5%                            │ │  │       /    \   Online       │ │
│                                     │ │  │      /      \               │ │
│  In-Store:                          │ │  │     /        \              │ │
│  18-24: 15%    25-34: 20%           │ │  │    /          \             │ │
│  35-44: 30%    45-54: 25%           │ │  │   /            \            │ │
│  55+: 10%                           │ │  │  /              \           │ │
│                                     │ │  └─────────────────────────────┘ │
│  Phone:                             │ │  ─── In-Store ─── Phone ────── │
│  18-24: 5%     25-34: 10%           │ │                                     │
│  35-44: 25%    45-54: 35%           │ │                                     │
│  55+: 25%                           │ │                                     │
└─────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## 🎛️ INTERACTIVE FILTERS (Available on all pages)

### GLOBAL SLICERS (Top of each page)
```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Date Range  │ │ Age Groups  │ │ States      │ │ Channels    │ │ Segments    │
│ [Calendar]  │ │ □ 18-24     │ │ □ CA        │ │ □ Online    │ │ □ Champions │
│             │ │ □ 25-34     │ │ □ NY        │ │ □ In-Store  │ │ □ Loyal     │
│             │ │ □ 35-44     │ │ □ TX        │ │ □ Phone     │ │ □ Potential │
│             │ │ □ 45-54     │ │ □ FL        │ │             │ │ □ Promising │
│             │ │ □ 55+       │ │ □ Other     │ │             │ │ □ At Risk   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 🎨 DESIGN PRINCIPLES

### Color Scheme:
- **Champions**: Gold (#FFD700)
- **Loyal Customers**: Green (#32CD32)
- **Potential Loyalists**: Blue (#87CEEB)
- **Promising**: Orange (#FFA500)
- **Needs Attention**: Yellow (#FFFF00)
- **At Risk**: Red (#FF0000)

### Typography:
- Headers: Segoe UI Bold, 14pt
- Body Text: Segoe UI Regular, 10pt
- Numbers: Segoe UI Semibold, 12pt

### Layout:
- Consistent spacing (8px grid)
- Left-aligned text
- Clear visual hierarchy
- Mobile-responsive design

### Interactivity:
- Cross-filtering enabled
- Drillthrough pages
- Custom tooltips
- Sync'd slicers across pages

This layout provides a comprehensive view of customer segmentation data with intuitive navigation and powerful analytical capabilities.