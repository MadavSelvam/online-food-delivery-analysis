# ============================================================
# ONLINE FOOD DELIVERY ANALYTICS DASHBOARD
# ============================================================
# Technologies:
# Python | Pandas | Streamlit | Plotly | MySQL
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from db_connection import load_data


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Online Food Delivery Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GENERAL
       ====================================================== */

    .main {
        padding-top: 1rem;
    }

    h1 {
        font-weight: 700;
        margin-bottom: 5px;
    }

    h2 {
        margin-top: 1rem;
    }


    /* ======================================================
       KPI CARDS
       ====================================================== */

    div[data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.20);
        min-height: 105px;
    }

    div[data-testid="stMetric"] label {
        color: #d1d5db !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }


    /* ======================================================
       BUSINESS INSIGHT BOXES
       ====================================================== */

    .insight-box {
        padding: 18px;
        border-radius: 10px;
        background-color: #1f2937;
        border-left: 5px solid #60a5fa;
        margin-bottom: 15px;
        line-height: 1.6;
    }


    /* ======================================================
       DATA QUALITY BOXES
       ====================================================== */

    .quality-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1f2937;
        border: 1px solid #374151;
        margin-bottom: 10px;
        line-height: 1.6;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA FROM MYSQL
# ============================================================

@st.cache_data(ttl=300)
def get_mysql_data():

    return load_data()


try:

    df = get_mysql_data()

except Exception as e:

    st.error(
        "Unable to connect to the MySQL database."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

# Convert date
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)


# Numeric columns
numeric_columns = [
    "Customer_Age",
    "Delivery_Time_Min",
    "Distance_km",
    "Order_Value",
    "Discount_Applied",
    "Final_Amount",
    "Delivery_Rating",
    "Restaurant_Rating",
    "Profit_Margin",
    "Discount_Percentage",
    "Is_Delivered",
    "Is_Cancelled",
    "Customer_Order_Count"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# Categorical columns
categorical_columns = [
    "City",
    "Area",
    "Restaurant_Name",
    "Restaurant_ID",
    "Cuisine_Type",
    "Payment_Mode",
    "Order_Status",
    "Cancellation_Reason",
    "Order_Day",
    "Order_Month",
    "Order_Quarter",
    "Age_Group",
    "Distance_Category",
    "Delivery_Speed_Category",
    "Discount_Category",
    "Order_Value_Category",
    "Customer_Type",
    "Delivery_Rating_Category",
    "Restaurant_Rating_Category"
]


for column in categorical_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
        )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_currency(value):

    if pd.isna(value):

        return "₹0"

    return f"₹{value:,.0f}"


def format_number(value):

    if pd.isna(value):

        return "0"

    return f"{value:,.0f}"


def format_percentage(value):

    if pd.isna(value):

        return "0.00%"

    return f"{value:.2f}%"


def calculate_cancellation_rate(data):

    if len(data) == 0:

        return 0

    return (
        (
            data["Order_Status"] == "Cancelled"
        ).sum()
        / len(data)
        * 100
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🍔 Dashboard Filters")

st.sidebar.markdown("---")


# ============================================================
# CITY FILTER
# ============================================================

city_options = sorted(
    df["City"]
    .dropna()
    .unique()
    .tolist()
)

selected_city = st.sidebar.multiselect(
    "City",
    options=city_options,
    default=[]
)


# ============================================================
# CUISINE FILTER
# ============================================================

cuisine_options = sorted(
    df["Cuisine_Type"]
    .dropna()
    .unique()
    .tolist()
)

selected_cuisine = st.sidebar.multiselect(
    "Cuisine Type",
    options=cuisine_options,
    default=[]
)


# ============================================================
# STATUS FILTER
# ============================================================

status_options = sorted(
    df["Order_Status"]
    .dropna()
    .unique()
    .tolist()
)

selected_status = st.sidebar.multiselect(
    "Order Status",
    options=status_options,
    default=[]
)


# ============================================================
# YEAR FILTER
# ============================================================

year_options = sorted(
    df["Order_Year"]
    .dropna()
    .unique()
    .tolist()
)

selected_year = st.sidebar.multiselect(
    "Order Year",
    options=year_options,
    default=[]
)


# ============================================================
# MONTH FILTER
# ============================================================

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


available_months = [
    month
    for month in month_order
    if month in df["Order_Month"].unique()
]


selected_month = st.sidebar.multiselect(
    "Order Month",
    options=available_months,
    default=[]
)


# ============================================================
# DISCOUNT FILTER
# ============================================================

discount_options = sorted(
    df["Discount_Category"]
    .dropna()
    .unique()
    .tolist()
)


selected_discount = st.sidebar.multiselect(
    "Discount Category",
    options=discount_options,
    default=[]
)


# ============================================================
# DISTANCE FILTER
# ============================================================

distance_order = [
    "Short (0-5 km)",
    "Medium (6-15 km)",
    "Long (16-25 km)",
    "Very Long (26-40 km)",
    "Unknown"
]


available_distance = [
    value
    for value in distance_order
    if value in df["Distance_Category"].unique()
]


selected_distance = st.sidebar.multiselect(
    "Distance Category",
    options=available_distance,
    default=[]
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_city:

    filtered_df = filtered_df[
        filtered_df["City"].isin(selected_city)
    ]


if selected_cuisine:

    filtered_df = filtered_df[
        filtered_df["Cuisine_Type"].isin(
            selected_cuisine
        )
    ]


if selected_status:

    filtered_df = filtered_df[
        filtered_df["Order_Status"].isin(
            selected_status
        )
    ]


if selected_year:

    filtered_df = filtered_df[
        filtered_df["Order_Year"].isin(
            selected_year
        )
    ]


if selected_month:

    filtered_df = filtered_df[
        filtered_df["Order_Month"].isin(
            selected_month
        )
    ]


if selected_discount:

    filtered_df = filtered_df[
        filtered_df["Discount_Category"].isin(
            selected_discount
        )
    ]


if selected_distance:

    filtered_df = filtered_df[
        filtered_df["Distance_Category"].isin(
            selected_distance
        )
    ]


# ============================================================
# HEADER
# ============================================================

st.title(
    "🍔 Online Food Delivery Analytics"
)

st.markdown(
    "### Interactive Business Intelligence Dashboard"
)

st.success(
    f"🟢 Data Source: MySQL | "
    f"Database: online_food_delivery | "
    f"Records: {len(df):,}"
)

st.caption(
    "Analyze orders, revenue, cancellations, "
    "delivery performance and profitability."
)


# ============================================================
# FILTER STATUS
# ============================================================

if len(filtered_df) == len(df):

    st.info(
        f"Showing all **{len(df):,}** orders."
    )

else:

    st.info(
        f"Showing **{len(filtered_df):,}** "
        f"of **{len(df):,}** orders based on "
        f"selected filters."
    )


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Dashboard Pages",
    [
        "📊 Executive Overview",
        "🚚 Operations & Delivery",
        "💰 Revenue & Profitability"
    ]
)


# ============================================================
# ============================================================
# PAGE 1 — EXECUTIVE OVERVIEW
# ============================================================
# ============================================================

if page == "📊 Executive Overview":

    st.header(
        "Executive Overview"
    )

    st.write(
        "High-level view of business performance."
    )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_orders = len(filtered_df)

    delivered_orders = (
        filtered_df["Order_Status"]
        == "Delivered"
    ).sum()

    cancelled_orders = (
        filtered_df["Order_Status"]
        == "Cancelled"
    ).sum()

    cancel_rate = calculate_cancellation_rate(
        filtered_df
    )

    total_order_value = (
        filtered_df["Order_Value"].sum()
    )

    avg_order_value = (
        filtered_df["Order_Value"].mean()
    )

    avg_delivery_time = (
        filtered_df["Delivery_Time_Min"].mean()
    )

    avg_profit_margin = (
        filtered_df["Profit_Margin"].mean()
        * 100
    )


    # ========================================================
    # KPI ROW 1
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Orders",
        format_number(total_orders)
    )


    col2.metric(
        "Delivered Orders",
        format_number(delivered_orders)
    )


    col3.metric(
        "Cancelled Orders",
        format_number(cancelled_orders)
    )


    col4.metric(
        "Cancellation Rate",
        format_percentage(cancel_rate)
    )


    # ========================================================
    # KPI ROW 2
    # ========================================================

    col5, col6, col7, col8 = st.columns(4)


    col5.metric(
        "Total Order Value",
        format_currency(total_order_value)
    )


    col6.metric(
        "Average Order Value",
        format_currency(avg_order_value)
    )


    col7.metric(
        "Avg Delivery Time",
        (
            f"{avg_delivery_time:.2f} min"
            if not pd.isna(avg_delivery_time)
            else "N/A"
        )
    )


    col8.metric(
        "Avg Profit Margin",
        format_percentage(avg_profit_margin)
    )


    st.markdown("---")


    # ========================================================
    # MONTHLY ORDER TREND
    # ========================================================

    st.subheader(
        "📈 Monthly Order Trend"
    )


    monthly_df = (
        filtered_df[
            filtered_df["Order_Month"].isin(
                month_order
            )
        ]
        .groupby(
            [
                "Order_Year",
                "Order_Month_Num",
                "Order_Month"
            ],
            as_index=False
        )
        .agg(
            Total_Orders=(
                "Order_ID",
                "count"
            ),
            Total_Order_Value=(
                "Order_Value",
                "sum"
            )
        )
        .sort_values(
            [
                "Order_Year",
                "Order_Month_Num"
            ]
        )
    )


    if not monthly_df.empty:

        monthly_df["Month_Label"] = (
            monthly_df["Order_Month"]
            + " "
            + monthly_df["Order_Year"]
            .astype(int)
            .astype(str)
        )


        fig = px.line(
            monthly_df,
            x="Month_Label",
            y="Total_Orders",
            markers=True,
            title="Monthly Orders",
            hover_data={
                "Total_Orders": ":,.0f",
                "Total_Order_Value": ":,.0f"
            }
        )


        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Orders",
            height=450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # CITY ANALYSIS
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # ORDER VALUE BY CITY
    # ========================================================

    with col1:

        st.subheader(
            "🏙️ Order Value by City"
        )


        city_df = (
            filtered_df
            .groupby(
                "City",
                as_index=False
            )
            .agg(
                Total_Order_Value=(
                    "Order_Value",
                    "sum"
                ),
                Total_Orders=(
                    "Order_ID",
                    "count"
                )
            )
            .sort_values(
                "Total_Order_Value",
                ascending=False
            )
        )


        fig = px.bar(
            city_df,
            x="City",
            y="Total_Order_Value",
            title="Total Order Value by City",
            hover_data={
                "Total_Order_Value": ":,.0f",
                "Total_Orders": ":,.0f"
            }
        )


        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Order Value (₹)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # CANCELLATION RATE BY CITY
    # ========================================================

    with col2:

        st.subheader(
            "❌ Cancellation Rate by City"
        )


        city_cancel = (
            filtered_df
            .groupby("City")
            .agg(
                Total_Orders=(
                    "Order_ID",
                    "count"
                ),
                Cancelled_Orders=(
                    "Is_Cancelled",
                    "sum"
                )
            )
            .reset_index()
        )


        city_cancel[
            "Cancellation_Rate"
        ] = (
            city_cancel["Cancelled_Orders"]
            / city_cancel["Total_Orders"]
            * 100
        )


        city_cancel = (
            city_cancel
            .sort_values(
                "Cancellation_Rate",
                ascending=False
            )
        )


        fig = px.bar(
            city_cancel,
            x="City",
            y="Cancellation_Rate",
            title="Cancellation Rate by City",
            hover_data={
                "Total_Orders": ":,.0f",
                "Cancelled_Orders": ":,.0f",
                "Cancellation_Rate": ":.2f"
            }
        )


        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Cancellation Rate (%)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # ORDER STATUS
    # ========================================================

    st.subheader(
        "📦 Order Status Distribution"
    )


    status_df = (
        filtered_df
        .groupby("Order_Status")
        .size()
        .reset_index(
            name="Orders"
        )
    )


    fig = px.pie(
        status_df,
        names="Order_Status",
        values="Orders",
        hole=0.45,
        title="Delivered vs Cancelled Orders"
    )


    fig.update_traces(
        textinfo="percent+label"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # DYNAMIC BUSINESS INSIGHTS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "💡 Key Business Insights"
    )


    if not filtered_df.empty:

        # ----------------------------------------------------
        # Highest Revenue City
        # ----------------------------------------------------

        revenue_by_city = (
            filtered_df
            .groupby("City")["Order_Value"]
            .sum()
        )


        highest_revenue_city = (
            revenue_by_city.idxmax()
        )


        highest_revenue_value = (
            revenue_by_city.max()
        )


        # ----------------------------------------------------
        # Highest Cancellation City
        # ----------------------------------------------------

        cancellation_by_city = (
            filtered_df
            .groupby("City")
            .agg(
                Orders=(
                    "Order_ID",
                    "count"
                ),
                Cancelled=(
                    "Is_Cancelled",
                    "sum"
                )
            )
        )


        cancellation_by_city[
            "Rate"
        ] = (
            cancellation_by_city["Cancelled"]
            / cancellation_by_city["Orders"]
            * 100
        )


        highest_cancel_city = (
            cancellation_by_city[
                "Rate"
            ].idxmax()
        )


        highest_cancel_rate = (
            cancellation_by_city[
                "Rate"
            ].max()
        )


        # ----------------------------------------------------
        # Highest Profit City
        # ----------------------------------------------------

        profit_by_city = (
            filtered_df
            .groupby("City")[
                "Profit_Margin"
            ]
            .mean()
        )


        highest_profit_city = (
            profit_by_city.idxmax()
        )


        highest_profit_margin = (
            profit_by_city.max() * 100
        )


        insight_col1, insight_col2 = (
            st.columns(2)
        )


        with insight_col1:

            st.markdown(
                f"""
                <div class="insight-box">

                <b>💰 Highest Revenue City</b><br><br>

                <b>{highest_revenue_city}</b>
                generated the highest total order value
                in the selected data:

                <b>{format_currency(highest_revenue_value)}</b>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="insight-box">

                <b>❌ Highest Cancellation Rate</b><br><br>

                <b>{highest_cancel_city}</b>
                currently has the highest cancellation rate:

                <b>{highest_cancel_rate:.2f}%</b>

                This area can be investigated further for
                operational improvement opportunities.

                </div>
                """,
                unsafe_allow_html=True
            )


        with insight_col2:

            st.markdown(
                f"""
                <div class="insight-box">

                <b>📦 Order Performance</b><br><br>

                The selected data contains
                <b>{format_number(total_orders)}</b>
                orders with an average order value of

                <b>{format_currency(avg_order_value)}</b>.

                </div>
                """,
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
                <div class="insight-box">

                <b>📈 Profitability</b><br><br>

                <b>{highest_profit_city}</b>
                currently has the highest average profit
                margin:

                <b>{highest_profit_margin:.2f}%</b>.

                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # DATA QUALITY
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔎 Data Quality Overview"
    )


    missing_dates = (
        df["Order_Date"].isna().sum()
    )


    missing_delivery = (
        df["Delivery_Time_Min"].isna().sum()
    )


    missing_distance = (
        df["Distance_km"].isna().sum()
    )


    missing_final = (
        df["Final_Amount"].isna().sum()
    )


    quality_col1, quality_col2 = (
        st.columns(2)
    )


    with quality_col1:

        st.markdown(
            f"""
            <div class="quality-box">

            <b>Missing Order Dates</b><br>
            {format_number(missing_dates)}

            </div>

            <div class="quality-box">

            <b>Missing Delivery Times</b><br>
            {format_number(missing_delivery)}

            </div>
            """,
            unsafe_allow_html=True
        )


    with quality_col2:

        st.markdown(
            f"""
            <div class="quality-box">

            <b>Missing Distance</b><br>
            {format_number(missing_distance)}

            </div>

            <div class="quality-box">

            <b>Missing Final Amount</b><br>
            {format_number(missing_final)}

            </div>
            """,
            unsafe_allow_html=True
        )


    st.caption(
        "Missing values are retained where the original "
        "data does not provide sufficient information "
        "for reliable imputation."
    )


# ============================================================
# ============================================================
# PAGE 2 — OPERATIONS & DELIVERY
# ============================================================
# ============================================================

elif page == "🚚 Operations & Delivery":

    st.header(
        "🚚 Operations & Delivery"
    )

    st.write(
        "Analyze delivery performance, delays "
        "and customer experience."
    )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    avg_delivery_time = (
        filtered_df[
            "Delivery_Time_Min"
        ].mean()
    )


    avg_delivery_rating = (
        filtered_df[
            "Delivery_Rating"
        ].mean()
    )


    available_delivery = (
        filtered_df[
            "Delivery_Time_Min"
        ].notna()
    )


    delayed_orders = (
        filtered_df[
            "Delivery_Time_Min"
        ] > 120
    ).sum()


    available_count = (
        available_delivery.sum()
    )


    if available_count > 0:

        delay_rate = (
            delayed_orders
            / available_count
            * 100
        )

    else:

        delay_rate = 0


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = (
        st.columns(4)
    )


    col1.metric(
        "Avg Delivery Time",
        (
            f"{avg_delivery_time:.2f} min"
            if not pd.isna(avg_delivery_time)
            else "N/A"
        )
    )


    col2.metric(
        "Avg Delivery Rating",
        (
            f"{avg_delivery_rating:.2f}"
            if not pd.isna(avg_delivery_rating)
            else "N/A"
        )
    )


    col3.metric(
        "Delayed Orders",
        format_number(delayed_orders)
    )


    col4.metric(
        "Delay Rate",
        format_percentage(delay_rate)
    )


    st.markdown("---")


    # ========================================================
    # DISTANCE ANALYSIS
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # DELIVERY TIME BY DISTANCE
    # ========================================================

    with col1:

        st.subheader(
            "📍 Delivery Time by Distance"
        )


        distance_df = (
            filtered_df[
                filtered_df[
                    "Distance_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Distance_Category"
            )
            .agg(
                Avg_Distance=(
                    "Distance_km",
                    "mean"
                ),
                Avg_Delivery_Time=(
                    "Delivery_Time_Min",
                    "mean"
                )
            )
            .reset_index()
        )


        distance_df[
            "Sort_Order"
        ] = distance_df[
            "Distance_Category"
        ].map(
            {
                "Short (0-5 km)": 1,
                "Medium (6-15 km)": 2,
                "Long (16-25 km)": 3,
                "Very Long (26-40 km)": 4
            }
        )


        distance_df = (
            distance_df
            .sort_values("Sort_Order")
        )


        fig = px.bar(
            distance_df,
            x="Distance_Category",
            y="Avg_Delivery_Time",
            title="Average Delivery Time by Distance",
            hover_data={
                "Avg_Distance": ":.2f",
                "Avg_Delivery_Time": ":.2f"
            }
        )


        fig.update_layout(
            xaxis_title="Distance Category",
            yaxis_title="Average Delivery Time (min)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # DELAY RATE BY DISTANCE
    # ========================================================

    with col2:

        st.subheader(
            "⏱️ Delay Rate by Distance"
        )


        delay_distance = (
            filtered_df[
                filtered_df[
                    "Distance_Category"
                ] != "Unknown"
            ]
            .dropna(
                subset=["Delivery_Time_Min"]
            )
            .groupby(
                "Distance_Category"
            )
            .agg(
                Total_Orders=(
                    "Order_ID",
                    "count"
                ),
                Delayed_Orders=(
                    "Delivery_Time_Min",
                    lambda x: (x > 120).sum()
                )
            )
            .reset_index()
        )


        delay_distance[
            "Delay_Rate"
        ] = (
            delay_distance[
                "Delayed_Orders"
            ]
            / delay_distance[
                "Total_Orders"
            ]
            * 100
        )


        fig = px.bar(
            delay_distance,
            x="Distance_Category",
            y="Delay_Rate",
            title="Orders Delayed >120 Minutes",
            hover_data={
                "Total_Orders": ":,.0f",
                "Delayed_Orders": ":,.0f",
                "Delay_Rate": ":.2f"
            }
        )


        fig.update_layout(
            xaxis_title="Distance Category",
            yaxis_title="Delay Rate (%)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # DELIVERY SPEED
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # SPEED DISTRIBUTION
    # ========================================================

    with col1:

        st.subheader(
            "🚀 Delivery Speed Distribution"
        )


        speed_df = (
            filtered_df[
                filtered_df[
                    "Delivery_Speed_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Delivery_Speed_Category"
            )
            .size()
            .reset_index(
                name="Orders"
            )
        )


        speed_df[
            "Sort_Order"
        ] = speed_df[
            "Delivery_Speed_Category"
        ].map(
            {
                "Fast ≤60": 1,
                "Moderate 61-120": 2,
                "Slow 121-180": 3,
                "Very Slow >180": 4
            }
        )


        speed_df = (
            speed_df
            .sort_values("Sort_Order")
        )


        fig = px.bar(
            speed_df,
            x="Delivery_Speed_Category",
            y="Orders",
            title="Delivery Speed Categories",
            hover_data={
                "Orders": ":,.0f"
            }
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # DELIVERY RATING BY SPEED
    # ========================================================

    with col2:

        st.subheader(
            "⭐ Delivery Rating by Speed"
        )


        rating_speed = (
            filtered_df[
                filtered_df[
                    "Delivery_Speed_Category"
                ] != "Unknown"
            ]
            .groupby(
                "Delivery_Speed_Category"
            )
            .agg(
                Avg_Delivery_Rating=(
                    "Delivery_Rating",
                    "mean"
                ),
                Avg_Delivery_Time=(
                    "Delivery_Time_Min",
                    "mean"
                )
            )
            .reset_index()
        )


        fig = px.bar(
            rating_speed,
            x="Delivery_Speed_Category",
            y="Avg_Delivery_Rating",
            title="Average Delivery Rating",
            hover_data={
                "Avg_Delivery_Rating": ":.2f",
                "Avg_Delivery_Time": ":.2f"
            }
        )


        fig.update_layout(
            yaxis_title="Average Rating"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # CANCELLATION REASONS
    # ========================================================

    st.subheader(
        "❌ Cancellation Reasons"
    )


    cancelled_df = filtered_df[
        filtered_df["Order_Status"]
        == "Cancelled"
    ]


    if not cancelled_df.empty:

        reason_df = (
            cancelled_df
            .groupby(
                "Cancellation_Reason"
            )
            .size()
            .reset_index(
                name="Cancelled Orders"
            )
            .sort_values(
                "Cancelled Orders",
                ascending=False
            )
        )


        fig = px.bar(
            reason_df,
            x="Cancellation_Reason",
            y="Cancelled Orders",
            title="Cancelled Orders by Reason",
            hover_data={
                "Cancelled Orders": ":,.0f"
            }
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No cancelled orders are available "
            "for the selected filters."
        )


    # ========================================================
    # WEEKDAY VS WEEKEND
    # ========================================================

    st.subheader(
        "📅 Weekday vs Weekend"
    )


    day_df = (
        filtered_df
        .groupby("Order_Day")
        .agg(
            Orders=(
                "Order_ID",
                "count"
            ),
            Avg_Order_Value=(
                "Order_Value",
                "mean"
            ),
            Avg_Delivery_Time=(
                "Delivery_Time_Min",
                "mean"
            ),
            Avg_Delivery_Rating=(
                "Delivery_Rating",
                "mean"
            )
        )
        .reset_index()
    )


    day_df = day_df.rename(
        columns={
            "Order_Day": "Day Type"
        }
    )


    st.dataframe(
        day_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ============================================================
# PAGE 3 — REVENUE & PROFITABILITY
# ============================================================
# ============================================================

elif page == "💰 Revenue & Profitability":

    st.header(
        "💰 Revenue & Profitability"
    )

    st.write(
        "Analyze revenue, discounts, restaurants "
        "and profit margins."
    )


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

    total_order_value = (
        filtered_df["Order_Value"].sum()
    )


    avg_order_value = (
        filtered_df["Order_Value"].mean()
    )


    avg_final_amount = (
        filtered_df["Final_Amount"].mean()
    )


    avg_profit_margin = (
        filtered_df["Profit_Margin"].mean()
        * 100
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = (
        st.columns(4)
    )


    col1.metric(
        "Total Order Value",
        format_currency(total_order_value)
    )


    col2.metric(
        "Average Order Value",
        format_currency(avg_order_value)
    )


    col3.metric(
        "Average Final Amount",
        format_currency(avg_final_amount)
    )


    col4.metric(
        "Average Profit Margin",
        format_percentage(avg_profit_margin)
    )


    st.markdown("---")


    # ========================================================
    # CUISINE PERFORMANCE
    # ========================================================

    col1, col2 = st.columns(2)


    # ========================================================
    # REVENUE BY CUISINE
    # ========================================================

    with col1:

        st.subheader(
            "🍜 Revenue by Cuisine"
        )


        cuisine_df = (
            filtered_df
            .groupby(
                "Cuisine_Type"
            )
            .agg(
                Total_Order_Value=(
                    "Order_Value",
                    "sum"
                ),
                Orders=(
                    "Order_ID",
                    "count"
                ),
                Avg_Order_Value=(
                    "Order_Value",
                    "mean"
                )
            )
            .reset_index()
            .sort_values(
                "Total_Order_Value",
                ascending=False
            )
        )


        fig = px.bar(
            cuisine_df,
            x="Cuisine_Type",
            y="Total_Order_Value",
            title="Total Order Value by Cuisine",
            hover_data={
                "Total_Order_Value": ":,.0f",
                "Orders": ":,.0f",
                "Avg_Order_Value": ":,.2f"
            }
        )


        fig.update_layout(
            xaxis_title="Cuisine",
            yaxis_title="Order Value (₹)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # ORDERS BY CUISINE
    # ========================================================

    with col2:

        st.subheader(
            "📊 Orders by Cuisine"
        )


        cuisine_volume = (
            cuisine_df
            .sort_values(
                "Orders",
                ascending=False
            )
        )


        fig = px.bar(
            cuisine_volume,
            x="Cuisine_Type",
            y="Orders",
            title="Order Volume by Cuisine",
            hover_data={
                "Orders": ":,.0f"
            }
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # DISCOUNT IMPACT
    # ========================================================

    st.subheader(
        "🏷️ Discount Impact"
    )


    discount_df = (
        filtered_df[
            filtered_df[
                "Discount_Category"
            ] != "Unknown"
        ]
        .groupby(
            "Discount_Category"
        )
        .agg(
            Orders=(
                "Order_ID",
                "count"
            ),
            Avg_Order_Value=(
                "Order_Value",
                "mean"
            ),
            Avg_Discount=(
                "Discount_Applied",
                "mean"
            ),
            Avg_Final_Amount=(
                "Final_Amount",
                "mean"
            ),
            Avg_Discount_Percentage=(
                "Discount_Percentage",
                "mean"
            )
        )
        .reset_index()
    )


    discount_sort = {
        "No Discount": 1,
        "Low": 2,
        "Medium": 3,
        "High": 4
    }


    discount_df[
        "Sort_Order"
    ] = discount_df[
        "Discount_Category"
    ].map(
        discount_sort
    )


    discount_df = (
        discount_df
        .sort_values("Sort_Order")
    )


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            discount_df,
            x="Discount_Category",
            y="Avg_Order_Value",
            title="Average Order Value by Discount",
            hover_data={
                "Orders": ":,.0f",
                "Avg_Order_Value": ":,.2f",
                "Avg_Discount": ":,.2f"
            }
        )


        fig.update_layout(
            xaxis_title="Discount Category",
            yaxis_title="Average Order Value (₹)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = px.bar(
            discount_df,
            x="Discount_Category",
            y="Avg_Final_Amount",
            title="Average Final Amount by Discount",
            hover_data={
                "Orders": ":,.0f",
                "Avg_Final_Amount": ":,.2f",
                "Avg_Discount_Percentage": ":.2f"
            }
        )


        fig.update_layout(
            xaxis_title="Discount Category",
            yaxis_title="Average Final Amount (₹)"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # PROFITABILITY BY CITY
    # ========================================================

    st.subheader(
        "🏙️ Profitability by City"
    )


    city_profit = (
        filtered_df
        .groupby("City")
        .agg(
            Orders=(
                "Order_ID",
                "count"
            ),
            Avg_Profit_Margin=(
                "Profit_Margin",
                "mean"
            ),
            Total_Order_Value=(
                "Order_Value",
                "sum"
            )
        )
        .reset_index()
    )


    city_profit[
        "Avg_Profit_Margin"
    ] = (
        city_profit[
            "Avg_Profit_Margin"
        ] * 100
    )


    fig = px.bar(
        city_profit.sort_values(
            "Avg_Profit_Margin",
            ascending=False
        ),
        x="City",
        y="Avg_Profit_Margin",
        title="Average Profit Margin by City",
        hover_data={
            "Orders": ":,.0f",
            "Avg_Profit_Margin": ":.2f",
            "Total_Order_Value": ":,.0f"
        }
    )


    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Profit Margin (%)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # CITY + CUISINE PROFITABILITY
    # ========================================================

    st.subheader(
        "📈 Profitability by City & Cuisine"
    )


    city_cuisine = (
        filtered_df
        .groupby(
            [
                "City",
                "Cuisine_Type"
            ]
        )
        .agg(
            Orders=(
                "Order_ID",
                "count"
            ),
            Avg_Profit_Margin=(
                "Profit_Margin",
                "mean"
            ),
            Total_Order_Value=(
                "Order_Value",
                "sum"
            )
        )
        .reset_index()
    )


    city_cuisine[
        "Avg_Profit_Margin"
    ] = (
        city_cuisine[
            "Avg_Profit_Margin"
        ] * 100
    )


    fig = px.bar(
        city_cuisine,
        x="City",
        y="Avg_Profit_Margin",
        color="Cuisine_Type",
        barmode="group",
        title="Profit Margin by City and Cuisine",
        hover_data={
            "Orders": ":,.0f",
            "Avg_Profit_Margin": ":.2f",
            "Total_Order_Value": ":,.0f"
        }
    )


    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Average Profit Margin (%)"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # TOP RESTAURANTS
    # ========================================================

    st.subheader(
        "🏆 Top Restaurants by Order Value"
    )


    restaurant_df = (
        filtered_df
        .groupby(
            [
                "Restaurant_ID",
                "Restaurant_Name"
            ]
        )
        .agg(
            Orders=(
                "Order_ID",
                "count"
            ),
            Total_Order_Value=(
                "Order_Value",
                "sum"
            ),
            Avg_Order_Value=(
                "Order_Value",
                "mean"
            ),
            Avg_Restaurant_Rating=(
                "Restaurant_Rating",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "Total_Order_Value",
            ascending=False
        )
        .head(10)
    )


    st.dataframe(
        restaurant_df,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # BUSINESS INSIGHT
    # ========================================================

    st.markdown("---")

    st.subheader(
        "💡 Revenue & Profitability Insight"
    )


    st.markdown(
        """
        <div class="insight-box">

        <b>Discount Strategy:</b><br><br>

        Higher discount categories result in lower average
        final amounts. Discount strategies should therefore
        be evaluated based on their impact on final revenue
        and profitability rather than order value alone.

        <br><br>

        <b>Restaurant Rankings:</b><br><br>

        Restaurant rankings should be interpreted carefully
        when order volumes are low. A minimum order threshold
        can provide a more reliable comparison of restaurant
        performance.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Online Food Delivery Analytics | "
    "Python • Pandas • Streamlit • Plotly • MySQL"
)