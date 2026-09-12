from db_connection import load_data


print("=" * 60)
print("TESTING MYSQL CONNECTION")
print("=" * 60)


try:

    df = load_data()

    print("\nMySQL connection successful!")

    print(f"\nRecords loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    print("\nFirst 5 records:")

    print(
        df.head()
    )

    print("\nColumn names:")

    print(
        df.columns.tolist()
    )

    print("\n" + "=" * 60)
    print("DATABASE TEST SUCCESSFUL")
    print("=" * 60)


except Exception as e:

    print("\nDATABASE CONNECTION FAILED")

    print("\nError:")

    print(e)