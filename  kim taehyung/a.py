import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Main title
st.title("My First Streamlit App 🎉")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.write("This is the sidebar section.")

choice = st.sidebar.radio(
    "Select a section",
    ["Home", "Graph of Student Scores"]
)

# Sections
if choice == "Home":
    st.subheader("Welcome to the Home Section")
    st.write("Use the sidebar to explore different features.")

elif choice == "Graph of Student Scores":
    st.subheader("📊 Student Scores Bar Graph")

    # Dummy data
    data = {
        "Students": ["Ali", "Sara", "Ahmed", "Zara", "Usman"],
        "Scores": [85, 92, 78, 88, 95]
    }
    df = pd.DataFrame(data)

    # Show table
    st.write("### Data Table")
    st.dataframe(df)

    # Create bar chart with matplotlib
    fig, ax = plt.subplots()
    ax.bar(df["Students"], df["Scores"], color="skyblue")
    ax.set_ylabel("Scores")
    ax.set_title("Student Scores")

    st.pyplot(fig)
