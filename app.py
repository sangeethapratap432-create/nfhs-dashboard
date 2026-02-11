import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

st.title("📊 National Family Health Survey Dashboard")
st.markdown("Interactive dashboard for NFHS Indicators")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

# Select Columns / Indicators
numeric_columns = df.select_dtypes(include='number').columns.tolist()

indicator = st.sidebar.selectbox(
    "Select Indicator",
    numeric_columns
)

# Optional State Filter if exists
if "State" in df.columns:
    states = st.sidebar.multiselect(
        "Select State",
        df["State"].unique(),
        default=df["State"].unique()
    )
    df = df[df["State"].isin(states)]

# -----------------------------
# Main Dashboard
# -----------------------------

col1, col2 = st.columns(2)

# Summary Metric
with col1:
    st.subheader("📈 Average Value")
    st.metric(
        label="Mean",
        value=round(df[indicator].mean(),2)
    )

# Data Table
with col2:
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

# -----------------------------
# Chart Section
# -----------------------------
st.subheader("📊 Indicator Visualization")

# Bar Chart if State exists
if "State" in df.columns:
    fig = px.bar(
        df,
        x="State",
        y=indicator,
        title=f"{indicator} by State"
    )
else:
    fig = px.histogram(
        df,
        x=indicator,
        title=f"Distribution of {indicator}"
    )

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.subheader("🔥 Correlation Heatmap")

corr = df[numeric_columns].corr()

heatmap = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Between Indicators"
)

st.plotly_chart(heatmap, use_container_width=True)
