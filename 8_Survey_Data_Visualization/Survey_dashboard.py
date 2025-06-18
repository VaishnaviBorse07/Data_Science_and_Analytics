import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="📝 Survey Feedback Dashboard", layout="wide")
st.title("📋 Student Feedback Survey Visualization")

@st.cache_data
def load_data():
    df = pd.read_csv("student_feedback.csv")
    df.drop(columns=['Unnamed: 0', 'Student ID'], inplace=True)
    return df

df = load_data()

st.sidebar.header("🔍 Choose Question")
selected_question = st.sidebar.selectbox("Select a survey question to analyze", df.columns)

# Plot distribution of selected question
st.subheader(f"📊 Distribution: {selected_question}")
fig, ax = plt.subplots()
sns.histplot(df[selected_question], bins=10, kde=True, ax=ax)
ax.set_xlabel("Rating")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

# Overall average ratings
st.subheader("⭐ Average Rating per Question")
avg_ratings = df.mean().sort_values(ascending=False)
st.bar_chart(avg_ratings)

# Export option
st.subheader("⬇️ Download Filtered Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", csv, "student_feedback_cleaned.csv", "text/csv")
