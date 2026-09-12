USE online_food_delivery;

-- =========================================================
-- Q1. Overall Business Performance
-- =========================================================

SELECT
    COUNT(*) AS total_orders,

    SUM(CASE
        WHEN Order_Status = 'Delivered' THEN 1
        ELSE 0
    END) AS delivered_orders,

    SUM(CASE
        WHEN Order_Status = 'Cancelled' THEN 1
        ELSE 0
    END) AS cancelled_orders,

    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct,

    ROUND(SUM(Order_Value), 2) AS total_order_value,

    ROUND(SUM(Final_Amount), 2) AS total_final_amount,

    ROUND(AVG(Order_Value), 2) AS avg_order_value,

    ROUND(AVG(Final_Amount), 2) AS avg_final_amount,

    ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time_min,

    ROUND(AVG(Delivery_Rating), 2) AS avg_delivery_rating,

    ROUND(AVG(Restaurant_Rating), 2) AS avg_restaurant_rating,

    ROUND(AVG(Profit_Margin) * 100, 2) AS avg_profit_margin_pct

FROM food_delivery_orders;

-- =========================================================
-- Q2. City Performance
-- =========================================================

SELECT
    City,
    COUNT(*) AS total_orders,
    ROUND(SUM(Order_Value), 2) AS total_order_value,
    ROUND(AVG(Order_Value), 2) AS avg_order_value,
    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct

FROM food_delivery_orders

GROUP BY City

ORDER BY total_order_value DESC;

-- =========================================================
-- Q3. Cuisine Performance
-- =========================================================

SELECT
    Cuisine_Type,
    COUNT(*) AS total_orders,
    ROUND(SUM(Order_Value), 2) AS total_order_value,
    ROUND(AVG(Order_Value), 2) AS avg_order_value,
    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct

FROM food_delivery_orders

GROUP BY Cuisine_Type

ORDER BY total_order_value DESC;

-- =========================================================
-- Q4. Monthly Order Trend
-- =========================================================

SELECT
    Order_Year,
    Order_Month_Num,
    Order_Month,
    COUNT(*) AS total_orders,
    ROUND(SUM(Order_Value), 2) AS total_order_value,
    ROUND(AVG(Order_Value), 2) AS avg_order_value,
    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct

FROM food_delivery_orders

GROUP BY
    Order_Year,
    Order_Month_Num,
    Order_Month

ORDER BY
    Order_Year,
    Order_Month_Num;

    -- =========================================================
-- Q5. Weekday vs Weekend Performance
-- =========================================================

SELECT
    Order_Day,
    COUNT(*) AS total_orders,
    ROUND(SUM(Order_Value), 2) AS total_order_value,
    ROUND(AVG(Order_Value), 2) AS avg_order_value,
    ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time_min,
    ROUND(AVG(Delivery_Rating), 2) AS avg_delivery_rating,
    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct

FROM food_delivery_orders

GROUP BY Order_Day

ORDER BY total_orders DESC;

-- =========================================================
-- Q6. Cancellation Rate by City
-- =========================================================

SELECT
    City,
    COUNT(*) AS total_orders,

    SUM(CASE
        WHEN Order_Status = 'Cancelled' THEN 1
        ELSE 0
    END) AS cancelled_orders,

    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct,

    ROUND(SUM(Order_Value), 2) AS total_order_value

FROM food_delivery_orders

GROUP BY City

ORDER BY cancellation_rate_pct DESC;

-- =========================================================
-- Q7. Cancellation Reasons
-- =========================================================

SELECT
    Cancellation_Reason,
    COUNT(*) AS cancelled_orders,
    ROUND(
        COUNT(*) * 100.0 /
        SUM(COUNT(*)) OVER (),
        2
    ) AS cancellation_share_pct

FROM food_delivery_orders

WHERE Order_Status = 'Cancelled'

GROUP BY Cancellation_Reason

ORDER BY cancelled_orders DESC;

-- =========================================================
-- Q8. Delivery Time vs Distance
-- =========================================================

SELECT
    Distance_Category,
    COUNT(*) AS total_orders,
    ROUND(AVG(Distance_km), 2) AS avg_distance_km,
    ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time_min,
    ROUND(AVG(Delivery_Rating), 2) AS avg_delivery_rating

FROM food_delivery_orders

WHERE Distance_Category <> 'Unknown'

GROUP BY Distance_Category

ORDER BY
    CASE Distance_Category
        WHEN 'Short (0-5 km)' THEN 1
        WHEN 'Medium (6-15 km)' THEN 2
        WHEN 'Long (16-25 km)' THEN 3
        WHEN 'Very Long (26-40 km)' THEN 4
    END;

-- =========================================================
-- Q9. Delivery Delays by Distance Category
-- =========================================================

SELECT
    Distance_Category,
    COUNT(*) AS total_orders,

    SUM(CASE
        WHEN Delivery_Time_Min > 120 THEN 1
        ELSE 0
    END) AS delayed_orders,

    ROUND(
        SUM(CASE
            WHEN Delivery_Time_Min > 120 THEN 1
            ELSE 0
        END) * 100.0 /
        COUNT(Delivery_Time_Min),
        2
    ) AS delay_rate_pct,

    ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time_min

FROM food_delivery_orders

WHERE Distance_Category <> 'Unknown'
  AND Delivery_Time_Min IS NOT NULL

GROUP BY Distance_Category

ORDER BY delay_rate_pct DESC;

-- =========================================================
-- Q10. Delivery Performance vs Delivery Rating
-- =========================================================

SELECT
    Delivery_Speed_Category,
    COUNT(*) AS total_orders,
    ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time_min,
    ROUND(AVG(Delivery_Rating), 2) AS avg_delivery_rating,
    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct

FROM food_delivery_orders

WHERE Delivery_Speed_Category <> 'Unknown'

GROUP BY Delivery_Speed_Category

ORDER BY
    CASE Delivery_Speed_Category
        WHEN 'Fast ≤60' THEN 1
        WHEN 'Moderate 61-120' THEN 2
        WHEN 'Slow 121-180' THEN 3
        WHEN 'Very Slow >180' THEN 4
    END;

-- =========================================================
-- Q11. Discount Impact
-- =========================================================

SELECT
    Discount_Category,
    COUNT(*) AS total_orders,
    ROUND(AVG(Order_Value), 2) AS avg_order_value,
    ROUND(AVG(Discount_Applied), 2) AS avg_discount,
    ROUND(AVG(Final_Amount), 2) AS avg_final_amount,
    ROUND(
        AVG(Discount_Percentage),
        2
    ) AS avg_discount_percentage

FROM food_delivery_orders

WHERE Discount_Category <> 'Unknown'

GROUP BY Discount_Category

ORDER BY
    CASE Discount_Category
        WHEN 'No Discount' THEN 1
        WHEN 'Low' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'High' THEN 4
    END;

-- =========================================================
-- Q12. Restaurant Performance
-- =========================================================

SELECT
    Restaurant_ID,
    Restaurant_Name,
    COUNT(*) AS total_orders,
    ROUND(SUM(Order_Value), 2) AS total_order_value,
    ROUND(AVG(Order_Value), 2) AS avg_order_value,
    ROUND(AVG(Restaurant_Rating), 2) AS avg_restaurant_rating

FROM food_delivery_orders

GROUP BY
    Restaurant_ID,
    Restaurant_Name

ORDER BY total_order_value DESC
LIMIT 10;

-- =========================================================
-- Q13. Best-Rated Restaurants
-- =========================================================

SELECT
    Restaurant_ID,
    Restaurant_Name,
    COUNT(*) AS total_orders,
    ROUND(AVG(Restaurant_Rating), 2) AS avg_restaurant_rating,
    ROUND(SUM(Order_Value), 2) AS total_order_value

FROM food_delivery_orders

WHERE Restaurant_Rating IS NOT NULL

GROUP BY
    Restaurant_ID,
    Restaurant_Name

ORDER BY
    avg_restaurant_rating DESC,
    total_orders DESC

LIMIT 10;

-- =========================================================
-- Q14. Profitability by City and Cuisine
-- =========================================================

SELECT
    City,
    Cuisine_Type,
    COUNT(*) AS total_orders,
    ROUND(AVG(Profit_Margin) * 100, 2) AS avg_profit_margin_pct,
    ROUND(SUM(Order_Value), 2) AS total_order_value,
    ROUND(AVG(Order_Value), 2) AS avg_order_value

FROM food_delivery_orders

GROUP BY
    City,
    Cuisine_Type

ORDER BY
    avg_profit_margin_pct DESC;

-- =========================================================
-- Q15. Management Priorities by City
-- =========================================================

SELECT
    City,
    COUNT(*) AS total_orders,

    SUM(CASE
        WHEN Order_Status = 'Cancelled' THEN 1
        ELSE 0
    END) AS cancelled_orders,

    ROUND(
        SUM(CASE
            WHEN Order_Status = 'Cancelled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct,

    ROUND(AVG(Delivery_Time_Min), 2) AS avg_delivery_time_min,

    ROUND(AVG(Delivery_Rating), 2) AS avg_delivery_rating,

    ROUND(AVG(Profit_Margin) * 100, 2) AS avg_profit_margin_pct,

    ROUND(SUM(Order_Value), 2) AS total_order_value

FROM food_delivery_orders

GROUP BY City

ORDER BY
    cancellation_rate_pct DESC,
    avg_delivery_time_min DESC;