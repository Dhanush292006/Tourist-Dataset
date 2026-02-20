import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tourist Analytics Dashboard", layout="wide")

st.title("🌍 Tourist Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_excel("Transaction.xlsx")

df = load_data()

# ---------------- Filters ----------------
st.sidebar.header("Filter Data")

year_filter = st.sidebar.selectbox(
    "Select Year",
    sorted(df["VisitYear"].unique())
)

filtered_df = df[df["VisitYear"] == year_filter]

# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Transactions", len(filtered_df))
col2.metric("Unique Users", filtered_df["UserId"].nunique())
col3.metric("Average Rating", round(filtered_df["Rating"].mean(), 2))
col4.metric("Unique Attractions", filtered_df["AttractionId"].nunique())

st.divider()

# ---------------- Charts ----------------
st.subheader("📊 Visits by Year")
year_chart = filtered_df["VisitYear"].value_counts().reset_index()
year_chart.columns = ["Year", "Visits"]
fig1 = px.bar(year_chart, x="Year", y="Visits")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("⭐ Rating Distribution")
fig2 = px.histogram(filtered_df, x="Rating")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🚗 Visit Mode Distribution")
mode_chart = filtered_df["VisitMode"].value_counts().reset_index()
mode_chart.columns = ["Mode", "Count"]
fig3 = px.pie(mode_chart, names="Mode", values="Count")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head())
