import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


# ============================================================
# CONFIGURATION
# ============================================================

CSV_FILE = "data/processed/analytical_food_delivery.csv"

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "12345"
DB_NAME = "online_food_delivery"

TABLE_NAME = "food_delivery_orders"


# ============================================================
# START
# ============================================================

print("=" * 60)
print("LOADING DATA INTO MYSQL")
print("=" * 60)


# ============================================================
# 1. LOAD CSV
# ============================================================

df = pd.read_csv(CSV_FILE)

print(f"\nCSV records: {len(df):,}")
print(f"CSV columns: {len(df.columns)}")


# ============================================================
# 2. PREPARE DATE COLUMN
# ============================================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
).dt.date


# ============================================================
# 3. CREATE MYSQL CONNECTION
# ============================================================

try:

    encoded_password = quote_plus(DB_PASSWORD)

    connection_string = (
        f"mysql+mysqlconnector://"
        f"{DB_USER}:{encoded_password}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    engine = create_engine(
        connection_string
    )

    # Test connection
    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    @@hostname,
                    @@port,
                    DATABASE(),
                    USER()
            """)
        )

        details = result.fetchone()

        print("\nPython MySQL connection details:")
        print(details)

        print("\nConnected to MySQL successfully.")


    # ========================================================
    # 4. CLEAR EXISTING DATA
    # ========================================================

    with engine.begin() as connection:

        connection.execute(
            text(
                f"TRUNCATE TABLE {TABLE_NAME}"
            )
        )

    print("\nExisting table data cleared.")


    # ========================================================
    # 5. LOAD DATA USING PANDAS
    # ========================================================

    print("\nStarting data import...")

    df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi"
    )

    print("\nData import completed.")


    # ========================================================
    # 6. VERIFY RECORD COUNT
    # ========================================================

    with engine.connect() as connection:

        result = connection.execute(
            text(
                f"SELECT COUNT(*) FROM {TABLE_NAME}"
            )
        )

        count = result.scalar()


    # ========================================================
    # 7. FINAL RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("MYSQL DATA LOAD COMPLETE")
    print("=" * 60)

    print(
        f"\nCSV records: {len(df):,}"
    )

    print(
        f"Records in MySQL: {count:,}"
    )

    if count == len(df):

        print(
            "\nSUCCESS: All 100,000 records loaded correctly."
        )

    else:

        print(
            "\nWARNING: Record count does not match."
        )

        print(
            f"Expected: {len(df):,}"
        )

        print(
            f"Found: {count:,}"
        )


    # ========================================================
    # 8. VERIFY NULL VALUES
    # ========================================================

    print("\n--- NULL Verification ---")

    with engine.connect() as connection:

        result = connection.execute(
            text(f"""
                SELECT
                    COUNT(*) AS total_records,
                    COUNT(Customer_Age) AS age_available,
                    COUNT(Order_Value) AS order_value_available,
                    COUNT(Discount_Applied) AS discount_available,
                    COUNT(Final_Amount) AS final_amount_available,
                    COUNT(Restaurant_Rating) AS restaurant_rating_available
                FROM {TABLE_NAME}
            """)
        )

        null_check = result.fetchone()

        print(
            f"Total records: {null_check[0]:,}"
        )

        print(
            f"Customer Age available: {null_check[1]:,}"
        )

        print(
            f"Order Value available: {null_check[2]:,}"
        )

        print(
            f"Discount available: {null_check[3]:,}"
        )

        print(
            f"Final Amount available: {null_check[4]:,}"
        )

        print(
            f"Restaurant Rating available: "
            f"{null_check[5]:,}"
        )


    engine.dispose()

    print("\nMySQL connection closed.")


except Exception as e:

    print("\nERROR:")
    print(e)