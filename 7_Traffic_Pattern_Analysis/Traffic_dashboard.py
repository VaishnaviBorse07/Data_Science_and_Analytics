import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="🚦 Traffic Pattern Dashboard", layout="wide")
st.title("🚦 Traffic Pattern Analysis Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv("Traffic_Congestion_Dataset.csv", parse_dates=["timestamp"])
    df['Hour'] = df['timestamp'].dt.hour
    df['Date'] = df['timestamp'].dt.date
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📍 Filter Options")
min_speed = st.sidebar.slider("Minimum Speed (km/h)", int(df['avg_speed'].min()), int(df['avg_speed'].max()), int(df['avg_speed'].min()))
weather = st.sidebar.multiselect("Weather Conditions", df['weather_condition'].unique(), default=list(df['weather_condition'].unique()))

filtered_df = df[(df['avg_speed'] >= min_speed) & (df['weather_condition'].isin(weather))]

# 1. Line plot: Average Speed by Hour
st.subheader("📊 Average Speed by Hour")
hourly_speed = filtered_df.groupby('Hour')['avg_speed'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=hourly_speed, x='Hour', y='avg_speed', marker='o', ax=ax1)
ax1.set_title("Average Speed by Hour")
ax1.set_ylabel("Speed (km/h)")
st.pyplot(fig1)

# 2. Heatmap: Congestion Level by Hour and Weather
st.subheader("🌦️ Heatmap of Congestion by Hour and Weather")
pivot_table = filtered_df.pivot_table(index='weather_condition', columns='Hour', values='congestion_level', aggfunc='mean')

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot_table, cmap="YlOrRd", linewidths=0.5, annot=True, fmt=".1f", ax=ax2)
ax2.set_title("Average Congestion Level by Hour and Weather")
st.pyplot(fig2)

# 3. Violations per Weather
st.subheader("🚨 Traffic Rule Violations per Weather Condition")
violation_data = filtered_df.groupby('weather_condition')['traffic_rule_violation'].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(x=violation_data.values, y=violation_data.index, ax=ax3, palette="magma")
ax3.set_title("Violations per Weather Condition")
st.pyplot(fig3)

# 4. Fatalities Analysis
st.subheader("☠️ Fatalities per Weather")
fatal_data = filtered_df.groupby('weather_condition')['fatalities'].sum()

fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.barplot(x=fatal_data.values, y=fatal_data.index, palette="Reds", ax=ax4)
ax4.set_title("Fatalities per Weather Condition")
st.pyplot(fig4)

# Data preview
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_df)

# Download
st.subheader("⬇️ Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, file_name="filtered_traffic_data.csv", mime="text/csv")
