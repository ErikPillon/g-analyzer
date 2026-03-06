from glob import glob

import streamlit as st
from datetime import datetime
import pandas as pd
import os
from entitites.activities import Activity

root_path = "./inputs/activities/"


def initialize_session_state(debug: bool = False):
    """Initialize or retrieve the session state with repositories and services."""

    # Get current date information
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    st.session_state.setdefault("debug", debug)
    st.session_state.setdefault("current_date", current_date)
    st.session_state.setdefault("time", time)
    st.session_state.setdefault("activities", None)

    # import data if not already in session state and cache them in session state
    if st.session_state.activities is None:
        activities = []
        # Recursively find all .fit files
        files = glob(os.path.join(root_path, "**/*.fit"), recursive=True)

        for f in files:
            act = Activity(f)
            activities.append({"date": act.date, "trimp": act.calculate_trimp()})

        st.session_state["activities"] = activities
