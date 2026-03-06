import streamlit as st
from presentation.state.session_state_manager import initialize_session_state

initialize_session_state()


def main():
    st.title("Welcome to the Streamlit App!")
    return


if __name__ == "__main__":
    main()
