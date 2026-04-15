import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from pages.style_utils import DAY_STYLE, apply_style

st.set_page_config(page_title="Insights · FlowState", layout="wide")
st.markdown(DAY_STYLE, unsafe_allow_html=True)
apply_style()

sns.set_style("whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("Product_Sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    df["Profit"] = df["TotalPrice"] * 0.2
    return df

df = load_data()

st.markdown("""
<div class="page-header">
  <div class="page-title">🧠 AI Insights & Advanced Analytics</div>
  <div class="page-sub">Predictive modeling, clustering, anomalies, and feature importance</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# 🔮 1. PREDICTIVE TREND
# -------------------------------
st.markdown("### 🔮 Revenue Forecast")

trend = df.groupby("OrderDate")["TotalPrice"].sum().reset_index()
trend["t"] = np.arange(len(trend))

model = LinearRegression()
model.fit(trend[["t"]], trend["TotalPrice"])

trend["Prediction"] = model.predict(trend[["t"]])

fig, ax = plt.subplots(figsize=(8,3.8))
sns.lineplot(data=trend, x="OrderDate", y="TotalPrice", label="Actual", linewidth=2)
sns.lineplot(data=trend, x="OrderDate", y="Prediction", label="Forecast", linestyle="--")

plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.info("📌 Insight: Revenue shows a steady trend, and linear regression projects future growth patterns.")

# -------------------------------
# 🧩 2. CLUSTERING
# -------------------------------
st.markdown("### 🧩 Customer/Product Clustering")

X = df[["TotalPrice", "Quantity"]]
kmeans = KMeans(n_clusters=3, random_state=0)
df["Cluster"] = kmeans.fit_predict(X)

fig, ax = plt.subplots(figsize=(6,3))
sns.scatterplot(data=df, x="TotalPrice", y="Quantity", hue="Cluster", palette="Set2")

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.info("📌 Insight: Data points are grouped into clusters showing similar purchasing behavior.")

# -------------------------------
# ⚠️ 3. ANOMALY DETECTION
# -------------------------------
st.markdown("### ⚠️ Anomaly Detection")

df["z"] = (df["TotalPrice"] - df["TotalPrice"].mean()) / df["TotalPrice"].std()
df["Anomaly"] = df["z"].abs() > 3

fig, ax = plt.subplots(figsize=(8,3.8))
sns.scatterplot(
    data=df,
    x="OrderDate",
    y="TotalPrice",
    hue="Anomaly",
    palette={True:"red", False:"blue"}
)

plt.xticks(rotation=30)
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.info("📌 Insight: Red points indicate unusual spikes or drops in revenue (outliers).")

# -------------------------------
# 🤖 4. CLASSIFICATION
# -------------------------------
st.markdown("### 🤖 Classification (High vs Low Value Orders)")

df["HighValue"] = df["TotalPrice"] > df["TotalPrice"].median()

X = df[["Quantity"]]
y = df["HighValue"]

clf = LogisticRegression()
clf.fit(X, y)

df["Prediction"] = clf.predict(X)

fig, ax = plt.subplots(figsize=(8,3.8))
sns.scatterplot(
    data=df,
    x="Quantity",
    y="TotalPrice",
    hue="Prediction",
    palette={True:"green", False:"orange"}
)

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.info("📌 Insight: Orders are classified into high and low value based on quantity patterns.")

# -------------------------------
# 🌳 5. FEATURE IMPORTANCE
# -------------------------------
st.markdown("### 🌳 Feature Importance")

df_model = df.copy()
df_model = df_model.drop(columns=["OrderDate", "DeliveryDate"], errors="ignore")

for col in df_model.select_dtypes(include="object").columns:
    df_model[col] = LabelEncoder().fit_transform(df_model[col].astype(str))

X = df_model.drop(columns=["TotalPrice"])
y = df_model["TotalPrice"]
y_class = (y > y.median()).astype(int)

rf = RandomForestClassifier(n_estimators=50, random_state=42)
rf.fit(X, y_class)

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values("Importance", ascending=False)

fig, ax = plt.subplots(figsize=(6,3.8))
sns.barplot(data=importance.head(10), x="Importance", y="Feature", palette="coolwarm")

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.info("📌 Insight: Features with higher importance have a stronger influence on revenue prediction.")