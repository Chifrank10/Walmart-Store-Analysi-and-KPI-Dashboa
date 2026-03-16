SELECT 
    *
FROM
    walmart.walmart;
SELECT 
    *
FROM
    walmart;

-- Check the structure of the table

Describe walmart;

-- Remove dollar signs if present
UPDATE walmart 
SET 
    `unit_price` = REPLACE(`unit_price`, '$', '');

-- Then convert to DOUBLE
ALTER TABLE walmart
MODIFY COLUMN `unit_price` DOUBLE;

-- Then change the column dtype
ALTER TABLE walmart
MODIFY COLUMN `date` DATE;

-- change the column dtype
ALTER TABLE walmart
MODIFY COLUMN `time` TIME;
-- View your data 
SELECT 
    *
FROM
    walmart;
-- Check to see change in data type.
Describe walmart;

--  check for duplicate record
SELECT 
    invoice_id, COUNT(*) AS duplicate_count
FROM
    walmart
GROUP BY invoice_id
HAVING COUNT(*) > 1;
-- check using invoice_id if the data actually has a duplicate record
SELECT 
    *
FROM
    walmart
WHERE
    invoice_id = 9988;
-- delete duplicate records but first temporarily disable safe mode
-- create a row number windows column.
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER(PARTITION BY invoice_id ORDER BY invoice_id) AS row_num
    FROM walmart
) t
WHERE row_num > 1;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM walmart
WHERE invoice_id IN (
    SELECT invoice_id
    FROM (
        SELECT invoice_id,
               ROW_NUMBER() OVER(PARTITION BY invoice_id ORDER BY invoice_id) AS row_num
        FROM walmart
    ) t
    WHERE row_num > 1
);
-- confirm if duplicate record has been removed
SELECT 
    invoice_id, COUNT(*) AS duplicate_count
FROM
    walmart
GROUP BY invoice_id
HAVING COUNT(*) > 1;
-- check for null values
SELECT 
    SUM(CASE
        WHEN Invoice_id IS NULL THEN 1
        ELSE 0
    END) AS Invoice_NULLs,
    SUM(CASE
        WHEN Branch IS NULL THEN 1
        ELSE 0
    END) AS Branch_NULLs,
    SUM(CASE
        WHEN City IS NULL THEN 1
        ELSE 0
    END) AS City_NULLs,
    SUM(CASE
        WHEN Category IS NULL THEN 1
        ELSE 0
    END) AS Category_NULLs,
    SUM(CASE
        WHEN `unit_price` IS NULL THEN 1
        ELSE 0
    END) AS UnitPrice_NULLs,
    SUM(CASE
        WHEN Quantity IS NULL THEN 1
        ELSE 0
    END) AS Quantity_NULLs,
    SUM(CASE
        WHEN `date` IS NULL THEN 1
        ELSE 0
    END) AS Date_NULLs,
    SUM(CASE
        WHEN `time` IS NULL THEN 1
        ELSE 0
    END) AS Time_NULLs,
    SUM(CASE
        WHEN `payment_method` IS NULL THEN 1
        ELSE 0
    END) AS PaymentMethod_NULLs,
    SUM(CASE
        WHEN Rating IS NULL THEN 1
        ELSE 0
    END) AS Rating_NULLs,
    SUM(CASE
        WHEN `profit_margin` IS NULL THEN 1
        ELSE 0
    END) AS ProfitMargin_NULLs
FROM
    walmart;
-- so there is no miss values so no need to remove missing values
-- we do some feature engineering that would help in time analysis
ALTER TABLE walmart
ADD year INT,
ADD month INT,
ADD day INT;
-- populate the columns
UPDATE walmart 
SET 
    year = YEAR(date),
    month = MONTH(date),
    day = DAY(date);
SELECT 
    *
FROM
    walmart
LIMIT 20;
-- Quality check for data
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT invoice_id) AS unique_transactions
FROM
    walmart;
SET SQL_SAFE_UPDATES = 1;
