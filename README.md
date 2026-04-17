# 📊 E-commerce Sales Analytics Project

## 🔹 Project Overview
This project focuses on analyzing e-commerce sales data to extract meaningful business insights. It involves data preprocessing, exploratory data analysis (EDA), SQL-based querying, and building an interactive Power BI dashboard.

The goal of this project is to understand customer behavior, product performance, and revenue trends to support data-driven business decisions.

---
Due to Large mb of data dataset is not uploaded but there is link where u seen - https://www.kaggle.com/datasets/carrie1/ecommerce-data

## 🔹 Tools & Technologies Used
- Python (Pandas, NumPy)
- SQL (MySQL Workbench)
- Power BI
- Jupyter Notebook

---

## 🔹 Project Workflow

1. **Data Collection**
   - Imported raw dataset in CSV format

2. **Data Cleaning (Python)**
   - Handled missing values
   - Removed duplicate records
   - Converted date columns into proper format
   - Removed invalid/negative transactions
   - Created new feature: `TotalPrice`

3. **Exploratory Data Analysis (EDA)**
   - Identified top-performing products
   - Analyzed country-wise sales
   - Examined monthly sales trends

4. **SQL Analysis**
   - Performed queries to extract:
     - Total revenue
     - Top customers
     - Product performance
     - Country-wise sales
     - Monthly trends

5. **Dashboard Development (Power BI)**
   - Built an interactive dashboard including:
     - Total Revenue KPI
     - Total Orders KPI
     - Sales by Country
     - Monthly Sales Trend
     - Top Products
     - Customer Insights

---

## 🔹 Key Insights

- A small group of products contributes to a large portion of total revenue
- Certain countries generate the majority of sales
- Sales show clear monthly trends indicating seasonal demand
- Top customers significantly impact overall revenue

---

## 🔹 Dashboard Preview

![Dashboard Screenshot](screenshots/dashboard.png)

---

## 🔹 Project Structure
Ecommerce-Churn-Analysis/
│
├── data/
│ ├── raw_data.csv
│ └── cleaned_data.csv
│
├── notebooks/
│ └── data_analysis.ipynb
│
├── sql/
│ └── analysis_queries.sql
│
├── dashboard/
│ └── ecommerce_dashboard.pbix
│
├── screenshots/
│ └── dashboard.png
│
└── README.md


---

## 🔹 Conclusion

This project demonstrates an end-to-end data analytics workflow, from raw data processing to business insights and visualization. It highlights the importance of data-driven decision-making in improving business performance.

---

## 🔹 Author
Sachin Kumar
