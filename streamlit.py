import streamlit as st
import pandas as pd

# Define the URL of your CSV file in the GitHub repo
csv_url = "https://raw.githubusercontent.com/Djean3/ALS/main/ALS_trial_data.csv
"

# Use pandas to load the data
@st.cache
def load_data():
    return pd.read_csv(csv_url)

# Load the data
df = load_data()

# Display the data in the Streamlit app
st.title("ALS Trial Dashboard")
st.dataframe(df)
