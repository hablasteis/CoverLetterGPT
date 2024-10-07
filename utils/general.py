import streamlit as st
import os
from src.job import LinkedinJob, CustomJob
from src.generator import LinkedinLetterGenerator, CustomLetterGenerator


#PAGINATION_SIZE = 25 # See AuthenticatedStrategy in LinkedinScraper

def initialize_app():
    st.session_state.initialized = True
        
    if 'cover_letters' not in st.session_state:
        st.session_state.cover_letters = {}

    if 'messages' not in st.session_state:
        st.session_state.messages = {}

    # Create necessary folders
    create_folders()

def create_folders():
    LinkedinLetterGenerator.initialize()
    LinkedinJob.initialize()
    CustomJob.initialize()
    CustomLetterGenerator.initialize()


def split_by_dear(content):
    """
    Splits the cover letter content into two parts:
    - The part before the line that starts with 'Dear' and ends with a comma.
    - The line containing 'Dear' and everything after it.
    
    Returns a tuple (pre_dear_part, dear_line, cover_letter_main).
    """

    import re
    
    dear_split = re.split(r"(^Dear .*?,\n)", content, maxsplit=1, flags=re.MULTILINE)

    if len(dear_split) == 3:
        pre_dear_part = dear_split[0]  # Text before "Dear"
        dear_line = dear_split[1]      # The line with "Dear"
        cover_letter_main = dear_split[2]  # The main content of the cover letter
        return pre_dear_part, dear_line + cover_letter_main
    else:
        return None, content  # Return entire content as main if "Dear" is not found
    
def update_model():
    st.session_state.model = st.session_state.model_name

def init_model_selection():
    models = ["gpt-4o-mini", "gpt-4o", "gpt-4"]
    if "model" in st.session_state:
        st.session_state["model_name"] = st.session_state["model"]
    else:
        st.session_state["model"] = models[0]

def show_model_selection():
    models = ["gpt-4o-mini", "gpt-4o", "gpt-4"]
    st.selectbox("Select Model", models, on_change=update_model, key="model_name")
    
def exists_cv():
    if not os.path.exists("cv.txt"):
        st.warning("😲 Psst! Your CV is empty, write it in the Profile section to generate cover letters!")