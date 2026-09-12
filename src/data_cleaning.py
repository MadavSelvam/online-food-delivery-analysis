import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "data/raw/ONINE_FOOD_DELIVERY_ANALYSIS (1).csv"
OUTPUT_FILE = "data/processed/cleaned_food_delivery.csv"


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 60)
print("DATA CLEANING")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)

print(f"\nOriginal dataset shape: {df.shape}")


# ============================================================
# 2. REMOVE DUPLICATE ROWS
# ============================================================

duplicate_count = df.duplicated().sum()

print(f"\nDuplicate rows found: {duplicate_count}")

if duplicate_count > 0:
    df = df.drop_duplicates()

print(f"Shape after duplicate removal: {df.shape}")


# ============================================================
# 3. STANDARDIZE MISSING CATEGORICAL VALUES
# ============================================================

categorical_columns = [
    "Customer_Gender",
    "City",
    "Area",
    "Cuisine_Type",
    "Payment_Mode"
]

for column in categorical_columns:
    df[column] = df[column].fillna("Unknown")


# ============================================================
# 4. HANDLE CANCELLATION REASON
# ============================================================

df.loc[
    (df["Order_Status"] == "Delivered") &
    (df["Cancellation_Reason"].isna()),
    "Cancellation_Reason"
] = "Not Applicable"

df.loc[
    (df["Order_Status"] == "Cancelled") &
    (df["Cancellation_Reason"].isna()),
    "Cancellation_Reason"
] = "Unknown"


# ============================================================
# 5. HANDLE INVALID RESTAURANT RATINGS
# ============================================================

invalid_restaurant_ratings = (
    (df["Restaurant_Rating"] < 1) |
    (df["Restaurant_Rating"] > 5)
)

invalid_count = invalid_restaurant_ratings.sum()

print(f"\nInvalid Restaurant Ratings: {invalid_count}")

df.loc[invalid_restaurant_ratings, "Restaurant_Rating"] = np.nan


# ============================================================
# 6. CORRECT NEGATIVE FINAL AMOUNTS
# ============================================================

negative_final_amount = df["Final_Amount"] < 0

negative_count = negative_final_amount.sum()

print(f"Negative Final Amount records: {negative_count}")

# Recalculate only when Order Value and Discount are available
recalculable = (
    negative_final_amount &
    df["Order_Value"].notna() &
    df["Discount_Applied"].notna()
)

df.loc[recalculable, "Final_Amount"] = (
    df.loc[recalculable, "Order_Value"] -
    df.loc[recalculable, "Discount_Applied"]
).clip(lower=0)


# ============================================================
# 7. VALIDATE FINAL AMOUNT
# ============================================================

financial_records = (
    df["Order_Value"].notna() &
    df["Discount_Applied"].notna()
)

df.loc[financial_records, "Final_Amount"] = (
    df.loc[financial_records, "Order_Value"] -
    df.loc[financial_records, "Discount_Applied"]
).clip(lower=0)


# ============================================================
# 8. KEEP MISSING DISCOUNTS AS MISSING
# ============================================================

# Missing discounts cannot be reliably derived from the
# available financial fields, so they are intentionally retained
# as missing values.

missing_discount = df["Discount_Applied"].isna().sum()

print(f"\nMissing Discount records retained: {missing_discount}")


# ============================================================
# 9. DATE VALIDATION
# ============================================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print(
    f"Order Date range: "
    f"{df['Order_Date'].min()} to {df['Order_Date'].max()}"
)


# ============================================================
# 10. VALIDATE ORDER DAY
# ============================================================

valid_dates = df["Order_Date"].notna()

calculated_order_day = np.where(
    df["Order_Date"].dt.dayofweek < 5,
    "Weekday",
    "Weekend"
)

order_day_mismatch = (
    valid_dates &
    (df["Order_Day"] != calculated_order_day)
).sum()

print(f"Order Day mismatches: {order_day_mismatch}")


# ============================================================
# 11. ORDER TIME VALIDATION
# ============================================================

# Order_Time contains mostly 0:00 values and therefore should
# not be used for detailed hour-of-day analysis.

print(
    f"\nUnique non-null Order Time values: "
    f"{df['Order_Time'].dropna().nunique()}"
)

print(
    f"Missing Order Time: "
    f"{df['Order_Time'].isna().sum()}"
)


# ============================================================
# 12. SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETE")
print("=" * 60)

print(f"\nCleaned dataset shape: {df.shape}")
print(f"Output file: {OUTPUT_FILE}")

print("\nRemaining missing values:")
print(df.isna().sum())

print("\nCleaned dataset saved successfully.")