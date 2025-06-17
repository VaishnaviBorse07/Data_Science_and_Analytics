import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Title and Layout
st.set_page_config(layout="wide")
st.title("📊 Student Performance Analytics Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("student_marks.csv")  # Ensure this matches your file name
    return df

df = load_data()

# Clean and process columns
df.columns = df.columns.str.strip()  # Remove extra spaces from column names

# Calculate average marks
df['Average_Marks'] = df[['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4']].mean(axis=1)

# Fix invalid attendance (e.g., -94)
df['Attendance'] = df['Attendance'].apply(lambda x: max(x, 0))

# Create At_Risk column
df['At_Risk'] = ((df['Attendance'] < 75) | (df['Average_Marks'] < 40)).astype(int)

# Show raw data
if st.checkbox("Show Raw Data"):
    st.write(df)

# Data Overview
st.subheader("🔍 Data Overview")
st.write(df.describe())

# Attendance vs Marks
st.subheader("📈 Attendance vs Average Marks")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="Attendance", y="Average_Marks", hue="At_Risk", palette="Set1", ax=ax1)
st.pyplot(fig1)

# At-Risk Distribution
st.subheader("⚠️ At-Risk Student Distribution")
fig2, ax2 = plt.subplots()
sns.countplot(data=df, x="At_Risk", palette="Set2", ax=ax2)
st.pyplot(fig2)

# Model Training
st.subheader("🧠 Risk Prediction Model")
features = ['Attendance', 'Average_Marks']
target = 'At_Risk'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluation
acc = accuracy_score(y_test, y_pred)
st.success(f"Model Accuracy: {acc:.2f}")

st.text("Classification Report:")
st.text(classification_report(y_test, y_pred))

# Prediction Interface
st.subheader("🔍 Predict Risk from Inputs")
input_attendance = st.slider("Attendance (%)", 0, 100, 75)
input_marks = st.slider("Average Marks (%)", 0, 100, 50)

input_df = pd.DataFrame({
    'Attendance': [input_attendance],
    'Average_Marks': [input_marks]
})

prediction = model.predict(input_df)[0]
if prediction == 1:
    st.error("This student is at risk.")
else:
    st.success("This student is not at risk.")
