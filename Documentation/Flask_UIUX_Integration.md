# Flask UI/UX Integration for Customer Segmentation Project

## One-Sequence Plan: Power BI → Flask Web Dashboard

### Goal
Transform the Power BI customer segmentation project into a polished Flask web dashboard with excellent UI/UX and the same customer insights.

---

## Step 1: Install Python Dependencies

Run this once in your project folder:

```powershell
cd "c:\Users\yerra\OneDrive\Desktop\BI2\FlaskDashboard"
pip install -r requirements.txt
```

You can start the app two ways:

```powershell
cd "c:\Users\yerra\OneDrive\Desktop\BI2\FlaskDashboard"
python app.py
```

or from the project root:

```powershell
cd "c:\Users\yerra\OneDrive\Desktop\BI2"
run_flask.bat
```

---

## Step 2: Launch the Flask App

```powershell
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

## Step 3: Use the UI in One Sequence

1. Open the home page
2. Choose filters:
   - Age Group
   - State
   - Purchase Channel
3. Click **Apply Filters**
4. Review key metrics, segment distribution, channel revenue, and top customers6. Navigate to **Advanced Analytics** for RFM distribution and drill-down charts
7. Open **Power BI Embed** and paste a publish-to-web or embed URL to view a Power BI report inside Flask
This is the one clean sequence from raw CSV to actionable dashboard.

---

## What the Flask Dashboard Shows

- Total revenue
- Unique customer count
- Average order value
- Total orders
- RFM customer segments
- Channel revenue breakdown
- Top 10 customers by CLV

---

## Why This UI/UX Works

- Clean dark interface with modern cards and spacing
- Responsive layout for desktop and tablet screens
- Dynamic filtering with immediate metrics update
- Minimal clicks to access the full customer segmentation story
- Clear color palette for segment and channel charts

---

## File Structure

```
BI2/
├── Data/
│   ├── Customers.csv
│   ├── Products.csv
│   └── Transactions.csv
├── FlaskDashboard/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   │   └── css/style.css
│   └── templates/
│       ├── base.html
│       └── index.html
└── Documentation/
    ├── Flask_UIUX_Integration.md
    └── ...
```

---

## Notes

- The Flask app reads your existing CSV files directly from the `Data/` folder.
- This is a native web app version of the same project, with advanced analytics and drill-down support.
- It now includes:
  - `/analytics` for advanced RFM and CLV visualizations
  - drill-down navigation by customer segment
  - `/embed` for embedding a Power BI report via publish-to-web or embed URL
- For a secure Power BI deployment, use Power BI Service embed tokens and secure app registration later.
