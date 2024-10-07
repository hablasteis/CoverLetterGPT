import streamlit as st
from src.display_cover_letters import display_cover_letters

st.set_page_config(page_title="Letters", page_icon="✉️", layout="wide")

st.title("Your Cover Letters")


display_cover_letters()