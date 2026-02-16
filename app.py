import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Tourism Experience Analytics", layout="wide")

st.title("🌍 Tourism Experience Analytics")
st.write("Regression | Classification | Recommendation System")

@st.cache_data
def load_data():
    transaction = pd.read_excel("Transaction.xlsx")
    user = pd.read_excel("User.xlsx")
    city = pd.read_excel("City.xlsx")
    region = pd.read_excel("Region.xlsx")
    country = pd.read_excel("Country.xlsx")
    continent = pd.read_excel("Continent.xlsx")

    df = transaction.merge(user, on="UserId", how="left")
    df = df.merge(city, on="CityId", how="left")
    df = df.merge(country, on="CountryId", how="left")
    df = df.merge(region, on="RegionId", how="left")
    df = df.merge(continent, on="ContinentId", how="left")

    return df

df = load_data()

menu = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📈 Predict Rating", "🎯 Predict Visit Mode", "🤖 Recommend Attractions"]
)

# ---------------- Dashboard ----------------
if menu == "📊 Dashboard":
    st.subheader("Rating Distribution")
    st.bar_chart(df["Rating"].value_counts())

    st.subheader("Visit Mode Distribution")
    st.bar_chart(df["VisitMode"].value_counts())

# ---------------- Regression ----------------
elif menu == "📈 Predict Rating":

    le = LabelEncoder()
    df["Continent"] = le.fit_transform(df["Continent"])

    X = df[["Continent", "VisitYear", "VisitMonth"]]
    y = df["Rating"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    continent_input = st.selectbox("Select Continent", df["Continent"].unique())
    year_input = st.slider("Visit Year", int(df["VisitYear"].min()), int(df["VisitYear"].max()))
    month_input = st.slider("Visit Month", 1, 12)

    if st.button("Predict Rating"):
        input_data = np.array([[continent_input, year_input, month_input]])
        prediction = model.predict(input_data)
        st.success(f"Predicted Rating: {round(prediction[0],2)} ⭐")

# ---------------- Classification ----------------
elif menu == "🎯 Predict Visit Mode":

    le = LabelEncoder()
    df["Continent"] = le.fit_transform(df["Continent"])
    df["VisitMode"] = le.fit_transform(df["VisitMode"])

    X = df[["Continent", "VisitYear", "VisitMonth"]]
    y = df["VisitMode"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    continent_input = st.selectbox("Select Continent", df["Continent"].unique())
    year_input = st.slider("Visit Year", int(df["VisitYear"].min()), int(df["VisitYear"].max()))
    month_input = st.slider("Visit Month", 1, 12)

    if st.button("Predict Visit Mode"):
        input_data = np.array([[continent_input, year_input, month_input]])
        prediction = clf.predict(input_data)
        st.success(f"Predicted Visit Mode: {prediction[0]}")

# ---------------- Recommendation ----------------
elif menu == "🤖 Recommend Attractions":

    user_item = df.pivot_table(index="UserId", columns="AttractionId", values="Rating").fillna(0)

    similarity = cosine_similarity(user_item)
    similarity_df = pd.DataFrame(similarity, index=user_item.index, columns=user_item.index)

    selected_user = st.selectbox("Select User", user_item.index)

    if st.button("Get Recommendations"):
        similar_users = similarity_df[selected_user].sort_values(ascending=False)[1:6]

        recommended = (
            user_item.loc[similar_users.index]
            .mean()
            .sort_values(ascending=False)
            .head(5)
        )

        st.write("Top Recommended Attraction IDs:")
        st.write(recommended.index.tolist())
