import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/cleaned_food_delivery.csv"
OUTPUT_FILE = "data/processed/analytical_food_delivery.csv"


print("=" * 60)
print("FEATURE ENGINEERING")
print("=" * 60)


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print(f"\nInput dataset shape: {df.shape}")


# ============================================================
# 2. DATE FEATURES
# ============================================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

df["Order_Year"] = df["Order_Date"].dt.year

df["Order_Month_Num"] = df["Order_Date"].dt.month

df["Order_Month"] = df["Order_Date"].dt.month_name()

df["Order_Quarter"] = (
    "Q" + df["Order_Date"].dt.quarter.astype("Int64").astype(str)
)

df["Day_Name"] = df["Order_Date"].dt.day_name()

df["Is_Weekend"] = np.where(
    df["Order_Date"].isna(),
    "Unknown",
    np.where(
        df["Order_Date"].dt.dayofweek >= 5,
        "Yes",
        "No"
    )
)


# ============================================================
# 3. CUSTOMER AGE GROUP
# ============================================================

df["Age_Group"] = pd.cut(
    df["Customer_Age"],
    bins=[17, 25, 35, 45, 55, 100],
    labels=[
        "18-25",
        "26-35",
        "36-45",
        "46-55",
        "56+"
    ]
)

df["Age_Group"] = df["Age_Group"].astype("object")

df["Age_Group"] = df["Age_Group"].fillna("Unknown")


# ============================================================
# 4. DISTANCE CATEGORY
# ============================================================

df["Distance_Category"] = pd.cut(
    df["Distance_km"],
    bins=[0, 5, 15, 25, 40],
    labels=[
        "Short (0-5 km)",
        "Medium (6-15 km)",
        "Long (16-25 km)",
        "Very Long (26-40 km)"
    ]
)

df["Distance_Category"] = (
    df["Distance_Category"]
    .astype("object")
    .fillna("Unknown")
)


# ============================================================
# 5. DELIVERY SPEED CATEGORY
# ============================================================

df["Delivery_Speed_Category"] = pd.cut(
    df["Delivery_Time_Min"],
    bins=[0, 60, 120, 180, 300],
    labels=[
        "Fast (≤60 min)",
        "Moderate (61-120 min)",
        "Slow (121-180 min)",
        "Very Slow (>180 min)"
    ]
)

df["Delivery_Speed_Category"] = (
    df["Delivery_Speed_Category"]
    .astype("object")
    .fillna("Unknown")
)


# ============================================================
# 6. DISCOUNT CATEGORY
# ============================================================

df["Discount_Category"] = pd.cut(
    df["Discount_Applied"],
    bins=[-0.01, 0, 50, 100, 300],
    labels=[
        "No Discount",
        "Low Discount",
        "Medium Discount",
        "High Discount"
    ]
)

df["Discount_Category"] = (
    df["Discount_Category"]
    .astype("object")
    .fillna("Unknown")
)


# ============================================================
# 7. DISCOUNT PERCENTAGE
# ============================================================

df["Discount_Percentage"] = np.where(
    (df["Order_Value"].notna()) &
    (df["Order_Value"] > 0) &
    (df["Discount_Applied"].notna()),
    (df["Discount_Applied"] / df["Order_Value"]) * 100,
    np.nan
)


# ============================================================
# 8. ORDER VALUE CATEGORY
# ============================================================

df["Order_Value_Category"] = pd.cut(
    df["Order_Value"],
    bins=[0, 1000, 2500, 4000, 5000],
    labels=[
        "Low (≤1000)",
        "Medium (1001-2500)",
        "High (2501-4000)",
        "Very High (>4000)"
    ]
)

df["Order_Value_Category"] = (
    df["Order_Value_Category"]
    .astype("object")
    .fillna("Unknown")
)


# ============================================================
# 9. ORDER STATUS FLAGS
# ============================================================

df["Is_Delivered"] = np.where(
    df["Order_Status"] == "Delivered",
    1,
    0
)

df["Is_Cancelled"] = np.where(
    df["Order_Status"] == "Cancelled",
    1,
    0
)


# ============================================================
# 10. CUSTOMER ORDER FREQUENCY
# ============================================================

customer_order_counts = (
    df.groupby("Customer_ID")["Order_ID"]
    .transform("count")
)

df["Customer_Order_Count"] = customer_order_counts


# ============================================================
# 11. CUSTOMER TYPE
# ============================================================

df["Customer_Type"] = np.where(
    df["Customer_Order_Count"] == 1,
    "One-Time Customer",
    "Repeat Customer"
)


# ============================================================
# 12. DELIVERY RATING CATEGORY
# ============================================================

df["Delivery_Rating_Category"] = pd.cut(
    df["Delivery_Rating"],
    bins=[0, 2, 3, 4, 5],
    labels=[
        "Low (1-2)",
        "Average (3)",
        "Good (4)",
        "Excellent (5)"
    ]
)

df["Delivery_Rating_Category"] = (
    df["Delivery_Rating_Category"]
    .astype("object")
    .fillna("Unknown")
)


# ============================================================
# 13. RESTAURANT RATING CATEGORY
# ============================================================

df["Restaurant_Rating_Category"] = pd.cut(
    df["Restaurant_Rating"],
    bins=[0, 3, 4, 5],
    labels=[
        "Low (≤3)",
        "Good (>3-4)",
        "Excellent (>4-5)"
    ]
)

df["Restaurant_Rating_Category"] = (
    df["Restaurant_Rating_Category"]
    .astype("object")
    .fillna("Unknown")
)


# ============================================================
# 14. DATASET SUMMARY
# ============================================================

print("\n--- New Features Created ---")

original_columns = pd.read_csv(INPUT_FILE, nrows=1).columns.tolist()

new_columns = [
    column for column in df.columns
    if column not in original_columns
]

for column in new_columns:
    print(f"- {column}")

print(f"\nNumber of new features: {len(new_columns)}")


# ============================================================
# 15. FEATURE SUMMARY
# ============================================================

print("\n--- Feature Distribution ---")

print("\nCustomer Type:")
print(df["Customer_Type"].value_counts())

print("\nDistance Category:")
print(df["Distance_Category"].value_counts())

print("\nDelivery Speed Category:")
print(df["Delivery_Speed_Category"].value_counts())

print("\nDiscount Category:")
print(df["Discount_Category"].value_counts())

print("\nOrder Value Category:")
print(df["Order_Value_Category"].value_counts())


# ============================================================
# 16. SAVE ANALYTICAL DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 60)

print(f"\nFinal dataset shape: {df.shape}")
print(f"Output file: {OUTPUT_FILE}")

print("\nAnalytical dataset saved successfully.")