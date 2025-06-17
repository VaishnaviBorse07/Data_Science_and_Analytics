import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Set up page
st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("🛍️ Customer Segmentation Dashboard")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("Mall_Customers.csv")
    df['GenderEncoded'] = LabelEncoder().fit_transform(df['Gender'])
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("🔧 Configuration")
selected_features = st.sidebar.multiselect(
    "Select features for clustering",
    ['Age', 'Annual Income (k$)', 'Spending Score (1-100)', 'GenderEncoded'],
    default=['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
)

k = st.sidebar.slider("Select number of clusters (k)", 2, 10, 5)

# Main layout
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)

# Prepare data
X = df[selected_features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow Method
st.subheader("📉 Elbow Method")
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

fig1, ax1 = plt.subplots()
ax1.plot(range(1, 11), wcss, marker='o')
ax1.set_title("Elbow Method to find optimal k")
ax1.set_xlabel("Number of clusters")
ax1.set_ylabel("WCSS")
st.pyplot(fig1)

# Clustering
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Cluster names (optional logic)
cluster_names = {
    0: "🎯 Target",
    1: "💼 Average Spender",
    2: "🛒 Low Spender",
    3: "💰 High Income",
    4: "🎉 Young Spender"
}
df['Segment'] = df['Cluster'].map(cluster_names).fillna("Segment " + df['Cluster'].astype(str))

# PCA for visualization
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)
df['PCA1'], df['PCA2'] = components[:, 0], components[:, 1]

# 2D cluster plot
st.subheader("📌 Cluster Visualization (PCA)")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Segment', palette='Set2', ax=ax2)
ax2.set_title("Customer Segments")
st.pyplot(fig2)

# Cluster profile table
st.subheader("📊 Cluster Profiles")
cluster_summary = df.groupby('Segment')[selected_features].mean().round(1)
st.dataframe(cluster_summary)

# Gender breakdown per cluster
st.subheader("🧍 Gender Distribution per Segment")
gender_plot = df.groupby(['Segment', 'Gender']).size().unstack().fillna(0)
st.bar_chart(gender_plot)

# Export segmented data
st.subheader("⬇️ Download Segmented Dataset")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "customer_segments.csv", "text/csv")
