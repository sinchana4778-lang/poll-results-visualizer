import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Poll Visualizer", layout="wide")

st.title("📊 Advanced Poll Results Visualizer")

# Load Data
df = pd.read_csv("data/poll_data.csv")

# -----------------------------
# 🔍 SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filter Data")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

ages = st.sidebar.multiselect(
    "Select Age Group",
    options=df["age_group"].unique(),
    default=df["age_group"].unique()
)

# Apply Filters
filtered_df = df[
    (df["region"].isin(regions)) &
    (df["age_group"].isin(ages))
]

# -----------------------------
# 📊 DATA PREVIEW
# -----------------------------
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head())

# -----------------------------
# 📊 VOTE SUMMARY
# -----------------------------
vote_counts = filtered_df["selected_option"].value_counts()
percentages = (vote_counts / len(filtered_df)) * 100

col1, col2 = st.columns(2)

with col1:
    st.subheader("Bar Chart")
    fig1, ax1 = plt.subplots()
    sns.barplot(x=vote_counts.index, y=vote_counts.values, ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Pie Chart")
    fig2, ax2 = plt.subplots()
    vote_counts.plot.pie(autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

# -----------------------------
# 🌍 REGION ANALYSIS
# -----------------------------
st.subheader("Region-wise Analysis")
region = pd.crosstab(filtered_df["region"], filtered_df["selected_option"])
st.bar_chart(region)

# -----------------------------
# 👥 AGE ANALYSIS
# -----------------------------
st.subheader("Age Group Analysis")
age = pd.crosstab(filtered_df["age_group"], filtered_df["selected_option"])
st.bar_chart(age)

# -----------------------------
# 📈 TREND ANALYSIS
# -----------------------------
st.subheader("Trend Over Time")

trend = filtered_df.groupby(["date", "selected_option"]).size().unstack()
trend = trend.fillna(0)

st.line_chart(trend)

# -----------------------------
# 🧠 SMART INSIGHTS
# -----------------------------
st.subheader("Insights")

if len(filtered_df) > 0:
    top_option = vote_counts.idxmax()
    top_percentage = percentages.max()

    st.success(f"🏆 Top Choice: {top_option} ({top_percentage:.2f}%)")

    if top_percentage > 50:
        st.info("📢 Strong majority preference detected.")
    else:
        st.warning("⚖️ No clear majority — competition is close.")

else:
    st.error("No data available for selected filters.")