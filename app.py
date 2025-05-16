import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv", parse_dates=["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

st.title("📊 Retail Sales Data Analytics Dashboard")

# KPIs
total_sales = df["Total"].sum()
total_orders = df.shape[0]
avg_order_value = df["Total"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("🛒 Total Orders", f"{total_orders}")
col3.metric("📦 Average Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# Monthly Revenue Line Chart
monthly_sales = df.groupby("Month")[["Total"]].sum().reset_index()
fig1 = px.line(monthly_sales, x="Month", y="Total", title="📈 Monthly Revenue")
st.plotly_chart(fig1, use_container_width=True)

# Region-wise Sales
region_sales = df.groupby("Region")[["Total"]].sum().reset_index()
fig2 = px.bar(region_sales, x="Region", y="Total", color="Region", title="🌍 Sales by Region")
st.plotly_chart(fig2, use_container_width=True)

# Product-wise Sales
product_sales = df.groupby("Product")[["Total"]].sum().reset_index().sort_values(by="Total", ascending=False)
fig3 = px.bar(product_sales, x="Product", y="Total", color="Product", title="📦 Sales by Product")
st.plotly_chart(fig3, use_container_width=True)

# Category Pie Chart
category_sales = df.groupby("Category")[["Total"]].sum().reset_index()
fig4 = px.pie(category_sales, values="Total", names="Category", title="📊 Sales by Category")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("Made with ❤️ using Streamlit")
