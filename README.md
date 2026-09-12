# Online Food Delivery Data Analytics

## 1. Project Overview

The Online Food Delivery Data Analytics project is an end-to-end data analytics solution developed to analyze food delivery order data and generate meaningful business insights.

The project analyzes customer orders, restaurants, cuisines, delivery performance, cancellations, discounts, revenue, and profitability.

The solution uses Python and Pandas for data processing and analysis, MySQL for database storage and SQL analysis, and Streamlit with Plotly for the interactive dashboard.

---

## 2. Business Objective

The main objective of this project is to transform raw food delivery data into actionable business insights that can support data-driven decision-making.

The project focuses on:

- Monitoring overall order and revenue performance
- Analyzing order cancellations
- Identifying cities with higher cancellation rates
- Understanding delivery performance
- Analyzing the relationship between delivery distance and delays
- Evaluating the impact of discounts
- Comparing restaurant and cuisine performance
- Analyzing profitability across cities and cuisine combinations
- Presenting insights through an interactive dashboard

---

## 3. Project Objectives

- Clean and validate the raw food delivery dataset
- Handle missing and inconsistent data
- Perform feature engineering
- Create an analytical dataset
- Store the analytical dataset in MySQL
- Perform SQL analysis for 15 business questions
- Perform exploratory data analysis using Python
- Develop an interactive Streamlit dashboard
- Generate business insights and recommendations

---

## 4. Dataset

The project uses an Online Food Delivery dataset containing:

- **100,000 records**
- **25 original columns**
- **8,999 unique customers**
- **900 unique restaurants**
- **900 unique delivery partners**
- **100,000 unique orders**

### Original Dataset Columns

1. Order_ID
2. Customer_ID
3. Customer_Age
4. Customer_Gender
5. City
6. Area
7. Restaurant_ID
8. Restaurant_Name
9. Cuisine_Type
10. Order_Date
11. Order_Time
12. Delivery_Time_Min
13. Distance_km
14. Order_Value
15. Discount_Applied
16. Final_Amount
17. Payment_Mode
18. Order_Status
19. Cancellation_Reason
20. Delivery_Partner_ID
21. Delivery_Rating
22. Restaurant_Rating
23. Order_Day
24. Peak_Hour
25. Profit_Margin

---

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning and transformation |
| MySQL | Database storage and SQL analysis |
| MySQL Workbench | SQL development and execution |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| SQLAlchemy | Database connectivity |
| MySQL Connector | MySQL connection |
| VS Code | Development environment |

---

## 6. Project Architecture

```text
Raw CSV
   |
   v
Python / Pandas
   |
   v
Data Understanding
   |
   v
Data Cleaning & Validation
   |
   v
Feature Engineering
   |
   v
Analytical Dataset
   |
   +--------------------+
   |                    |
   v                    v
MySQL Database       Python EDA
   |                    |
   v                    v
SQL Analysis        Business Insights
   |                    |
   +---------+----------+
             |
             v
     Streamlit Dashboard
             |
             v
   Interactive Reporting