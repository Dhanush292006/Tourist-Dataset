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

# Year Filter
year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["VisitYear"].unique()),
    default=sorted(df["VisitYear"].unique())
)

# Continent Filter
continent_filter = st.sidebar.multiselect(
    "Select Continent",
    df["Continent"].unique(),
    default=df["Continent"].unique()
)

# Visit Mode Filter
mode_filter = st.sidebar.multiselect(
    "Select Visit Mode",
    df["VisitMode"].unique(),
    default=df["VisitMode"].unique()
)

# Rating Filter
rating_filter = st.sidebar.slider(
    "Select Rating Range",
    int(df["Rating"].min()),
    int(df["Rating"].max()),
    (int(df["Rating"].min()), int(df["Rating"].max()))
)

# Apply Filters
filtered_df = df[
    (df["VisitYear"].isin(year_filter)) &
    (df["Continent"].isin(continent_filter)) &
    (df["VisitMode"].isin(mode_filter)) &
    (df["Rating"] >= rating_filter[0]) &
    (df["Rating"] <= rating_filter[1])
]

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
