import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from src.retriever import LinkedinRetriever, CustomRetriever
from src.display_cover_letters import display_cover_letters
from src.chat import is_chat_visible, display_chat, is_correct_chat
from utils.general import show_model_selection, init_model_selection, initialize_app, exists_cv
    

st.set_page_config(page_title="Search", page_icon="🔎", layout="wide")

if "initialized" not in st.session_state:
    initialize_app()

with st.sidebar:
    init_model_selection()
    show_model_selection()

job_board = st.empty()


tab1, tab2 = st.tabs(["LinkedIn", "✍️ Custom"])

# Warn user if CV is not registered
exists_cv()

with tab1:
    retriever = LinkedinRetriever()
    retriever.display_search_bar()
    
    if is_chat_visible() and is_correct_chat(retriever):
        display_chat()

with tab2:
    retriever = CustomRetriever()
    retriever.display_search_bar()

    if is_chat_visible() and is_correct_chat(retriever):
        display_chat()



if "jobs" not in st.session_state and not is_chat_visible():
    st.header("")

    st.header("Your Letters")
    st.write("")

    display_cover_letters()
