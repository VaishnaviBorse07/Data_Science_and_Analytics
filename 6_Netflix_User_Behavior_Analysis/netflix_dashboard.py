import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="🎬 Netflix Behavior Dashboard", layout="wide")
st.title("📺 Netflix User Behavior Analysis")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_data.csv", parse_dates=["WatchDate"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
genre_filter = st.sidebar.multiselect("Select Genres", df["Genre"].unique(), default=list(df["Genre"].unique()))
gender_filter = st.sidebar.multiselect("Select Genders", df["Gender"].unique(), default=list(df["Gender"].unique()))
min_duration = st.sidebar.slider("Minimum Watch Duration (min)", 30, 180, 30)

# Filtered Data
filtered_df = df[
    (df["Genre"].isin(genre_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["WatchDuration"] >= min_duration)
]

# Genre Popularity
st.subheader("🎞️ Genre Popularity")
genre_count = filtered_df["Genre"].value_counts().reset_index()
genre_count.columns = ["Genre", "Views"]
fig1 = px.bar(genre_count, x="Genre", y="Views", color="Genre", labels={"Genre": "Genre", "Views": "Views"})
st.plotly_chart(fig1, use_container_width=True)

# Age Distribution
st.subheader("👥 Age Distribution")
fig2 = px.histogram(filtered_df, x="Age", nbins=20, color="Gender", barmode="overlay", labels={"Age": "User Age"})
st.plotly_chart(fig2, use_container_width=True)

# Average Watch Duration by Genre
st.subheader("⏱️ Average Watch Duration by Genre")
duration_df = filtered_df.groupby("Genre")["WatchDuration"].mean().reset_index()
fig3 = px.bar(duration_df, x="Genre", y="WatchDuration", color="Genre", labels={"WatchDuration": "Avg Duration (min)"})
st.plotly_chart(fig3, use_container_width=True)

# Ratings Overview
st.subheader("⭐ Average Rating by Genre")
rating_df = filtered_df.groupby("Genre")["Rating"].mean().reset_index()
fig4 = px.bar(rating_df, x="Genre", y="Rating", color="Genre", labels={"Rating": "Avg Rating"})
st.plotly_chart(fig4, use_container_width=True)

# Watch Trend Over Time
st.subheader("📅 Viewing Trends Over Time")
trend_df = filtered_df.groupby(filtered_df["WatchDate"].dt.to_period("M"))["WatchDuration"].sum().reset_index()
trend_df["WatchDate"] = trend_df["WatchDate"].dt.to_timestamp()
fig5 = px.line(trend_df, x="WatchDate", y="WatchDuration", markers=True, labels={"WatchDate": "Month", "WatchDuration": "Total Watch Time (min)"})
st.plotly_chart(fig5, use_container_width=True)

# Data Export
st.subheader("⬇️ Download Filtered Dataset")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "filtered_netflix_data.csv", "text/csv")
