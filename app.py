import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------------------
# Google Sheets Connection
# ---------------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)

client = gspread.authorize(creds)
sheet = client.open("wos_svs_tracker").sheet1

# ---------------------------
# Load Data
# ---------------------------
def load_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    if not df.empty:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
    
    return df

# ---------------------------
# Append Data
# ---------------------------
def add_entry(us, them):
    now = datetime.now().isoformat()
    sheet.append_row([now, us, them])

# ---------------------------
# UI
# ---------------------------
st.title("Score Tracker")

us = st.number_input("Us", min_value=0)
them = st.number_input("Them", min_value=0)

if st.button("Add Entry"):
    add_entry(us, them)
    st.success("Entry added!")

# ---------------------------
# Data Display
# ---------------------------
df = load_data()

if not df.empty:

    st.subheader("Data Table")
    st.dataframe(df)

    # ---------------------------
    # Derived Metrics
    # ---------------------------
    df["diff"] = df["us"] - df["them"]

    df["time_delta"] = df["datetime"].diff().dt.total_seconds() / 60
    df["us_rate"] = df["us"].diff() / df["time_delta"]
    df["them_rate"] = df["them"].diff() / df["time_delta"]
    df["diff_rate"] = df["diff"].diff() / df["time_delta"]

    # ---------------------------
    # Plot 1: Scores
    # ---------------------------
    st.subheader("Scores Over Time")

    fig1, ax1 = plt.subplots()
    ax1.plot(df["datetime"], df["us"], label="Us")
    ax1.plot(df["datetime"], df["them"], label="Them")
    ax1.legend()
    st.pyplot(fig1)

    # ---------------------------
    # Plot 2: Difference
    # ---------------------------
    st.subheader("Score Difference")

    fig2, ax2 = plt.subplots()
    ax2.plot(df["datetime"], df["diff"], label="Difference")
    ax2.legend()
    st.pyplot(fig2)

    # ---------------------------
    # Plot 3: Rate of Change
    # ---------------------------
    st.subheader("Rate of Change (Points per Minute)")

    fig3, ax3 = plt.subplots()
    ax3.plot(df["datetime"], df["us_rate"], label="Us Rate")
    ax3.plot(df["datetime"], df["them_rate"], label="Them Rate")
    ax3.plot(df["datetime"], df["diff_rate"], label="Diff Rate")
    ax3.legend()
    st.pyplot(fig3)