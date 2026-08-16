-- ============================================================
-- NOVAMART SALES PERFORMANCE & BUSINESS ANALYTICS
-- ============================================================

USE novamart;


-- ============================================================
-- 1. DATA VALIDATION
-- ============================================================

SELECT COUNT(*) AS total_customers
FROM customers;

SELECT COUNT(*) AS total_products
FROM products;

SELECT COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(*) AS total_order_details
FROM order_details;


-- ============================================================
-- 2. OVERALL BUSINESS KPIs
-- ============================================================

SELECT
    ROUND(
        SUM(p.unit_price * od.quantity * (1 - od.discount)),
        2
    ) AS total_revenue,

    ROUND(
        SUM(p.unit_cost * od.quantity),
        2
    ) AS total_cost,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit,

    ROUND(
        100 *
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        )
        /
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS profit_margin_percentage

FROM products p

JOIN order_details od
    ON p.product_id = od.product_id;


-- Average Order Value

SELECT
    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        )
        / COUNT(DISTINCT od.order_id),
        2
    ) AS average_order_value

FROM products p

JOIN order_details od
    ON p.product_id = od.product_id;


-- ============================================================
-- 3. REVENUE BY CATEGORY
-- ============================================================

SELECT
    p.category,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue

FROM products p

JOIN order_details od
    ON p.product_id = od.product_id

GROUP BY p.category

ORDER BY total_revenue DESC;


-- ============================================================
-- 4. PROFIT BY CATEGORY
-- ============================================================

SELECT
    p.category,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit

FROM products p

JOIN order_details od
    ON p.product_id = od.product_id

GROUP BY p.category

ORDER BY total_profit DESC;


-- ============================================================
-- 5. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue

FROM products p

JOIN order_details od
    ON p.product_id = od.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.category

ORDER BY total_revenue DESC

LIMIT 10;


-- ============================================================
-- 6. MONTHLY REVENUE
-- ============================================================

SELECT
    YEAR(o.order_date) AS year,
    MONTH(o.order_date) AS month,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue

FROM orders o

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY
    YEAR(o.order_date),
    MONTH(o.order_date)

ORDER BY
    year,
    month;


-- ============================================================
-- 7. MONTHLY PROFIT
-- ============================================================

SELECT
    YEAR(o.order_date) AS year,
    MONTH(o.order_date) AS month,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit

FROM orders o

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY
    YEAR(o.order_date),
    MONTH(o.order_date)

ORDER BY
    year,
    month;


-- ============================================================
-- 8. MONTHLY REVENUE + PROFIT + MARGIN
-- ============================================================

SELECT
    YEAR(o.order_date) AS year,
    MONTH(o.order_date) AS month,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit,

    ROUND(
        100 *
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        )
        /
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS profit_margin_percentage

FROM orders o

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY
    YEAR(o.order_date),
    MONTH(o.order_date)

ORDER BY
    year,
    month;


-- ============================================================
-- 9. REGIONAL PERFORMANCE
-- ============================================================

SELECT
    o.region,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit,

    ROUND(
        100 *
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        )
        /
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS profit_margin_percentage

FROM orders o

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY o.region

ORDER BY total_revenue DESC;


-- ============================================================
-- 10. SALES CHANNEL PERFORMANCE
-- ============================================================

SELECT
    o.sales_channel,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit,

    ROUND(
        100 *
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        )
        /
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS profit_margin_percentage,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        )
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value

FROM orders o

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY o.sales_channel

ORDER BY total_revenue DESC;


-- ============================================================
-- 11. CUSTOMER SEGMENT PERFORMANCE
-- ============================================================

SELECT
    c.customer_segment,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY c.customer_segment

ORDER BY total_revenue DESC;


-- ============================================================
-- 12. TOP 10 CUSTOMERS
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.customer_segment,

    COUNT(DISTINCT o.order_id) AS total_orders,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

JOIN order_details od
    ON o.order_id = od.order_id

JOIN products p
    ON od.product_id = p.product_id

GROUP BY
    c.customer_id,
    c.customer_name,
    c.customer_segment

ORDER BY total_revenue DESC

LIMIT 10;


-- ============================================================
-- 13. REPEAT CUSTOMERS
-- ============================================================

SELECT
    COUNT(*) AS repeat_customers

FROM (
    SELECT
        customer_id

    FROM orders

    GROUP BY customer_id

    HAVING COUNT(DISTINCT order_id) > 1
) AS customer_orders;


-- ============================================================
-- 14. DISCOUNT ANALYSIS
-- ============================================================

SELECT
    od.discount,

    COUNT(DISTINCT od.order_id) AS total_orders,

    SUM(od.quantity) AS total_units_sold,

    ROUND(
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ),
        2
    ) AS total_profit,

    ROUND(
        100 *
        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        )
        /
        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ),
        2
    ) AS profit_margin_percentage

FROM order_details od

JOIN products p
    ON od.product_id = p.product_id

GROUP BY od.discount

ORDER BY od.discount;


-- ============================================================
-- 15. TOP 3 PRODUCTS WITHIN EACH CATEGORY
-- ============================================================

WITH product_revenue AS (

    SELECT
        p.product_id,
        p.product_name,
        p.category,

        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ) AS revenue

    FROM products p

    JOIN order_details od
        ON p.product_id = od.product_id

    GROUP BY
        p.product_id,
        p.product_name,
        p.category
),

ranked_products AS (

    SELECT
        product_id,
        product_name,
        category,
        revenue,

        RANK() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS category_rank

    FROM product_revenue
)

SELECT
    product_id,
    product_name,
    category,

    ROUND(revenue, 2) AS revenue,

    category_rank

FROM ranked_products

WHERE category_rank <= 3

ORDER BY
    category,
    category_rank;


-- ============================================================
-- 16. MONTHLY REVENUE GROWTH
-- ============================================================

WITH monthly_sales AS (

    SELECT
        YEAR(o.order_date) AS year,
        MONTH(o.order_date) AS month,

        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ) AS revenue

    FROM orders o

    JOIN order_details od
        ON o.order_id = od.order_id

    JOIN products p
        ON od.product_id = p.product_id

    GROUP BY
        YEAR(o.order_date),
        MONTH(o.order_date)
),

monthly_growth AS (

    SELECT
        year,
        month,
        revenue,

        LAG(revenue) OVER (
            ORDER BY year, month
        ) AS previous_revenue

    FROM monthly_sales
)

SELECT
    year,
    month,

    ROUND(revenue, 2) AS revenue,

    ROUND(previous_revenue, 2) AS previous_revenue,

    ROUND(
        100 * (revenue - previous_revenue)
        / previous_revenue,
        2
    ) AS growth_percentage

FROM monthly_growth

ORDER BY
    year,
    month;


-- ============================================================
-- 17. CUMULATIVE REVENUE
-- ============================================================

WITH monthly_sales AS (

    SELECT
        YEAR(o.order_date) AS year,
        MONTH(o.order_date) AS month,

        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ) AS revenue

    FROM orders o

    JOIN order_details od
        ON o.order_id = od.order_id

    JOIN products p
        ON od.product_id = p.product_id

    GROUP BY
        YEAR(o.order_date),
        MONTH(o.order_date)
)

SELECT
    year,
    month,

    ROUND(revenue, 2) AS monthly_revenue,

    ROUND(
        SUM(revenue) OVER (
            ORDER BY year, month
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS cumulative_revenue

FROM monthly_sales

ORDER BY
    year,
    month;


-- ============================================================
-- 18. HIGH-REVENUE LOW-MARGIN PRODUCTS
-- ============================================================

WITH product_performance AS (

    SELECT
        p.product_id,
        p.product_name,
        p.category,

        SUM(
            p.unit_price * od.quantity * (1 - od.discount)
        ) AS revenue,

        SUM(
            (p.unit_price * od.quantity * (1 - od.discount))
            - (p.unit_cost * od.quantity)
        ) AS profit

    FROM products p

    JOIN order_details od
        ON p.product_id = od.product_id

    GROUP BY
        p.product_id,
        p.product_name,
        p.category
)

SELECT
    product_id,
    product_name,
    category,

    ROUND(revenue, 2) AS revenue,

    ROUND(profit, 2) AS profit,

    ROUND(
        100 * profit / revenue,
        2
    ) AS profit_margin

FROM product_performance

WHERE revenue > 500000

AND (100 * profit / revenue) < 30

ORDER BY revenue DESC;


-- ============================================================
-- END OF SQL ANALYSIS
-- ============================================================