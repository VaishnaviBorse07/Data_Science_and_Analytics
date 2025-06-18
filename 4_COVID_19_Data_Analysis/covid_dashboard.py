import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="COVID-19 Global Dashboard", layout="wide")
st.title("🦠 WHO COVID-19 Global Data Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("WHO-COVID-19-global-data.csv")
    df['Date_reported'] = pd.to_datetime(df['Date_reported'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
countries = st.sidebar.multiselect(
    "Select Country/Countries", 
    options=sorted(df['Country'].unique()), 
    default=["India", "United States of America"]
)
metric = st.sidebar.selectbox(
    "Select Metric", 
    ["New_cases", "Cumulative_cases", "New_deaths", "Cumulative_deaths"]
)
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Date_reported'].min(), df['Date_reported'].max()]
)

# Filter data
mask = (
    (df['Country'].isin(countries)) &
    (df['Date_reported'] >= pd.to_datetime(date_range[0])) &
    (df['Date_reported'] <= pd.to_datetime(date_range[1]))
)
filtered_df = df.loc[mask]

# Line plot
st.subheader(f"📈 Trend of {metric.replace('_', ' ')}")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered_df, x='Date_reported', y=metric, hue='Country', marker='o', ax=ax)
ax.set_xlabel("Date")
ax.set_ylabel(metric.replace('_', ' '))
ax.set_title(f"{metric.replace('_', ' ')} Over Time")
plt.xticks(rotation=45)
st.pyplot(fig)

# Latest data snapshot
st.subheader("📊 Latest Available Data Per Country")
latest_data = (
    filtered_df.sort_values("Date_reported")
    .groupby("Country")
    .tail(1)
    .sort_values(metric, ascending=False)
)[["Country", "Date_reported", metric]]
st.dataframe(latest_data.reset_index(drop=True))

# Bar chart
st.subheader(f"📉 {metric.replace('_', ' ')} on Latest Reported Date")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=latest_data, x=metric, y="Country", ax=ax2)
ax2.set_title(f"{metric.replace('_', ' ')} by Country")
st.pyplot(fig2)

# Download filtered data
st.subheader("⬇️ Export Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_covid_data.csv", "text/csv")
