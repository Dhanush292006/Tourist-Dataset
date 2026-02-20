import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Tourist Dataset App", layout="wide")

st.title("🌍 Tourist Dataset Analysis")

# ----------------------------
# Load Data Function
# ----------------------------
@st.cache_data
def load_data():
    try:
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "data", "Transaction.xlsx")
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error("Error loading file.")
        st.write("Current directory:", os.getcwd())
        st.write("Files available:", os.listdir())
        st.stop()

# ----------------------------
# Load Dataset
# ----------------------------
df = load_data()

# ----------------------------
# Display Data
# ----------------------------
st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

st.subheader("📈 Basic Statistics")
st.write(df.describe())

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Options")

if len(df.columns) > 0:
    selected_column = st.sidebar.selectbox("Select Column", df.columns)

    if df[selected_column].dtype == "object":
        unique_values = df[selected_column].unique()
        selected_value = st.sidebar.selectbox("Select Value", unique_values)
        filtered_df = df[df[selected_column] == selected_value]
        st.write("Filtered Data:")
        st.dataframe(filtered_df)
    else:
        st.info("Selected column is numeric.")

