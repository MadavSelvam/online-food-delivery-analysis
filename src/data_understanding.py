import pandas as pd
from pathlib import Path


# ---------------------------------------------
# 1. Define the file path
# ---------------------------------------------

file_path = Path("data/raw/ONINE_FOOD_DELIVERY_ANALYSIS (1).csv")


# ---------------------------------------------
# 2. Load the dataset
# ---------------------------------------------

df = pd.read_csv(file_path)


# ---------------------------------------------
# 3. Basic dataset information
# ---------------------------------------------

print("\n========== DATASET OVERVIEW ==========")

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# ---------------------------------------------
# 4. Display column names
# ---------------------------------------------

print("\n========== COLUMN NAMES ==========")

for column in df.columns:
    print(column)


# ---------------------------------------------
# 5. Display data types
# ---------------------------------------------

print("\n========== DATA TYPES ==========")

print(df.dtypes)


# ---------------------------------------------
# 6. Check missing values
# ---------------------------------------------

print("\n========== MISSING VALUES ==========")

missing_values = df.isnull().sum()

print(missing_values)


# ---------------------------------------------
# 7. Check duplicate rows
# ---------------------------------------------

print("\n========== DUPLICATES ==========")

duplicates = df.duplicated().sum()

print(f"Duplicate rows : {duplicates}")


# ---------------------------------------------
# 8. Display first 5 records
# ---------------------------------------------

print("\n========== FIRST 5 RECORDS ==========")

print(df.head())