import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

TABLE_NAME = "food_delivery_orders"


# ============================================================
# CREATE DATABASE CONNECTION
# ============================================================

def get_engine():

    # Read database credentials from Streamlit secrets
    db_host = st.secrets["DB_HOST"]
    db_port = st.secrets["DB_PORT"]
    db_user = st.secrets["DB_USER"]
    db_password = st.secrets["DB_PASSWORD"]
    db_name = st.secrets["DB_NAME"]

    # Encode password to handle special characters
    encoded_password = quote_plus(str(db_password))

    # MySQL connection string
    connection_string = (
        f"mysql+mysqlconnector://"
        f"{db_user}:{encoded_password}@"
        f"{db_host}:{db_port}/"
        f"{db_name}"
    )

    # Create SQLAlchemy engine
    engine = create_engine(
        connection_string,
        pool_pre_ping=True
    )

    return engine


# ============================================================
# LOAD DATA FROM MYSQL
# ============================================================

def load_data():

    engine = get_engine()

    query = f"""
        SELECT *
        FROM {TABLE_NAME}
    """

    try:

        df = pd.read_sql(query, engine)

        return df

    finally:

        engine.dispose()


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

def test_connection():

    try:

        engine = get_engine()

        with engine.connect() as connection:
            connection.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )

        engine.dispose()

        return True, "MySQL connection successful."

    except Exception as e:

        return False, f"MySQL connection failed: {e}"