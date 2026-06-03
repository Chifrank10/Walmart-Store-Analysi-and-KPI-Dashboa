-- Walmart Project Queries - MySQL

SELECT * FROM walmart;

SELECT COUNT(*) FROM walmart;

-- Count payment methods and number of transactions by payment method
SELECT 
    payment_method,
    COUNT(*) AS no_payments
FROM walmart
GROUP BY payment_method;

-- Count distinct branches
SELECT COUNT(DISTINCT branch) FROM walmart;

-- Find the minimum quantity sold
SELECT MIN(quantity) FROM walmart;

-- Business Problem Q1: Find different payment methods, number of transactions, and quantity sold by payment method
SELECT 
    payment_method,
    COUNT(*) AS no_payments,
    SUM(quantity) AS no_qty_sold
FROM walmart
GROUP BY payment_method;

-- Project Question #2: Identify the highest-rated category in each branch
-- Display the branch, category, and avg rating
SELECT branch, category, avg_rating
FROM (
    SELECT 
        branch,
        category,
        AVG(rating) AS avg_rating,
        RANK() OVER (PARTITION BY branch ORDER BY AVG(rating) DESC) AS rnk
    FROM walmart
    GROUP BY branch, category
) AS ranked
WHERE rnk = 1;
-- Q3: Identify the busiest day for each branch based on the number of transactions
WITH daily_transactions AS (
    SELECT 
        branch,
        DAYNAME(STR_TO_DATE(date, '%d/%m/%Y')) AS day_name,
        COUNT(*) AS no_transactions
    FROM walmart
    GROUP BY branch, DAYNAME(STR_TO_DATE(date, '%d/%m/%Y'))
),
ranked AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY branch 
               ORDER BY no_transactions DESC
           ) AS rnk
    FROM daily_transactions
)
SELECT branch, day_name, no_transactions
FROM ranked
WHERE rnk = 1;
-- Q4: Calculate the total quantity of items sold per payment method
SELECT 
    payment_method,
    SUM(quantity) AS no_qty_sold
FROM walmart
GROUP BY payment_method;

-- Q5: Determine the average, minimum, and maximum rating of categories for each city
SELECT 
    city,
    category,
    MIN(rating) AS min_rating,
    MAX(rating) AS max_rating,
    AVG(rating) AS avg_rating
FROM walmart
GROUP BY city, category;

-- Q6: Calculate the total profit for each category
SELECT 
    category,
    round(SUM(unit_price * quantity * profit_margin),1) AS total_profit
FROM walmart
GROUP BY category
ORDER BY total_profit DESC;

-- Q7: Determine the most common payment method for each branch
WITH cte AS (
    SELECT 
        branch,
        payment_method,
        COUNT(*) AS total_trans
    FROM walmart
    GROUP BY branch, payment_method
),
ranked AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY branch 
               ORDER BY total_trans DESC
           ) AS rnk
    FROM cte
)
SELECT branch, payment_method AS preferred_payment_method
FROM ranked
WHERE rnk = 1;
-- Q8: Categorize sales into Morning, Afternoon, and Evening shifts
SELECT
    branch,
    CASE 
        WHEN HOUR(TIME(time)) < 12 THEN 'Morning'
        WHEN HOUR(TIME(time)) BETWEEN 12 AND 17 THEN 'Afternoon'
        ELSE 'Evening'
    END AS shift,
    COUNT(*) AS num_invoices
FROM walmart
GROUP BY branch, shift
ORDER BY branch, num_invoices DESC;

-- Q9: Identify the 5 branches with the highest revenue decrease ratio from last year to current year (e.g., 2022 to 2023)
WITH revenue_2022 AS (
    SELECT 
        branch,
        SUM(Sales) AS revenue
    FROM walmart
    WHERE YEAR(STR_TO_DATE(date, '%d/%m/%Y')) = 2022
    GROUP BY branch
),
revenue_2023 AS (
    SELECT 
        branch,
        SUM(Sales) AS revenue
    FROM walmart
    WHERE YEAR(STR_TO_DATE(date, '%d/%m/%Y')) = 2023
    GROUP BY branch
)
SELECT 
    r2022.branch,
    r2022.revenue AS last_year_revenue,
    COALESCE(r2023.revenue, 0) AS current_year_revenue,
    ROUND(
        ((r2022.revenue - COALESCE(r2023.revenue, 0)) / NULLIF(r2022.revenue, 0)) * 100,
        2
    ) AS revenue_decrease_ratio
FROM revenue_2022 r2022
LEFT JOIN revenue_2023 r2023 
    ON r2022.branch = r2023.branch
ORDER BY revenue_decrease_ratio DESC
LIMIT 5;