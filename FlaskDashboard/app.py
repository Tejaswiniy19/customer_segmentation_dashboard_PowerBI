from datetime import datetime
from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CUSTOMER_CSV = os.path.join(BASE_DIR, "Data", "Customers.csv")
PRODUCT_CSV = os.path.join(BASE_DIR, "Data", "Products.csv")
TRANSACTION_CSV = os.path.join(BASE_DIR, "Data", "Transactions.csv")

customers = pd.read_csv(CUSTOMER_CSV, parse_dates=["DateOfBirth", "JoinDate"])
products = pd.read_csv(PRODUCT_CSV)
transactions = pd.read_csv(TRANSACTION_CSV, parse_dates=["TransactionDate"])

# Normalize text fields for filters
customers["State"] = customers["State"].astype(str)
customers["AgeGroup"] = customers["AgeGroup"].astype(str)
transactions["Channel"] = transactions["Channel"].astype(str)

# Build lookup dictionaries for filters
AGE_GROUPS = ["All"] + sorted(customers["AgeGroup"].dropna().unique().tolist())
STATES = ["All"] + sorted(customers["State"].dropna().unique().tolist())
CHANNELS = ["All"] + sorted(transactions["Channel"].dropna().unique().tolist())


def compute_segment(score):
    if score >= 555:
        return "Champions"
    if score >= 445:
        return "Loyal Customers"
    if score >= 334:
        return "Potential Loyalists"
    if score >= 223:
        return "Promising"
    if score >= 112:
        return "Needs Attention"
    return "At Risk"


def make_scores(df):
    # Recency scoring
    df["RecencyScore"] = df["Recency"].apply(
        lambda d: 5 if d <= 30 else 4 if d <= 60 else 3 if d <= 90 else 2 if d <= 180 else 1
    )
    # Frequency scoring
    df["FrequencyScore"] = df["Frequency"].apply(
        lambda f: 5 if f >= 8 else 4 if f >= 5 else 3 if f >= 3 else 2 if f >= 2 else 1
    )
    # Monetary scoring
    df["MonetaryScore"] = df["Monetary"].apply(
        lambda m: 5 if m >= 1000 else 4 if m >= 500 else 3 if m >= 250 else 2 if m >= 100 else 1
    )
    df["RFMScore"] = df["RecencyScore"] * 100 + df["FrequencyScore"] * 10 + df["MonetaryScore"]
    df["CustomerSegment"] = df["RFMScore"].apply(compute_segment)
    df["LifetimeValue"] = df["Monetary"]
    return df


def load_dashboard_data(age_filter, state_filter, channel_filter):
    filtered_customers = customers.copy()
    filtered_transactions = transactions.copy()

    if age_filter and age_filter != "All":
        filtered_customers = filtered_customers[filtered_customers["AgeGroup"] == age_filter]
    if state_filter and state_filter != "All":
        filtered_customers = filtered_customers[filtered_customers["State"] == state_filter]
    if channel_filter and channel_filter != "All":
        filtered_transactions = filtered_transactions[filtered_transactions["Channel"] == channel_filter]

    merged = pd.merge(filtered_transactions, filtered_customers, on="CustomerID", how="inner")
    if merged.empty:
        return None, None

    latest_date = merged["TransactionDate"].max()
    customer_agg = merged.groupby("CustomerID").agg(
        CustomerName=("CustomerName", "first"),
        AgeGroup=("AgeGroup", "first"),
        State=("State", "first"),
        Channel=("Channel", "first"),
        Recency=("TransactionDate", lambda dates: (latest_date - dates.max()).days),
        Frequency=("TransactionID", "count"),
        Monetary=("TotalAmount", "sum"),
        LastPurchase=("TransactionDate", "max")
    ).reset_index()
    customer_agg = make_scores(customer_agg)

    return merged, customer_agg


def prepare_dashboard_data(age_filter, state_filter, channel_filter):
    merged, customer_agg = load_dashboard_data(age_filter, state_filter, channel_filter)
    if merged is None:
        return None

    metrics = {
        "total_revenue": merged["TotalAmount"].sum(),
        "total_customers": merged["CustomerID"].nunique(),
        "total_orders": len(merged),
        "average_order_value": merged["TotalAmount"].sum() / len(merged) if len(merged) else 0,
        "average_customer_value": customer_agg["LifetimeValue"].mean() if not customer_agg.empty else 0
    }

    segment_counts = customer_agg["CustomerSegment"].value_counts().reindex(
        ["Champions", "Loyal Customers", "Potential Loyalists", "Promising", "Needs Attention", "At Risk"], fill_value=0
    ).to_dict()

    channel_revenue = merged.groupby("Channel")["TotalAmount"].sum().sort_values(ascending=False).to_dict()
    top_customers = customer_agg.sort_values(by="LifetimeValue", ascending=False).head(10)

    return {
        "metrics": metrics,
        "segment_counts": segment_counts,
        "channel_revenue": channel_revenue,
        "top_customers": top_customers.to_dict("records"),
        "customer_agg": customer_agg,
        "merged": merged,
        "filter_state": {
            "age": age_filter,
            "state": state_filter,
            "channel": channel_filter,
        },
        "available_filters": {
            "age_groups": AGE_GROUPS,
            "states": STATES,
            "channels": CHANNELS,
        },
    }


@app.route("/", methods=["GET"])
def index():
    age_filter = request.args.get("age", "All")
    state_filter = request.args.get("state", "All")
    channel_filter = request.args.get("channel", "All")

    data = prepare_dashboard_data(age_filter, state_filter, channel_filter)
    if data is None:
        return render_template("index.html", error="No data matches the selected filters.")

    return render_template(
        "index.html",
        metrics=data["metrics"],
        segment_counts=data["segment_counts"],
        channel_revenue=data["channel_revenue"],
        top_customers=data["top_customers"],
        filters=data["filter_state"],
        available_filters=data["available_filters"],
    )


@app.route("/analytics", methods=["GET"])
def analytics():
    age_filter = request.args.get("age", "All")
    state_filter = request.args.get("state", "All")
    channel_filter = request.args.get("channel", "All")

    data = prepare_dashboard_data(age_filter, state_filter, channel_filter)
    if data is None:
        return render_template("analytics.html", error="No data matches the selected filters.")

    customer_agg = data["customer_agg"]
    rfm_distribution = {
        "recency": customer_agg["RecencyScore"].value_counts().reindex([5, 4, 3, 2, 1], fill_value=0).to_dict(),
        "frequency": customer_agg["FrequencyScore"].value_counts().reindex([5, 4, 3, 2, 1], fill_value=0).to_dict(),
        "monetary": customer_agg["MonetaryScore"].value_counts().reindex([5, 4, 3, 2, 1], fill_value=0).to_dict(),
    }

    return render_template(
        "analytics.html",
        metrics=data["metrics"],
        segment_counts=data["segment_counts"],
        channel_revenue=data["channel_revenue"],
        top_customers=data["top_customers"],
        filter_state=data["filter_state"],
        available_filters=data["available_filters"],
        rfm_distribution=rfm_distribution,
    )


@app.route("/segment/<segment_name>", methods=["GET"])
def segment_detail(segment_name):
    age_filter = request.args.get("age", "All")
    state_filter = request.args.get("state", "All")
    channel_filter = request.args.get("channel", "All")

    merged, customer_agg = load_dashboard_data(age_filter, state_filter, channel_filter)
    if merged is None:
        return render_template("segment.html", error="No data matches the selected filters.")

    segment_customers = customer_agg[customer_agg["CustomerSegment"] == segment_name]
    if segment_customers.empty:
        return render_template("segment.html", segment=segment_name, customers=[], total_revenue=0, average_clv=0)

    total_revenue = segment_customers["Monetary"].sum()
    average_clv = segment_customers["LifetimeValue"].mean()
    top_customers = segment_customers.sort_values(by="LifetimeValue", ascending=False).head(15)

    return render_template(
        "segment.html",
        segment=segment_name,
        customers=top_customers.to_dict("records"),
        total_revenue=total_revenue,
        average_clv=average_clv,
        filters={"age": age_filter, "state": state_filter, "channel": channel_filter},
        available_filters={"age_groups": AGE_GROUPS, "states": STATES, "channels": CHANNELS},
    )


@app.route("/embed", methods=["GET"])
def embed():
    embed_url = request.args.get("report_url", "")
    return render_template("embed.html", embed_url=embed_url)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
