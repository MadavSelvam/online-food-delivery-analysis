import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. Load Dataset
# --------------------------------------------------

file_path = Path("data/raw/ONINE_FOOD_DELIVERY_ANALYSIS (1).csv")

df = pd.read_csv(file_path)


# --------------------------------------------------
# 2. Basic Information
# --------------------------------------------------

print("\n========== DATASET SHAPE ==========")

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# --------------------------------------------------
# 3. Categorical Columns
# --------------------------------------------------

categorical_columns = [
    "Customer_Gender",
    "City",
    "Area",
    "Cuisine_Type",
    "Payment_Mode",
    "Order_Status",
    "Cancellation_Reason",
    "Order_Day",
    "Peak_Hour"
]

print("\n========== CATEGORICAL VALUES ==========")

for column in categorical_columns:

    print(f"\n--- {column} ---")

    print(
        df[column]
        .value_counts(dropna=False)
        .head(20)
    )


# --------------------------------------------------
# 4. Numerical Summary
# --------------------------------------------------

numeric_columns = [
    "Customer_Age",
    "Delivery_Time_Min",
    "Distance_km",
    "Order_Value",
    "Discount_Applied",
    "Final_Amount",
    "Delivery_Rating",
    "Restaurant_Rating",
    "Profit_Margin"
]

print("\n========== NUMERICAL SUMMARY ==========")

print(
    df[numeric_columns]
    .describe()
    .T
)


# --------------------------------------------------
# 5. Negative Values
# --------------------------------------------------

print("\n========== NEGATIVE VALUES ==========")

for column in numeric_columns:

    count = (df[column] < 0).sum()

    print(f"{column}: {count}")


# --------------------------------------------------
# 6. Rating Validation
# --------------------------------------------------

print("\n========== RATING VALIDATION ==========")

print(
    "Delivery ratings outside 1-5:",
    ((df["Delivery_Rating"] < 1) |
     (df["Delivery_Rating"] > 5)).sum()
)

print(
    "Restaurant ratings outside 1-5:",
    ((df["Restaurant_Rating"] < 1) |
     (df["Restaurant_Rating"] > 5)).sum()
)


# --------------------------------------------------
# 7. Customer Age Validation
# --------------------------------------------------

print("\n========== CUSTOMER AGE VALIDATION ==========")

print(
    "Age below 18:",
    (df["Customer_Age"] < 18).sum()
)

print(
    "Age above 100:",
    (df["Customer_Age"] > 100).sum()
)


# --------------------------------------------------
# 8. Cancellation Analysis
# --------------------------------------------------

print("\n========== CANCELLATION ANALYSIS ==========")

print(
    df["Order_Status"]
    .value_counts(dropna=False)
)


cancelled = df["Order_Status"] == "Cancelled"

print(
    "\nCancelled orders:",
    cancelled.sum()
)

print(
    "Cancelled orders without reason:",
    df.loc[
        cancelled,
        "Cancellation_Reason"
    ].isna().sum()
)

print(
    "Delivered orders with cancellation reason:",
    df.loc[
        df["Order_Status"] == "Delivered",
        "Cancellation_Reason"
    ].notna().sum()
)


# --------------------------------------------------
# 9. Financial Validation
# --------------------------------------------------

print("\n========== FINANCIAL VALIDATION ==========")

financial_complete = df[
    ["Order_Value", "Discount_Applied", "Final_Amount"]
].notna().all(axis=1)

calculated_final = (
    df.loc[financial_complete, "Order_Value"]
    - df.loc[financial_complete, "Discount_Applied"]
)

actual_final = df.loc[
    financial_complete,
    "Final_Amount"
]

difference = (
    calculated_final - actual_final
).abs()

print(
    "Records with all financial values:",
    financial_complete.sum()
)

print(
    "Records with calculation mismatch:",
    (difference > 0.01).sum()
)


# --------------------------------------------------
# 10. Negative Final Amount
# --------------------------------------------------

print("\n========== FINAL AMOUNT VALIDATION ==========")

negative_final = df["Final_Amount"] < 0

print(
    "Negative Final Amount records:",
    negative_final.sum()
)

print(
    "\nNegative Final Amount examples:"
)

print(
    df.loc[
        negative_final,
        [
            "Order_ID",
            "Order_Value",
            "Discount_Applied",
            "Final_Amount",
            "Order_Status"
        ]
    ].head(10)
)


# --------------------------------------------------
# 11. Delivery Logic
# --------------------------------------------------

print("\n========== DELIVERY LOGIC ==========")

print(
    "Cancelled orders with delivery time:",
    df.loc[
        cancelled,
        "Delivery_Time_Min"
    ].notna().sum()
)

print(
    "Delivered orders without delivery time:",
    df.loc[
        df["Order_Status"] == "Delivered",
        "Delivery_Time_Min"
    ].isna().sum()
)

print(
    "Cancelled orders with delivery rating:",
    df.loc[
        cancelled,
        "Delivery_Rating"
    ].notna().sum()
)


# --------------------------------------------------
# 12. Date and Time Information
# --------------------------------------------------

print("\n========== DATE / TIME INFORMATION ==========")

print(
    "Missing Order_Date:",
    df["Order_Date"].isna().sum()
)

print(
    "Missing Order_Time:",
    df["Order_Time"].isna().sum()
)

print(
    "Missing Peak_Hour:",
    df["Peak_Hour"].isna().sum()
)


# --------------------------------------------------
# 13. Validation Complete
# --------------------------------------------------

print("\n========== VALIDATION COMPLETE ==========")

print(
    "Data validation completed successfully."
)