import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Page setup
st.set_page_config(page_title="🛒 E-Commerce Insights Dashboard", layout="wide")
st.title("📊 E-Commerce Data Insights Dashboard")

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("E-Commerce.csv", parse_dates=["InvoiceDate"])
    df['Month'] = df['InvoiceDate'].dt.to_period("M").dt.to_timestamp()
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
categories = st.sidebar.multiselect(
    "Select Device Category",
    options=df['DeviceCategory'].dropna().unique(),
    default=list(df['DeviceCategory'].dropna().unique())
)
min_sales = st.sidebar.slider("Minimum Sales", 0, int(df['Sales'].max()), 1000)

# Filtered DataFrame
filtered_df = df[(df['DeviceCategory'].isin(categories)) & (df['Sales'] >= min_sales)]

# Monthly Sales Trends
st.subheader("📈 Monthly Sales Trends")
monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_sales, x="Month", y="Sales", marker="o", ax=ax1)
ax1.set_title("Monthly Sales")
st.pyplot(fig1)

# Top Performing Products
st.subheader("🏆 Top Performing Products")
top_products = (
    filtered_df.groupby('ProductID')
    .agg(Total_Sales=('Sales', 'sum'), Orders=('InvoiceNumber', 'nunique'))
    .sort_values(by='Total_Sales', ascending=False)
    .head(10)
    .reset_index()
)
st.dataframe(top_products)

# Product Ratings
if 'ProductRating' in df.columns:
    st.subheader("⭐ Top Rated Products")
    top_rated = (
        filtered_df.groupby('ProductID')['ProductRating']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_rated)

# Country-wise Sales (Choropleth map)
st.subheader("🌍 Country-wise Sales Heatmap")
country_sales = filtered_df.groupby('Country')['Sales'].sum().reset_index()
fig2 = px.choropleth(
    country_sales,
    locations='Country',
    locationmode='country names',
    color='Sales',
    color_continuous_scale='Viridis',
    title='Country-wise Sales'
)
st.plotly_chart(fig2)

# Device Usage (Pie Chart)
st.subheader("📱 Device Usage Breakdown")
device_usage = filtered_df['Device'].value_counts()
fig3 = px.pie(names=device_usage.index, values=device_usage.values, title="Device Usage")
st.plotly_chart(fig3)

# Order Status Breakdown
st.subheader("📦 Order Status Breakdown")
order_status = filtered_df['OrderStatus'].value_counts()
fig4, ax4 = plt.subplots()
sns.barplot(x=order_status.index, y=order_status.values, ax=ax4)
ax4.set_title("Order Status Distribution")
ax4.set_ylabel("Number of Orders")
ax4.set_xlabel("Order Status")
st.pyplot(fig4)

# Export Button
st.subheader("⬇️ Export Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_ecommerce_data.csv", "text/csv")
