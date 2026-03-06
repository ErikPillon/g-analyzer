import streamlit as st
from entitites.activities import Activity
from presentation.state.session_state_manager import initialize_session_state
import pandas as pd
import os
from glob import glob

initialize_session_state()


st.set_page_config(page_title="Triathlon Performance Lab", layout="wide")


@st.cache_data
def get_all_data():
    activities = st.session_state.activities

    df = pd.DataFrame(activities).groupby("date").sum().sort_index()
    # Fill missing dates so the EWMA is accurate
    idx = pd.date_range(df.index.min(), df.index.max())
    df = df.reindex(idx, fill_value=0)

    # Math for ATL/CTL
    df["CTL"] = df["trimp"].ewm(span=42).mean()
    df["ATL"] = df["trimp"].ewm(span=7).mean()
    df["TSB"] = df["CTL"].shift(1) - df["ATL"].shift(1)
    df["AC_Ratio"] = df["ATL"] / df["CTL"]
    return df


st.title("🏊‍♂️ Triathlon Training Analytics")

data = get_all_data()

# Plotting
st.subheader("Fitness vs. Fatigue (CTL vs ATL)")
st.line_chart(data[["CTL", "ATL"]])

st.subheader("Training Stress Balance (TSB)")
st.area_chart(data["TSB"])

st.subheader("A:C Workload Ratio")
st.line_chart(data["AC_Ratio"])
st.write("Target Zone: 0.8 - 1.3")
