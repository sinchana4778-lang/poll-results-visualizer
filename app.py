import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Poll Visualizer", layout="wide")

# Style
sns.set_style("whitegrid")

# Title
st.title("📊 Poll Results Visualizer")
st.markdown("Analyze survey data with interactive insights and visualizations")

# -----------------------------
# 📂 FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload your poll data (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
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

# Apply filters
filtered_df = df[
    (df["region"].isin(regions)) &
    (df["age_group"].isin(ages))
]

# -----------------------------
# 📊 METRICS (NEW)
# -----------------------------
vote_counts = filtered_df["selected_option"].value_counts()
percentages = (vote_counts / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Responses", len(filtered_df))

if len(filtered_df) > 0:
    col2.metric("Top Option", vote_counts.idxmax())
    col3.metric("Top %", f"{percentages.max():.2f}%")
else:
    col2.metric("Top Option", "N/A")
    col3.metric("Top %", "N/A")

# -----------------------------
# 📊 DATA PREVIEW
# -----------------------------
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head())

# -----------------------------
# 📊 CHARTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bar Chart")
    fig1, ax1 = plt.subplots()
    sns.barplot(x=vote_counts.index, y=vote_counts.values, ax=ax1)
    ax1.set_xlabel("Options")
    ax1.set_ylabel("Votes")
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
# 🧠 INSIGHTS
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

# -----------------------------
# ⬇ DOWNLOAD BUTTON
# -----------------------------
st.subheader("Download Results")

if len(filtered_df) > 0:
    st.download_button(
        label="Download Summary CSV",
        data=vote_counts.to_csv(),
        file_name="poll_summary.csv",
        mime="text/csv"
    )