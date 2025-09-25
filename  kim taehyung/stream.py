import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import re

# Load dataset
df = pd.read_csv("titanic_data (1).csv")

# Extract title from Name column
df['title'] = df['Name'].apply(lambda y: re.search(r'([A-Z][a-z]+)\.', y).group(1))

# Streamlit app
st.title("Titanic  Deaths vs Survival")


# Show value counts of titles
st.write("### Title Counts")
st.write(df['title'].value_counts())

# Create Seaborn countplot
fig, ax = plt.subplots()
sns.countplot(x="title", hue="Survived", data=df, ax=ax)
plt.xticks(rotation=45)  # rotate labels for readability
st.pyplot(fig)

