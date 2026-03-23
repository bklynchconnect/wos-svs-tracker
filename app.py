import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams.update({
    "axes.facecolor": "#0E3A70",    # Dark blue background for axes
    "figure.facecolor": "#0E3A70",  # Dark blue background for figure
    "axes.edgecolor": "white",       # Axes lines
    "axes.labelcolor": "white",      # Axes labels
    "xtick.color": "white",          # X-axis ticks
    "ytick.color": "white",          # Y-axis ticks
    "text.color": "white",           # Any text
    "legend.facecolor": "#2056A5",   # Legend background (slightly lighter blue)
    "legend.edgecolor": "white",     # Legend border
})

st.set_page_config(layout="wide")

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
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

def add_entry(us, them):
    # Define EST timezone (UTC-5)
    est = timezone(timedelta(hours=-5))
    ny_tz = ZoneInfo("America/New_York")
    
    # Get current time in UTC, convert to EST
    now_est = datetime.now(tz=ny_tz)
    
    # Truncate microseconds and format as string
    timestamp = now_est.replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    
    # Append to Google Sheet
    sheet.append_row([timestamp, us, them])

# ---------------------------
# UI
# ---------------------------

from PIL import Image

# Load your banner image
banner = Image.open("images/banner.png")  # Replace with your file

# Display full width
st.image(banner, use_column_width=True)

st.title("WOS SvS Score Tracker")

st.text("Check the SvS event page, go to Preparation Phase tab, note the total points for us and them and enter below (in millions, e.g., if we have 267,103,781 points then just enter 267)")


st.warning("⚠️ Don't add the full points value, just the millions (e.g., 289)!")

from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=120 * 1000, key="datarefresh")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    us = st.number_input("Us", min_value=0, key="us")

with col2:
    them = st.number_input("Them", min_value=0, key="them")

with col3:
    st.write("")  # spacing
    st.write("")  # aligns button vertically
    add_clicked = st.button("Add Entry")

if add_clicked:
    add_entry(us, them)
    st.success("Entry added!")

# ---------------------------
# Data Display
# ---------------------------
df = load_data()

if not df.empty:

    

    # ---------------------------
    # Derived Metrics
    # ---------------------------
    df["diff"] = df["us"] - df["them"]

    df["time_delta"] = df["datetime"].diff().dt.total_seconds() / 3600
    df["us_rate"] = df["us"].diff() / df["time_delta"]
    df["them_rate"] = df["them"].diff() / df["time_delta"]
    df["diff_rate"] = df["diff"].diff() / df["time_delta"]

    st.subheader("Analytics")

    col1, col2, col3 = st.columns(3)

    # Plot 1: Scores
    with col1:
        st.markdown("**Scores Over Time (x 1M)**")
        fig1, ax1 = plt.subplots()
        ax1.plot(df["datetime"], df["us"], label="Us", color="#FFD700", linewidth=3)
        ax1.plot(df["datetime"], df["them"], label="Them", color="#FF4500", linewidth=3)
        ax1.legend()
        ax1.tick_params(axis='x', rotation=90)
        ax1.grid()
        st.pyplot(fig1)

    # Plot 2: Difference
    with col2:
        st.markdown("**Score Difference (x 1M)**")
        fig2, ax2 = plt.subplots()
        ax2.plot(df["datetime"], df["diff"], label="Difference", color="#808080", linewidth=3)
        ax2.legend()
        ax2.tick_params(axis='x', rotation=90)
        ax2.grid()
        st.pyplot(fig2)

    # Plot 3: Rate of Change
    with col3:
        st.markdown("**Rate of Change (x 1M/hr)**")
        fig3, ax3 = plt.subplots()
        ax3.plot(df["datetime"], df["us_rate"], label="Us Rate", color="#FFD700", linewidth=3)
        ax3.plot(df["datetime"], df["them_rate"], label="Them Rate", color="#FF4500", linewidth=3)
        ax3.plot(df["datetime"], df["diff_rate"], label="Diff Rate", color="#808080", linewidth=3)
        ax3.legend()
        ax3.tick_params(axis='x', rotation=90)
        ax3.grid()
        st.pyplot(fig3)

    st.subheader("Data Table")
    st.dataframe(df)