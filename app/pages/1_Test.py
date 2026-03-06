import streamlit as st
from presentation.state.session_state_manager import initialize_session_state


initialize_session_state()

st.set_page_config(page_title="Triathlon Performance Lab", layout="wide")

st.title("Triathlon Performance Lab")
st.write("Welcome to the Triathlon Performance Lab!")
