import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/analytical_food_delivery.csv"

CHART_DIR = "outputs/charts"
INSIGHT_DIR = "outputs/insights"

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(INSIGHT_DIR, exist_ok=True)


print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 2. OVERALL BUSINESS KPIs
# ============================================================

total_orders = df["Order_ID"].nunique()

delivered_orders = df["Is_Delivered"].sum()

cancelled_orders = df["Is_Cancelled"].sum()

cancellation_rate = (
    cancelled_orders / total_orders * 100
)

total_order_value = df["Order_Value"].sum()

total_final_amount = df["Final_Amount"].sum()

average_order_value = df["Order_Value"].mean()

average_final_amount = df["Final_Amount"].mean()

average_delivery_time = df["Delivery_Time_Min"].mean()

average_delivery_rating = df["Delivery_Rating"].mean()

average_restaurant_rating = df["Restaurant_Rating"].mean()

average_profit_margin = df["Profit_Margin"].mean()


print("\n" + "-" * 60)
print("OVERALL BUSINESS KPIs")
print("-" * 60)

print(f"Total Orders: {total_orders:,}")
print(f"Delivered Orders: {delivered_orders:,}")
print(f"Cancelled Orders: {cancelled_orders:,}")
print(f"Cancellation Rate: {cancellation_rate:.2f}%")
print(f"Total Order Value: {total_order_value:,.2f}")
print(f"Total Final Amount: {total_final_amount:,.2f}")
print(f"Average Order Value: {average_order_value:,.2f}")
print(f"Average Final Amount: {average_final_amount:,.2f}")
print(f"Average Delivery Time: {average_delivery_time:.2f} minutes")
print(f"Average Delivery Rating: {average_delivery_rating:.2f}")
print(f"Average Restaurant Rating: {average_restaurant_rating:.2f}")
print(f"Average Profit Margin: {average_profit_margin:.2%}")


# ============================================================
# 3. ORDER STATUS ANALYSIS
# ============================================================

status_counts = df["Order_Status"].value_counts()

plt.figure(figsize=(8, 5))

status_counts.plot(kind="bar")

plt.title("Orders by Status")
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    f"{CHART_DIR}/01_order_status.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. MONTHLY ORDER TREND
# ============================================================

monthly_orders = (
    df.dropna(subset=["Order_Date"])
    .groupby(["Order_Year", "Order_Month_Num", "Order_Month"])
    ["Order_ID"]
    .nunique()
    .reset_index()
    .sort_values(["Order_Year", "Order_Month_Num"])
)

plt.figure(figsize=(12, 5))

plt.plot(
    monthly_orders["Order_Month"],
    monthly_orders["Order_ID"],
    marker="o"
)

plt.title("Monthly Order Trend")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    f"{CHART_DIR}/02_monthly_orders.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. CITY ANALYSIS
# ============================================================

city_analysis = (
    df.groupby("City")
    .agg(
        Orders=("Order_ID", "nunique"),
        Order_Value=("Order_Value", "sum"),
        Avg_Order_Value=("Order_Value", "mean"),
        Cancellation_Rate=("Is_Cancelled", "mean")
    )
    .reset_index()
)

city_analysis["Cancellation_Rate"] *= 100

city_analysis = city_analysis.sort_values(
    "Orders",
    ascending=False
)

print("\n" + "-" * 60)
print("CITY PERFORMANCE")
print("-" * 60)

print(city_analysis.to_string(index=False))


plt.figure(figsize=(10, 5))

plt.bar(
    city_analysis["City"],
    city_analysis["Orders"]
)

plt.title("Orders by City")
plt.xlabel("City")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    f"{CHART_DIR}/03_orders_by_city.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. CUISINE ANALYSIS
# ============================================================

cuisine_analysis = (
    df.groupby("Cuisine_Type")
    .agg(
        Orders=("Order_ID", "nunique"),
        Order_Value=("Order_Value", "sum"),
        Avg_Order_Value=("Order_Value", "mean"),
        Avg_Restaurant_Rating=("Restaurant_Rating", "mean")
    )
    .reset_index()
    .sort_values("Orders", ascending=False)
)

print("\n" + "-" * 60)
print("CUISINE PERFORMANCE")
print("-" * 60)

print(cuisine_analysis.to_string(index=False))


plt.figure(figsize=(10, 5))

plt.bar(
    cuisine_analysis["Cuisine_Type"],
    cuisine_analysis["Orders"]
)

plt.title("Orders by Cuisine")
plt.xlabel("Cuisine Type")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    f"{CHART_DIR}/04_orders_by_cuisine.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. DELIVERY PERFORMANCE
# ============================================================

delivery_analysis = (
    df.groupby("Delivery_Speed_Category")
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Delivery_Time=("Delivery_Time_Min", "mean"),
        Avg_Delivery_Rating=("Delivery_Rating", "mean")
    )
    .reset_index()
)

print("\n" + "-" * 60)
print("DELIVERY PERFORMANCE")
print("-" * 60)

print(delivery_analysis.to_string(index=False))


plt.figure(figsize=(10, 5))

plt.bar(
    delivery_analysis["Delivery_Speed_Category"],
    delivery_analysis["Orders"]
)

plt.title("Orders by Delivery Speed")
plt.xlabel("Delivery Speed")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    f"{CHART_DIR}/05_delivery_speed.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. DISTANCE VS DELIVERY TIME
# ============================================================

distance_delivery = (
    df.dropna(
        subset=[
            "Distance_km",
            "Delivery_Time_Min"
        ]
    )
)

plt.figure(figsize=(9, 6))

plt.scatter(
    distance_delivery["Distance_km"],
    distance_delivery["Delivery_Time_Min"],
    alpha=0.3
)

plt.title("Distance vs Delivery Time")
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (minutes)")
plt.tight_layout()

plt.savefig(
    f"{CHART_DIR}/06_distance_vs_delivery_time.png",
    dpi=300
)

plt.close()


# ============================================================
# 9. DISCOUNT ANALYSIS
# ============================================================

discount_analysis = (
    df.groupby("Discount_Category")
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Discount=("Discount_Applied", "mean"),
        Avg_Order_Value=("Order_Value", "mean"),
        Avg_Final_Amount=("Final_Amount", "mean")
    )
    .reset_index()
)

print("\n" + "-" * 60)
print("DISCOUNT ANALYSIS")
print("-" * 60)

print(discount_analysis.to_string(index=False))


# ============================================================
# 10. CUSTOMER ANALYSIS
# ============================================================

customer_analysis = (
    df.groupby("Customer_Type")
    .agg(
        Customers=("Customer_ID", "nunique"),
        Orders=("Order_ID", "nunique"),
        Avg_Order_Value=("Order_Value", "mean")
    )
    .reset_index()
)

print("\n" + "-" * 60)
print("CUSTOMER ANALYSIS")
print("-" * 60)

print(customer_analysis.to_string(index=False))


# ============================================================
# 11. RATINGS ANALYSIS
# ============================================================

rating_analysis = (
    df.groupby("Delivery_Rating_Category")
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Delivery_Time=("Delivery_Time_Min", "mean")
    )
    .reset_index()
)

print("\n" + "-" * 60)
print("DELIVERY RATING ANALYSIS")
print("-" * 60)

print(rating_analysis.to_string(index=False))


# ============================================================
# 12. PROFITABILITY ANALYSIS
# ============================================================

profit_analysis = (
    df.groupby("City")
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Profit_Margin=("Profit_Margin", "mean"),
        Total_Order_Value=("Order_Value", "sum")
    )
    .reset_index()
    .sort_values(
        "Avg_Profit_Margin",
        ascending=False
    )
)

print("\n" + "-" * 60)
print("PROFITABILITY BY CITY")
print("-" * 60)

print(profit_analysis.to_string(index=False))


# ============================================================
# 13. WEEKDAY VS WEEKEND
# ============================================================

day_analysis = (
    df.groupby("Is_Weekend")
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Order_Value=("Order_Value", "mean"),
        Cancellation_Rate=("Is_Cancelled", "mean")
    )
    .reset_index()
)

day_analysis["Cancellation_Rate"] *= 100

print("\n" + "-" * 60)
print("WEEKDAY VS WEEKEND")
print("-" * 60)

print(day_analysis.to_string(index=False))


# ============================================================
# 14. SAVE ANALYSIS TABLES
# ============================================================

city_analysis.to_csv(
    "outputs/tables/city_analysis.csv",
    index=False
)

cuisine_analysis.to_csv(
    "outputs/tables/cuisine_analysis.csv",
    index=False
)

delivery_analysis.to_csv(
    "outputs/tables/delivery_analysis.csv",
    index=False
)

discount_analysis.to_csv(
    "outputs/tables/discount_analysis.csv",
    index=False
)

customer_analysis.to_csv(
    "outputs/tables/customer_analysis.csv",
    index=False
)

profit_analysis.to_csv(
    "outputs/tables/profitability_analysis.csv",
    index=False
)

day_analysis.to_csv(
    "outputs/tables/weekday_weekend_analysis.csv",
    index=False
)


# ============================================================
# 15. SAVE KPI SUMMARY
# ============================================================

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Orders",
        "Delivered Orders",
        "Cancelled Orders",
        "Cancellation Rate",
        "Total Order Value",
        "Total Final Amount",
        "Average Order Value",
        "Average Final Amount",
        "Average Delivery Time",
        "Average Delivery Rating",
        "Average Restaurant Rating",
        "Average Profit Margin"
    ],
    "Value": [
        total_orders,
        delivered_orders,
        cancelled_orders,
        cancellation_rate,
        total_order_value,
        total_final_amount,
        average_order_value,
        average_final_amount,
        average_delivery_time,
        average_delivery_rating,
        average_restaurant_rating,
        average_profit_margin
    ]
})

kpi_summary.to_csv(
    "outputs/tables/kpi_summary.csv",
    index=False
)


# ============================================================
# 16. COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)

print(f"\nCharts saved to: {CHART_DIR}")
print(f"Analysis tables saved to: outputs/tables/")