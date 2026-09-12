import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

file_path = Path("data/raw/ONINE_FOOD_DELIVERY_ANALYSIS (1).csv")

df = pd.read_csv(file_path)


# ==================================================
# PART 1 — RESTAURANT RATING VALIDATION
# ==================================================

print("\n" + "=" * 60)
print("PART 1 — RESTAURANT RATING VALIDATION")
print("=" * 60)


# Distribution of restaurant ratings

print("\n--- Restaurant Rating Distribution ---")

print(
    df["Restaurant_Rating"]
    .value_counts()
    .sort_index()
)


# Ratings above 5

invalid_rating = df["Restaurant_Rating"] > 5

print("\n--- Ratings Above 5 ---")

print(
    f"Records with rating > 5: {invalid_rating.sum()}"
)

print(
    df.loc[
        invalid_rating,
        ["Restaurant_ID", "Restaurant_Name", "Restaurant_Rating"]
    ]
    .head(20)
)


# Unique invalid ratings

print("\n--- Unique Invalid Ratings ---")

print(
    sorted(
        df.loc[
            invalid_rating,
            "Restaurant_Rating"
        ].unique()
    )
)


# Restaurant-level analysis

print("\n--- Restaurants With Ratings Above 5 ---")

invalid_restaurants = (
    df.loc[invalid_rating]
    .groupby(
        ["Restaurant_ID", "Restaurant_Name"]
    )
    ["Restaurant_Rating"]
    .agg(
        Count="count",
        Min="min",
        Max="max"
    )
    .sort_values(
        "Count",
        ascending=False
    )
)

print(
    invalid_restaurants.head(20)
)


# ==================================================
# PART 2 — FINAL AMOUNT VALIDATION
# ==================================================

print("\n" + "=" * 60)
print("PART 2 — FINAL AMOUNT / DISCOUNT VALIDATION")
print("=" * 60)


# Calculate expected final amount

financial_complete = df[
    [
        "Order_Value",
        "Discount_Applied",
        "Final_Amount"
    ]
].notna().all(axis=1)


df["Calculated_Final_Amount"] = (
    df["Order_Value"]
    - df["Discount_Applied"]
)


# Check negative calculated values

negative_calculated = (
    df["Calculated_Final_Amount"] < 0
)

print("\n--- Negative Calculated Final Amount ---")

print(
    f"Records: {negative_calculated.sum()}"
)


print(
    df.loc[
        negative_calculated,
        [
            "Order_ID",
            "Order_Value",
            "Discount_Applied",
            "Final_Amount",
            "Calculated_Final_Amount",
            "Order_Status"
        ]
    ]
    .head(20)
)


# Check whether negative Final Amount is caused
# by discount exceeding order value

negative_final = df["Final_Amount"] < 0

discount_exceeds_value = (
    df["Discount_Applied"]
    > df["Order_Value"]
)

print("\n--- Negative Final Amount Investigation ---")

print(
    "Negative Final Amount:",
    negative_final.sum()
)

print(
    "Discount > Order Value:",
    discount_exceeds_value.sum()
)

print(
    "Both conditions:",
    (
        negative_final
        & discount_exceeds_value
    ).sum()
)


# ==================================================
# PART 3 — ORDER DATE VALIDATION
# ==================================================

print("\n" + "=" * 60)
print("PART 3 — DATE / ORDER DAY VALIDATION")
print("=" * 60)


# Convert date

df["Parsed_Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)


print("\n--- Date Range ---")

print(
    "Minimum date:",
    df["Parsed_Order_Date"].min()
)

print(
    "Maximum date:",
    df["Parsed_Order_Date"].max()
)


# Missing dates

print("\n--- Missing Dates ---")

print(
    "Missing Order_Date:",
    df["Parsed_Order_Date"].isna().sum()
)


# Derive weekday/weekend

df["Calculated_Order_Day"] = (
    df["Parsed_Order_Date"]
    .dt.dayofweek
    .map(
        lambda x:
        "Weekend"
        if x >= 5
        else "Weekday"
    )
)


# Compare existing vs calculated

date_available = (
    df["Parsed_Order_Date"].notna()
)

order_day_mismatch = (
    date_available
    &
    (
        df["Order_Day"]
        != df["Calculated_Order_Day"]
    )
)

print("\n--- Order Day Consistency ---")

print(
    "Records checked:",
    date_available.sum()
)

print(
    "Order Day mismatches:",
    order_day_mismatch.sum()
)


print(
    df.loc[
        order_day_mismatch,
        [
            "Order_ID",
            "Order_Date",
            "Order_Day",
            "Calculated_Order_Day"
        ]
    ]
    .head(20)
)


# ==================================================
# PART 4 — ORDER TIME VALIDATION
# ==================================================

print("\n" + "=" * 60)
print("PART 4 — ORDER TIME VALIDATION")
print("=" * 60)


print("\n--- Order Time Distribution ---")

print(
    df["Order_Time"]
    .value_counts(dropna=False)
    .head(30)
)


# Number of unique times

print(
    "\nUnique Order_Time values:",
    df["Order_Time"].nunique()
)


# ==================================================
# PART 5 — PEAK HOUR VALIDATION
# ==================================================

print("\n" + "=" * 60)
print("PART 5 — PEAK HOUR VALIDATION")
print("=" * 60)


print("\n--- Peak Hour Distribution ---")

print(
    df["Peak_Hour"]
    .value_counts(dropna=False)
)


# ==================================================
# PART 6 — CLEANUP
# ==================================================

df.drop(
    columns=[
        "Calculated_Final_Amount",
        "Parsed_Order_Date",
        "Calculated_Order_Day"
    ],
    inplace=True
)


print("\n" + "=" * 60)
print("DEEP VALIDATION COMPLETE")
print("=" * 60)