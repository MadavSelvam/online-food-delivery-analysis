
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Online Food Delivery Analysis",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Paths and data ----------
APP_DIR = Path(__file__).resolve().parent
DATA_PATH = APP_DIR / "data" / "processed" / "online_food_delivery_analysis_featured.csv"

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    # Normalize date values for date filters and time series charts.
    if "order_date" in data.columns:
        data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
    if "order_time" in data.columns:
        data["order_time"] = data["order_time"].astype("string")
    return data

def find_col(data: pd.DataFrame, *names):
    lookup = {str(c).lower(): c for c in data.columns}
    for name in names:
        if name.lower() in lookup:
            return lookup[name.lower()]
    return None

def numeric_series(data: pd.DataFrame, col):
    if not col:
        return pd.Series(dtype="float64")
    return pd.to_numeric(data[col], errors="coerce")

def money(value):
    if pd.isna(value):
        return "N/A"
    return f"₹{value:,.2f}"

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.info(
        "Run Notebook 03 — Feature Engineering first. "
        "Expected file: data/processed/online_food_delivery_analysis_featured.csv"
    )
    st.stop()

df = load_data(str(DATA_PATH))
if df.empty:
    st.warning("The dataset contains no rows.")
    st.stop()

# Resolve column names from the featured dataset.
order_id_col = find_col(df, "order_id")
date_col = find_col(df, "order_date")
status_col = find_col(df, "order_status")
amount_col = find_col(df, "final_amount")
order_value_col = find_col(df, "order_value")
delivery_time_col = find_col(df, "delivery_time_min")
delivery_rating_col = find_col(df, "delivery_rating")
profit_col = find_col(df, "profit_margin")
city_col = find_col(df, "city")
cuisine_col = find_col(df, "cuisine_type")
payment_col = find_col(df, "payment_mode")
distance_col = find_col(df, "distance_km")
restaurant_rating_col = find_col(df, "restaurant_rating")
peak_col = find_col(df, "peak_period", "peak_hour")
cancel_reason_col = find_col(df, "cancellation_reason")
is_delivered_col = find_col(df, "is_delivered")
is_cancelled_col = find_col(df, "is_cancelled")

# Convert the actual date column to datetime regardless of its original capitalization.
# This avoids string values reaching .min().date() and enables the .dt.date filter below.
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

def status_mask(frame, expected):
    if status_col:
        return frame[status_col].astype("string").str.strip().str.lower().eq(expected.lower())
    flag_col = is_delivered_col if expected.lower() == "delivered" else is_cancelled_col
    if flag_col:
        return frame[flag_col].astype("string").str.strip().str.lower().isin(["true", "1", "yes"])
    return pd.Series(False, index=frame.index)

# ---------- Header ----------
st.title("🍽️ Online Food Delivery Analysis")
st.caption("Interactive analysis of a synthetic food delivery dataset • Use the sidebar to filter results.")

with st.sidebar:
    st.header("Dashboard Filters")

    filtered = df.copy()

    if date_col:
        # Re-coerce defensively in case the source column was loaded as text.
        filtered[date_col] = pd.to_datetime(filtered[date_col], errors="coerce")
        valid_dates = filtered[date_col].dropna()
        if not valid_dates.empty:
            min_date = pd.Timestamp(valid_dates.min()).date()
            max_date = pd.Timestamp(valid_dates.max()).date()
            # Use two single-date inputs instead of Streamlit's date-range mode.
            # This removes the built-in quick-preset menu (for example, "Past 2 Years").
            start_date = st.date_input(
                "Start date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="order_start_date",
            )
            end_date = st.date_input(
                "End date",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="order_end_date",
            )
            if start_date <= end_date:
                filtered = filtered[
                    filtered[date_col].isna()
                    | (
                        filtered[date_col].dt.date.ge(start_date)
                        & filtered[date_col].dt.date.le(end_date)
                    )
                ]
            else:
                st.warning("Start date must be on or before the end date.")

    filter_fields = [
        ("City", city_col),
        ("Cuisine", cuisine_col),
        ("Order status", status_col),
        ("Payment mode", payment_col),
    ]
    for label, col in filter_fields:
        if col:
            options = sorted(filtered[col].dropna().astype(str).unique().tolist())
            selected = st.multiselect(f"{label}", options, default=[])
            if selected:
                filtered = filtered[filtered[col].astype(str).isin(selected)]

    st.divider()
    st.caption(f"Rows after filters: {len(filtered):,} / {len(df):,}")

# ---------- KPIs ----------
if filtered.empty:
    st.warning("No orders match the selected filters. Clear one or more filters to see results.")
    st.stop()

total_orders = len(filtered)
delivered_mask = status_mask(filtered, "Delivered")
cancelled_mask = status_mask(filtered, "Cancelled")

amounts = numeric_series(filtered, amount_col)
revenue = amounts[delivered_mask].sum(min_count=1) if amount_col else np.nan
# Average order value is based on delivered orders with recorded final amounts.
aov_values = amounts[delivered_mask].dropna() if amount_col else pd.Series(dtype=float)
aov = aov_values.mean() if not aov_values.empty else np.nan

delivery_times = numeric_series(filtered, delivery_time_col)
delivery_values = delivery_times[delivered_mask].dropna()
avg_delivery_time = delivery_values.mean() if not delivery_values.empty else np.nan

cancel_rate = cancelled_mask.mean() * 100 if total_orders else np.nan

delivery_ratings = numeric_series(filtered, delivery_rating_col)
rating_values = delivery_ratings[delivered_mask].dropna()
avg_delivery_rating = rating_values.mean() if not rating_values.empty else np.nan

profit_values = numeric_series(filtered, profit_col)[delivered_mask].dropna()
profit_margin_pct = profit_values.mean() * 100 if not profit_values.empty else np.nan

kpis = [
    ("Total Orders", f"{total_orders:,}"),
    ("Total Revenue", money(revenue)),
    ("Average Order Value", money(aov)),
    ("Average Delivery Time", f"{avg_delivery_time:.1f} min" if pd.notna(avg_delivery_time) else "N/A"),
    ("Cancellation Rate", f"{cancel_rate:.2f}%" if pd.notna(cancel_rate) else "N/A"),
    ("Average Delivery Rating", f"{avg_delivery_rating:.2f} / 5" if pd.notna(avg_delivery_rating) else "N/A"),
    ("Profit Margin", f"{profit_margin_pct:.2f}%" if pd.notna(profit_margin_pct) else "N/A"),
]
rows = [st.columns(4), st.columns(3)]
for idx, (label, value) in enumerate(kpis):
    container = rows[0][idx] if idx < 4 else rows[1][idx - 4]
    container.metric(label, value)

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

with left:
    st.subheader("Order Status Distribution")
    if status_col:
        status_data = filtered[status_col].fillna("Unknown").astype(str).value_counts().rename_axis("Order Status").reset_index(name="Orders")
        fig = px.pie(status_data, names="Order Status", values="Orders", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Order status column is unavailable.")

with right:
    st.subheader("Revenue Trend")
    if date_col and amount_col:
        revenue_data = filtered.loc[delivered_mask].copy()
        revenue_data["_amount"] = numeric_series(revenue_data, amount_col)
        revenue_data = revenue_data.dropna(subset=[date_col, "_amount"])
        if not revenue_data.empty:
            trend = revenue_data.groupby(revenue_data[date_col].dt.to_period("M"))["_amount"].sum().reset_index()
            trend[date_col] = trend[date_col].astype(str)
            trend.columns = ["Month", "Revenue"]
            fig = px.line(trend, x="Month", y="Revenue", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recorded delivered revenue is available for the selected filters.")
    else:
        st.info("Order date or final amount column is unavailable.")

left, right = st.columns(2)

with left:
    st.subheader("Revenue by City")
    if city_col and amount_col:
        city_data = filtered.loc[delivered_mask].copy()
        city_data["_amount"] = numeric_series(city_data, amount_col)
        city_data = city_data.dropna(subset=["_amount"])
        city_summary = city_data.groupby(city_col, dropna=False)["_amount"].sum().sort_values(ascending=False).head(12).reset_index()
        city_summary.columns = ["City", "Revenue"]
        if not city_summary.empty:
            fig = px.bar(city_summary, x="City", y="Revenue", text_auto=".2s")
            fig.update_layout(xaxis_title="", yaxis_title="Revenue (₹)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No revenue values available for the selected filters.")
    else:
        st.info("City or final amount column is unavailable.")

with right:
    st.subheader("Cuisine Performance")
    if cuisine_col and amount_col:
        cuisine_data = filtered.loc[delivered_mask].copy()
        cuisine_data["_amount"] = numeric_series(cuisine_data, amount_col)
        cuisine_summary = cuisine_data.groupby(cuisine_col, dropna=False).agg(
            Orders=("_amount", "size"),
            Revenue=("_amount", "sum"),
        ).sort_values("Revenue", ascending=False).head(12).reset_index()
        cuisine_summary = cuisine_summary.rename(columns={cuisine_col: "Cuisine"})
        if not cuisine_summary.empty:
            fig = px.bar(cuisine_summary, x="Cuisine", y="Revenue", hover_data=["Orders"], text_auto=".2s")
            fig.update_layout(xaxis_title="", yaxis_title="Revenue (₹)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cuisine revenue available.")
    else:
        st.info("Cuisine or final amount column is unavailable.")

left, right = st.columns(2)

with left:
    st.subheader("Delivery Time Distribution")
    if delivery_time_col:
        delivery_chart = filtered.loc[delivered_mask].copy()
        delivery_chart["_delivery_time"] = numeric_series(delivery_chart, delivery_time_col)
        delivery_chart = delivery_chart.dropna(subset=["_delivery_time"])
        if not delivery_chart.empty:
            fig = px.histogram(delivery_chart, x="_delivery_time", nbins=30, labels={"_delivery_time": "Delivery time (minutes)"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No delivery-time values available.")
    else:
        st.info("Delivery time column is unavailable.")

with right:
    st.subheader("Payment Mode")
    if payment_col:
        payment_data = filtered[payment_col].fillna("Unknown").astype(str).value_counts().rename_axis("Payment Mode").reset_index(name="Orders")
        fig = px.bar(payment_data, x="Payment Mode", y="Orders", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Payment mode column is unavailable.")

# ---------- Detail table and download ----------
st.divider()
st.subheader("Filtered Order Details")
st.caption("The table reflects the selected filters. Missing source values remain missing and are not imputed for display.")
st.dataframe(filtered, use_container_width=True, hide_index=True)

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv_bytes,
    file_name="food_delivery_filtered_orders.csv",
    mime="text/csv",
)

with st.expander("Metric definitions and data notes"):
    st.markdown("""
    - **Total Orders:** number of rows after filters.
    - **Total Revenue:** sum of recorded `Final_Amount` for delivered orders only; missing amounts are excluded.
    - **Average Order Value:** mean recorded `Final_Amount` for delivered orders only.
    - **Average Delivery Time:** mean recorded delivery time for delivered orders only.
    - **Cancellation Rate:** cancelled orders divided by all filtered orders.
    - **Average Delivery Rating:** mean recorded delivery rating for delivered orders only.
    - **Profit Margin:** mean recorded profit-margin value for delivered orders, displayed as a percentage.

    This is a synthetic dataset. Results are illustrative and should not be represented as actual company performance.
    """)