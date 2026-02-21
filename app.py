import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- Page Config ----------------
st.set_page_config(page_title="Tourist Analytics Dashboard", layout="wide")

st.title("🌍 Tourist Analytics Dashboard")

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    # Load all required files
    transaction = pd.read_excel("Transaction.xlsx")
    user = pd.read_excel("User.xlsx")
    continent = pd.read_excel("Continent.xlsx")
    mode = pd.read_excel("Mode.xlsx")

    # Merge transaction with user
    df = transaction.merge(user, on="UserId", how="left")

    # Merge continent to get continent names
    df = df.merge(continent, on="ContinentId", how="left")

    # Merge mode to get visit mode names (Business, Family, etc.)
    df = df.merge(mode, on="VisitModeId", how="left")

    # Clean column names
    df.columns = df.columns.str.strip()

    return df


# 🔥 Important: Load dataframe
df = load_data()

# ---------------- Sidebar Filters ----------------
st.sidebar.header("🔎 Filter Data")

# Year Filter
year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["VisitYear"].dropna().unique()),
    default=sorted(df["VisitYear"].dropna().unique())
)

# Continent Filter (Text, not ID)
continent_filter = st.sidebar.multiselect(
    "Select Continent",
    df["Continent"].dropna().unique(),
    default=df["Continent"].dropna().unique()
)

# Visit Mode Filter (Text, not ID)
mode_filter = st.sidebar.multiselect(
    "Select Visit Mode",
    df["VisitMode"].dropna().unique(),
    default=df["VisitMode"].dropna().unique()
)

# Rating Filter
rating_filter = st.sidebar.slider(
    "Select Rating Range",
    int(df["Rating"].min()),
    int(df["Rating"].max()),
    (int(df["Rating"].min()), int(df["Rating"].max()))
)

# ---------------- Apply Filters ----------------
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

# Visits by Year
st.subheader("📊 Visits by Year")
year_chart = filtered_df["VisitYear"].value_counts().reset_index()
year_chart.columns = ["Year", "Visits"]
fig1 = px.bar(year_chart, x="Year", y="Visits", color="Visits")
st.plotly_chart(fig1, use_container_width=True)

# Rating Distribution
st.subheader("⭐ Rating Distribution")
fig2 = px.histogram(filtered_df, x="Rating", nbins=10, color="Rating")
st.plotly_chart(fig2, use_container_width=True)

# Visit Mode Distribution (Shows names like Business, Family, Couples)
st.subheader("🚗 Visit Mode Distribution")
mode_chart = filtered_df["VisitMode"].value_counts().reset_index()
mode_chart.columns = ["Visit Mode", "Count"]
fig3 = px.pie(mode_chart, names="Visit Mode", values="Count")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- Dataset Preview ----------------
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(20))
