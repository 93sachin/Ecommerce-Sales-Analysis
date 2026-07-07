import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib

# ---------------- Page Configuration ---------------- #

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main{
    background-color:#F8F9FA;
}

div[data-testid="metric-container"]{
    background:white;
    padding:18px;
    border-radius:12px;
    border:1px solid #E6E6E6;
    box-shadow:0px 3px 8px rgba(0,0,0,.12);
}

h1{
    color:#1565C0;
}

</style>
""",unsafe_allow_html=True)

# ---------------- Load Data ---------------- #

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/data.csv",
        encoding="ISO-8859-1"
    )

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    return df

df = load_data()

model = joblib.load("models/sales_model.pkl")

# ---------------- Sidebar ---------------- #

st.sidebar.title("🛒 Dashboard Filters")

# Date Filter

start_date = st.sidebar.date_input(
    "Start Date",
    df["InvoiceDate"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["InvoiceDate"].max().date()
)

df = df[
    (df["InvoiceDate"].dt.date >= start_date)
    &
    (df["InvoiceDate"].dt.date <= end_date)
]

# Country Filter

country = st.sidebar.selectbox(

    "Country",

    ["All"] + sorted(df["Country"].dropna().unique())

)

if country != "All":

    df = df[df["Country"] == country]

# Product Search

product = st.sidebar.text_input("Search Product")

if product:

    df = df[
        df["Description"].str.contains(
            product,
            case=False,
            na=False
        )
    ]

# Forecast

st.sidebar.markdown("---")

months = st.sidebar.slider(

    "Forecast Months",

    min_value=1,

    max_value=12,

    value=3

)

# ---------------- Title ---------------- #

st.title("🛒 E-Commerce Sales Dashboard")

st.write(
    "Interactive dashboard built using Python, Streamlit, Plotly, SQL, Power BI and Machine Learning."
)

# ---------------- KPI ---------------- #

total_sales = df["Sales"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

total_products = df["StockCode"].nunique()

avg_order = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

avg_qty = df["Quantity"].mean()

row1 = st.columns(3)

row1[0].metric(
    "💰 Total Sales",
    f"${total_sales/1000000:.2f} M"
)

row1[1].metric(
    "📦 Orders",
    total_orders
)

row1[2].metric(
    "👤 Customers",
    total_customers
)

row2 = st.columns(3)

row2[0].metric(
    "🛍 Products",
    total_products
)

row2[1].metric(
    "💵 Avg Order Value",
    f"${avg_order:.2f}"
)

row2[2].metric(
    "📦 Avg Quantity",
    f"{avg_qty:.2f}"
)

st.divider()

# ---------------- Monthly Sales ---------------- #

monthly_sales = (

    df.groupby(

        df["InvoiceDate"].dt.to_period("M")

    )["Sales"]

    .sum()

    .reset_index()

)

monthly_sales["InvoiceDate"] = monthly_sales["InvoiceDate"].astype(str)

fig1 = px.line(

    monthly_sales,

    x="InvoiceDate",

    y="Sales",

    markers=True,

    title="📈 Monthly Sales Trend"

)

fig1.update_traces(line=dict(width=4))

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ================= COUNTRY SALES ================= #

country_sales = (
    df.groupby("Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    country_sales,
    x="Country",
    y="Sales",
    color="Sales",
    title="🌍 Top 10 Countries by Sales",
    text_auto=".2s"
)

fig2.update_layout(
    xaxis_title="Country",
    yaxis_title="Sales",
    showlegend=False
)

# ================= TOP PRODUCTS ================= #

top_products = (
    df.groupby("Description")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_products,
    x="Sales",
    y="Description",
    orientation="h",
    color="Sales",
    title="🏆 Top 10 Selling Products",
    text_auto=".2s"
)

fig3.update_layout(
    yaxis_title="Product",
    xaxis_title="Sales",
    showlegend=False
)

# ================= SHOW BOTH CHARTS ================= #

left, right = st.columns(2)

with left:
    st.plotly_chart(fig2, use_container_width=True)

with right:
    st.plotly_chart(fig3, use_container_width=True)

# ================= PIE CHART ================= #

pie_data = (
    df.groupby("Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig4 = px.pie(
    pie_data,
    names="Country",
    values="Sales",
    title="🥧 Top 5 Countries Sales Distribution",
    hole=0.45
)

st.plotly_chart(fig4, use_container_width=True)

# ================= TOP CUSTOMERS ================= #

st.subheader("👤 Top 10 Customers")

top_customers = (
    df.groupby("CustomerID")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_customers["Sales"] = top_customers["Sales"].round(2)

st.dataframe(
    top_customers,
    use_container_width=True,
    hide_index=True
)

# ================= DOWNLOAD ================= #

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

st.divider()

# ================= SALES FORECAST ================= #

st.header("📈 Machine Learning Sales Forecast")

# Create monthly data for forecasting
monthly_forecast = (
    df.groupby(pd.Grouper(key="InvoiceDate", freq="ME"))["Sales"]
    .sum()
    .reset_index()
)

last_month = len(monthly_forecast)

future = pd.DataFrame({
    "Month": np.arange(last_month + 1, last_month + months + 1)
})

prediction = model.predict(future)

forecast_df = pd.DataFrame({
    "Future Month": future["Month"],
    "Predicted Sales": prediction.round(2)
})

st.dataframe(
    forecast_df,
    use_container_width=True,
    hide_index=True
)

# ================= FORECAST GRAPH ================= #

fig5 = px.line(
    forecast_df,
    x="Future Month",
    y="Predicted Sales",
    markers=True,
    title="📈 Forecasted Sales",
)

fig5.update_traces(line=dict(width=4))

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ================= DOWNLOAD FORECAST ================= #

forecast_csv = forecast_df.to_csv(index=False)

st.download_button(
    label="📥 Download Forecast",
    data=forecast_csv,
    file_name="sales_forecast.csv",
    mime="text/csv"
)

st.divider()

# ================= PROJECT SUMMARY ================= #

st.subheader("📌 Project Summary")

summary = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Orders",
        "Customers",
        "Products"
    ],
    "Value": [
        f"${total_sales:,.2f}",
        total_orders,
        total_customers,
        total_products
    ]
})

st.dataframe(
    summary,
    hide_index=True,
    use_container_width=True
)

# ================= FOOTER ================= #

st.markdown("---")

st.markdown(
"""
<center>

### 🛒 E-Commerce Sales Analysis Dashboard

Developed by **Sachin Kumar**

**Tech Stack**

Python • Pandas • NumPy • Plotly • Streamlit • SQL • Power BI • Scikit-Learn

</center>
""",
unsafe_allow_html=True
)