import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create folders if not exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

print("\n--- POLL RESULTS VISUALIZER STARTED ---\n")

# ----------------------------
# 1. Generate Synthetic Data
# ----------------------------
np.random.seed(42)

n = 500

data = pd.DataFrame({
    "respondent_id": range(1, n+1),
    "region": np.random.choice(["North", "South", "East", "West"], n),
    "age_group": np.random.choice(["18-25", "26-35", "36-50"], n),
    "question": "Favorite Product",
    "selected_option": np.random.choice(
        ["Product A", "Product B", "Product C"],
        n,
        p=[0.4, 0.35, 0.25]   # Weighted to create realistic result
    ),
    "date": pd.date_range(start="2024-01-01", periods=n, freq='D')
})

data_path = "data/poll_data.csv"
data.to_csv(data_path, index=False)

print("✅ Dataset Created at:", data_path)

# ----------------------------
# 2. Load Data
# ----------------------------
df = pd.read_csv(data_path)

print("\n📊 Raw Data Preview:\n")
print(df.head())

# ----------------------------
# 3. Cleaning
# ----------------------------
df.dropna(inplace=True)

# ----------------------------
# 4. Analysis
# ----------------------------
vote_counts = df["selected_option"].value_counts()
percentages = (vote_counts / len(df)) * 100

summary = pd.DataFrame({
    "Votes": vote_counts,
    "Percentage": percentages.round(2)
})

print("\n📈 Vote Summary:\n")
print(summary)

# Save summary
summary.to_csv("outputs/summary.csv")

# ----------------------------
# 5. Visualization
# ----------------------------

# Bar Chart
plt.figure()
sns.barplot(x=vote_counts.index, y=vote_counts.values)
plt.title("Vote Count by Option")
plt.xlabel("Options")
plt.ylabel("Votes")
plt.savefig("outputs/bar_chart.png")
plt.close()

# Pie Chart
plt.figure()
vote_counts.plot.pie(autopct='%1.1f%%')
plt.title("Vote Share")
plt.ylabel("")
plt.savefig("outputs/pie_chart.png")
plt.close()

# Region-wise Analysis
region_analysis = pd.crosstab(df["region"], df["selected_option"])

region_analysis.plot(kind="bar", stacked=True)
plt.title("Region-wise Preferences")
plt.xlabel("Region")
plt.ylabel("Votes")
plt.savefig("outputs/region_chart.png")
plt.close()

# Age Group Analysis
age_analysis = pd.crosstab(df["age_group"], df["selected_option"])

age_analysis.plot(kind="bar", stacked=True)
plt.title("Age Group Preferences")
plt.savefig("outputs/age_chart.png")
plt.close()

# ----------------------------
# 6. Insights
# ----------------------------
top_option = vote_counts.idxmax()
top_percentage = percentages.max()

print(f"\n🏆 Top Selected Option: {top_option}")
print(f"📊 Vote Share: {top_percentage:.2f}%")

print("\n--- PROJECT COMPLETED SUCCESSFULLY ---")