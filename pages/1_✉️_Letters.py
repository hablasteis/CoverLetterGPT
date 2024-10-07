import streamlit as st
from src.display_cover_letters import display_cover_letters
from src.chat import is_chat_visible, is_correct_chat, display_chat, set_chat_type
from utils.general import initialize_app, init_model_selection, show_model_selection

st.set_page_config(page_title="Letters", page_icon="✉️", layout="wide")

if "initialized" not in st.session_state:
    initialize_app()

with st.sidebar:
    init_model_selection()
    show_model_selection()

if is_chat_visible() and is_correct_chat("LettersView"):
    st.button("", icon=":material/arrow_back_ios_new:", on_click=set_chat_type, args=[None])
    display_chat()

else:

    st.title("Your Cover Letters")

    display_cover_letters()