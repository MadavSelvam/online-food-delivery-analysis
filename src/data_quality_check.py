import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/processed/cleaned_food_delivery.csv"


print("=" * 60)
print("FINAL DATA QUALITY CHECK")
print("=" * 60)


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print(f"\nDataset shape: {df.shape}")


# ============================================================
# 2. DUPLICATE CHECK
# ============================================================

duplicates = df.duplicated().sum()

print("\n--- Duplicate Check ---")
print(f"Duplicate rows: {duplicates}")


# ============================================================
# 3. MISSING VALUE CHECK
# ============================================================

print("\n--- Missing Values ---")

missing = df.isna().sum()

missing = missing[missing > 0].sort_values(ascending=False)

if len(missing) > 0:
    print(missing)
else:
    print("No missing values found.")


# ============================================================
# 4. RESTAURANT RATING VALIDATION
# ============================================================

invalid_restaurant_rating = (
    (df["Restaurant_Rating"] < 1) |
    (df["Restaurant_Rating"] > 5)
).sum()

print("\n--- Restaurant Rating Check ---")
print(f"Invalid Restaurant Ratings: {invalid_restaurant_rating}")


# ============================================================
# 5. DELIVERY RATING VALIDATION
# ============================================================

invalid_delivery_rating = (
    (df["Delivery_Rating"] < 1) |
    (df["Delivery_Rating"] > 5)
).sum()

print("\n--- Delivery Rating Check ---")
print(f"Invalid Delivery Ratings: {invalid_delivery_rating}")


# ============================================================
# 6. FINAL AMOUNT VALIDATION
# ============================================================

negative_final_amount = (df["Final_Amount"] < 0).sum()

print("\n--- Final Amount Check ---")
print(f"Negative Final Amounts: {negative_final_amount}")


# ============================================================
# 7. FINANCIAL CALCULATION CHECK
# ============================================================

financial_records = (
    df["Order_Value"].notna() &
    df["Discount_Applied"].notna() &
    df["Final_Amount"].notna()
)

expected_final_amount = (
    df.loc[financial_records, "Order_Value"] -
    df.loc[financial_records, "Discount_Applied"]
).clip(lower=0)

actual_final_amount = df.loc[
    financial_records,
    "Final_Amount"
]

financial_mismatches = (
    ~np.isclose(
        expected_final_amount,
        actual_final_amount,
        atol=0.01
    )
).sum()

print("\n--- Financial Calculation Check ---")
print(f"Financial records checked: {financial_records.sum()}")
print(f"Final Amount mismatches: {financial_mismatches}")


# ============================================================
# 8. CUSTOMER AGE VALIDATION
# ============================================================

invalid_age = (
    (df["Customer_Age"] < 18) |
    (df["Customer_Age"] > 100)
).sum()

print("\n--- Customer Age Check ---")
print(f"Invalid Customer Ages: {invalid_age}")


# ============================================================
# 9. DELIVERY TIME VALIDATION
# ============================================================

invalid_delivery_time = (
    (df["Delivery_Time_Min"] < 0)
).sum()

print("\n--- Delivery Time Check ---")
print(f"Negative Delivery Times: {invalid_delivery_time}")


# ============================================================
# 10. DISTANCE VALIDATION
# ============================================================

invalid_distance = (
    (df["Distance_km"] < 0)
).sum()

print("\n--- Distance Check ---")
print(f"Negative Distances: {invalid_distance}")


# ============================================================
# 11. ORDER VALUE VALIDATION
# ============================================================

invalid_order_value = (
    (df["Order_Value"] < 0)
).sum()

print("\n--- Order Value Check ---")
print(f"Negative Order Values: {invalid_order_value}")


# ============================================================
# 12. DISCOUNT VALIDATION
# ============================================================

invalid_discount = (
    (df["Discount_Applied"] < 0)
).sum()

print("\n--- Discount Check ---")
print(f"Negative Discounts: {invalid_discount}")


# ============================================================
# 13. ORDER STATUS VALIDATION
# ============================================================

print("\n--- Order Status ---")
print(df["Order_Status"].value_counts(dropna=False))


# ============================================================
# 14. CATEGORICAL VALIDATION
# ============================================================

print("\n--- Categorical Values ---")

categorical_columns = [
    "Customer_Gender",
    "City",
    "Area",
    "Cuisine_Type",
    "Payment_Mode"
]

for column in categorical_columns:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False))


# ============================================================
# 15. ORDER DAY VALIDATION
# ============================================================

valid_dates = df["Order_Date"].notna()

calculated_order_day = np.where(
    pd.to_datetime(df["Order_Date"]).dt.dayofweek < 5,
    "Weekday",
    "Weekend"
)

order_day_mismatches = (
    valid_dates &
    (df["Order_Day"] != calculated_order_day)
).sum()

print("\n--- Order Day Check ---")
print(f"Order Day mismatches: {order_day_mismatches}")


# ============================================================
# 16. DATE RANGE
# ============================================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print("\n--- Order Date Range ---")
print(f"Minimum Date: {df['Order_Date'].min()}")
print(f"Maximum Date: {df['Order_Date'].max()}")


# ============================================================
# 17. PROFIT MARGIN CHECK
# ============================================================

invalid_profit_margin = (
    (df["Profit_Margin"] < -1) |
    (df["Profit_Margin"] > 1)
).sum()

print("\n--- Profit Margin Check ---")
print(f"Invalid Profit Margin values: {invalid_profit_margin}")


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("FINAL DATA QUALITY CHECK COMPLETE")
print("=" * 60)     