import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime
import numpy as np

# UI Title
st.title("📈 Sales Forecasting with Linear Regression")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your sales data CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show preview and number of rows
    st.write("### Preview of Uploaded Data")
    st.write(f"📄 Total rows in dataset: {len(df)}")
    st.dataframe(df.head(100))

    # Convert date to datetime and then to ordinal
    df['Date'] = pd.to_datetime(df['Date'])
    df['DayNumber'] = df['Date'].map(datetime.toordinal)

    # Feature and Target
    X = df[['DayNumber']]
    y = df['Revenue']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Predict for full dataset
    df['Predicted Revenue'] = model.predict(X)

    # Plotting
    st.write("### 📊 Actual vs Predicted Revenue")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Date'], df['Revenue'], label='Actual Revenue', marker='o')
    ax.plot(df['Date'], df['Predicted Revenue'], label='Predicted Revenue', linestyle='--')
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    ax.set_title("Sales Forecasting")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Error Metric
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    st.write(f"### 📉 RMSE: {rmse:.2f}")

else:
    st.info("Please upload a CSV file to proceed.")
