import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")

# Title
st.title("💼 Credit Risk Benchmark Dashboard")

# Load dataset
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# Sidebar file upload
st.sidebar.header("📤 Upload Your CSV File")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    df = load_data("Credit Risk Benchmark Dataset.csv")

# Navigation options
page = st.sidebar.radio("📑 Navigation", ["Raw Data", "Filter Data", "Summary", "Graphs & Charts"])

# ------------------ RAW DATA ------------------
if page == "Raw Data":
    st.subheader("📋 Raw Dataset")
    st.write(f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
    

    st.markdown("---")
    if st.button("🔗 Go to Kaggle Dataset Page"):
        st.markdown("[Click here to open in Kaggle](https://www.kaggle.com/datasets/adilshamim8/credit-risk-benchmark-dataset)", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# ------------------ FILTER DATA ------------------
elif page == "Filter Data":
    st.subheader("🔍 Filter Dataset")
    filtered_df = df.copy()

    if "age" in df.columns:
        age_min, age_max = int(df["age"].min()), int(df["age"].max())
        age_range = st.slider("Age Range", age_min, age_max, (age_min, age_max))
        filtered_df = filtered_df[(filtered_df["age"] >= age_range[0]) & (filtered_df["age"] <= age_range[1])]

    if "monthly_inc" in df.columns:
        inc_min, inc_max = int(df["monthly_inc"].min()), int(df["monthly_inc"].max())
        inc_range = st.slider("Monthly Income Range", inc_min, inc_max, (inc_min, inc_max))
        filtered_df = filtered_df[(filtered_df["monthly_inc"] >= inc_range[0]) & (filtered_df["monthly_inc"] <= inc_range[1])]

    if "real_estate" in df.columns:
        real_estate_opts = df["real_estate"].dropna().unique().tolist()
        selected_re = st.selectbox("Has Real Estate?", options=real_estate_opts)
        filtered_df = filtered_df[filtered_df["real_estate"] == selected_re]

    if "dependents" in df.columns:
        dep_opts = df["dependents"].dropna().unique().tolist()
        selected_deps = st.multiselect("Number of Dependents", options=dep_opts, default=dep_opts)
        filtered_df = filtered_df[filtered_df["dependents"].isin(selected_deps)]

    st.markdown("### 🧾 Filtered Data")
    st.write(f"{filtered_df.shape[0]} records match your criteria.")
    st.dataframe(filtered_df, use_container_width=True)

# ------------------ SUMMARY ------------------
elif page == "Summary":
    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    st.markdown("### 📌 Column Data Types")
    st.write(df.dtypes)

# ------------------ GRAPHS ------------------
elif page == "Graphs & Charts":
    st.subheader("📈 Graphs & Charts")
    chart_df = df.dropna()

    if "age" in chart_df.columns:
        st.markdown("### Age Distribution")
        fig1, ax1 = plt.subplots()
        sns.histplot(chart_df["age"], kde=True, ax=ax1, color="lightblue")
        st.pyplot(fig1)

    if "monthly_inc" in chart_df.columns:
        st.markdown("### Monthly Income Distribution")
        fig2, ax2 = plt.subplots()
        sns.histplot(chart_df["monthly_inc"], kde=True, ax=ax2, color="green")
        st.pyplot(fig2)

    st.markdown("### Correlation Heatmap")
    numeric_cols = chart_df.select_dtypes(include=["float64", "int64"])
    if not numeric_cols.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", ax=ax3)
        st.pyplot(fig3)
    else:
        st.info("No numeric columns available for heatmap.")
