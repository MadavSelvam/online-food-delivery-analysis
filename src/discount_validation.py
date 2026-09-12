import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

file_path = Path(
    "data/raw/ONINE_FOOD_DELIVERY_ANALYSIS (1).csv"
)

df = pd.read_csv(file_path)


# --------------------------------------------------
# 2. Basic Discount Distribution
# --------------------------------------------------

print("\n" + "=" * 60)
print("DISCOUNT VALIDATION")
print("=" * 60)

print("\n--- Discount Distribution ---")

print(
    df["Discount_Applied"]
    .value_counts(dropna=False)
    .sort_index()
)


# --------------------------------------------------
# 3. Missing Discount Records
# --------------------------------------------------

missing_discount = df["Discount_Applied"].isna()

print("\n--- Missing Discount ---")

print(
    "Missing Discount:",
    missing_discount.sum()
)


# --------------------------------------------------
# 4. Missing Discount + Financial Fields
# --------------------------------------------------

print("\n--- Missing Discount With Financial Values ---")

print(
    "Missing Discount + Order Value available:",
    (
        missing_discount
        & df["Order_Value"].notna()
    ).sum()
)

print(
    "Missing Discount + Final Amount available:",
    (
        missing_discount
        & df["Final_Amount"].notna()
    ).sum()
)


# --------------------------------------------------
# 5. Compare Final Amount and Order Value
# --------------------------------------------------

print("\n--- Missing Discount Relationship ---")

comparison = df.loc[
    missing_discount
    & df["Order_Value"].notna()
    & df["Final_Amount"].notna(),
    [
        "Order_ID",
        "Order_Value",
        "Discount_Applied",
        "Final_Amount",
        "Order_Status"
    ]
]

print(comparison.head(20))


# --------------------------------------------------
# 6. Check Whether Final Amount = Order Value
# --------------------------------------------------

same_amount = (
    comparison["Order_Value"]
    == comparison["Final_Amount"]
)

print(
    "\nRecords where Order Value = Final Amount:",
    same_amount.sum()
)

print(
    "Records where Order Value != Final Amount:",
    (~same_amount).sum()
)


# --------------------------------------------------
# 7. Missing Discount by Order Status
# --------------------------------------------------

print("\n--- Missing Discount by Order Status ---")

print(
    df.loc[missing_discount]
    ["Order_Status"]
    .value_counts()
)


# --------------------------------------------------
# 8. Missing Discount by Final Amount Availability
# --------------------------------------------------

print("\n--- Missing Discount / Final Amount ---")

print(
    pd.crosstab(
        missing_discount,
        df["Final_Amount"].isna()
    )
)


# --------------------------------------------------
# 9. Complete
# --------------------------------------------------

print("\n" + "=" * 60)
print("DISCOUNT VALIDATION COMPLETE")
print("=" * 60)