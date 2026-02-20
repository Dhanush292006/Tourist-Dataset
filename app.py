import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Tourist Dataset App", layout="wide")
st.title("🌍 Tourist Dataset Analysis")

@st.cache_data
def load_data():
    try:
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "Transaction.xlsx")  # ✅ FIXED
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.write("Current directory:", os.getcwd())
        st.write("Files available:", os.listdir())
        st.stop()

df = load_data()

st.subheader("📊 Dataset Preview")
st.dataframe(df.head())

st.subheader("📈 Basic Statistics")
st.write(df.describe())
