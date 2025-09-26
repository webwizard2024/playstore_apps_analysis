import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# Load dataset
# ========================
df = pd.read_csv("googleplaystore.csv")

# ========================
# Data Cleaning
# ========================

# Clean Installs (remove + , , M , K etc.)
def clean_installs(x):
    if pd.isna(x):
        return 0
    x = str(x).replace(",", "").replace("+", "").strip()
    if "M" in x:
        return int(float(x.replace("M", "")) * 1_000_000)
    elif "K" in x:
        return int(float(x.replace("K", "")) * 1_000)
    elif x.isdigit():
        return int(x)
    else:
        return 0

df["Installs"] = df["Installs"].apply(clean_installs)

# Clean Reviews (make sure numeric)
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)

# Clean Rating (numeric, drop invalid)
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Drop rows with missing Category
df = df.dropna(subset=["Category"])

# ========================
# Streamlit App
# ========================
st.title("📱 Google Play Store Analysis")

# ========================
# Sidebar Filters
# ========================
st.sidebar.header("Filters")

# Dropdown: Category
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Slider: Minimum Rating
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)

# Slider: Minimum Installs
min_installs = st.sidebar.slider("Minimum Installs", 0, int(df["Installs"].max()), 0, step=1000)

# Apply filters
filtered = df.copy()
if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]
filtered = filtered[(filtered["Rating"] >= min_rating) & (filtered["Installs"] >= min_installs)]

st.write(f"### Showing {len(filtered)} apps after filters")

# ========================
# Average Rating + Histogram
# ========================
if selected_category != "All" and not filtered.empty:
    avg_rating = filtered["Rating"].mean()
    st.metric(label=f"Average Rating in {selected_category}", value=round(avg_rating, 2))

    fig, ax = plt.subplots()
    filtered["Rating"].plot(kind="hist", bins=20, ax=ax, color="skyblue", edgecolor="black")
    ax.set_title(f"Ratings Distribution in {selected_category}")
    ax.set_xlabel("Rating")
    st.pyplot(fig)

# ========================
# Top Apps Table (by Installs) with link
# ========================
st.subheader("Top 10 Apps by Installs")
if "App" in filtered.columns and not filtered.empty:
    top_apps = filtered.sort_values(by="Installs", ascending=False).head(10)
    if "App" in top_apps.columns:
        # Fake "Visit Store" link (placeholder)
        top_apps["Visit Store"] = [
            "https://play.google.com/store/apps/details?id=" + str(i) for i in top_apps.index
        ]
        st.dataframe(top_apps[["App", "Category", "Installs", "Rating", "Reviews", "Visit Store"]])

# ========================
# Bar chart: Top Categories
# ========================
st.subheader("Top 10 Categories by Average Rating")
cat_rating = df.groupby("Category")["Rating"].mean().sort_values(ascending=False).head(10)
st.bar_chart(cat_rating)

st.subheader("Top 10 Categories by Number of Apps")
cat_count = df["Category"].value_counts().head(10)
st.bar_chart(cat_count)

# ========================
# Scatter Plot: Reviews vs Rating
# ========================
st.subheader("Reviews vs Rating (log scale)")
mask = (filtered["Reviews"] > 0) & (filtered["Rating"].notna())
if mask.any():
    fig, ax = plt.subplots()
    ax.scatter(filtered.loc[mask, "Reviews"], filtered.loc[mask, "Rating"], alpha=0.5)
    ax.set_xscale("log")
    ax.set_xlabel("Reviews (log scale)")
    ax.set_ylabel("Rating")

    ax.set_title("Reviews vs Rating")
    st.pyplot(fig)
