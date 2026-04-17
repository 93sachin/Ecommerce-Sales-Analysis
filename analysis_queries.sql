use ecommerce;
-- 1. Check data
SELECT * FROM orders LIMIT 10;

-- 2. Total Revenue
SELECT SUM(TotalPrice) AS Total_Revenue
FROM orders;

-- 3. Total Orders
SELECT COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM orders;

-- 4. Top 5 Products by Revenue
SELECT Description, SUM(TotalPrice) AS Revenue
FROM orders
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 5;

-- 5. Top 10 Products by Quantity Sold
SELECT Description, SUM(Quantity) AS Total_Quantity
FROM orders
GROUP BY Description
ORDER BY Total_Quantity DESC
LIMIT 10;

-- 6. Sales by Country
SELECT Country, SUM(TotalPrice) AS Revenue
FROM orders
GROUP BY Country
ORDER BY Revenue DESC;

-- 7. Monthly Sales Trend
SELECT MONTH(InvoiceDate) AS Month, SUM(TotalPrice) AS Revenue
FROM orders
GROUP BY Month
ORDER BY Month;

-- 8. Top 5 Customers by Spending
SELECT CustomerID, SUM(TotalPrice) AS Total_Spending
FROM orders
GROUP BY CustomerID
ORDER BY Total_Spending DESC
LIMIT 5;

-- 9. Average Order Value
SELECT 
    SUM(TotalPrice) / COUNT(DISTINCT InvoiceNo) AS Avg_Order_Value
FROM orders;

-- 10. Number of Unique Customers
SELECT COUNT(DISTINCT CustomerID) AS Total_Customers
FROM orders;

-- 11. Orders per Country
SELECT Country, COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM orders
GROUP BY Country
ORDER BY Total_Orders DESC;

-- 12. Revenue per Customer
SELECT CustomerID, SUM(TotalPrice) AS Revenue
FROM orders
GROUP BY CustomerID
ORDER BY Revenue DESC;