create database retail_analytics;
Use retail_analytics;

SELECT COUNT(*) FROM cleaned_dataset;

SELECT * FROM cleaned_dataset;

SELECT COUNT(*) FROM cleaned_dataset WHERE CustomerID IS NULL;

SELECT COUNT(*) FROM cleaned_dataset WHERE UnitPrice <= 0;

CREATE TABLE fact_sales AS
SELECT
    InvoiceNo,
    CustomerID,
    StockCode,
    InvoiceDate,
    Quantity,
    UnitPrice,
    Quantity * UnitPrice AS total_price,
    Country
FROM cleaned_dataset;

CREATE TABLE dim_customer AS
SELECT DISTINCT
    CustomerID,
    Country
FROM fact_sales;

CREATE TABLE dim_product AS
SELECT DISTINCT
    StockCode,
    Description,
    UnitPrice
FROM cleaned_dataset;

SELECT * FROM fact_sales LIMIT 10;

SELECT COUNT(*) AS customer_count FROM dim_customer;


CREATE VIEW single_customer_view AS
SELECT
    CustomerID,
    MAX(InvoiceDate) AS last_purchase_date,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    SUM(Quantity) AS total_items,
    SUM(total_price) AS total_revenue
FROM fact_sales
GROUP BY CustomerID;

SELECT * FROM single_customer_view LIMIT 50;

CREATE OR REPLACE VIEW single_customer_view AS
SELECT
    CustomerID,

    MIN(InvoiceDate) AS first_purchase_date,

    COUNT(DISTINCT InvoiceNo) AS total_orders,
    SUM(Quantity) AS total_items,
    ROUND(SUM(total_price), 2) AS total_revenue

FROM fact_sales
GROUP BY CustomerID;



