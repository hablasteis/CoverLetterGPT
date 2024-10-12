import streamlit as st
import os
import re
import json
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


def extract_cover_letter(text):
    # Look for the first valid "Dear" that appears after some context
    letter_start_pattern = r'(Dear\s*(?:\w+(?:\s+\w+)*)?,\s*\n?.*?\n)'

    start_match = re.search(letter_start_pattern, text, re.IGNORECASE)

    if start_match:
        start_index = start_match.start()

    else:
        # Fail-safe: Try to find the next-to-last occurrence of ',\n'
        commas_and_newlines = [m.start() for m in re.finditer(r',\s\n', text)]
        if len(commas_and_newlines) >= 2:
            # Get the next-to-last occurrence
            comma_index = commas_and_newlines[-2]
            
            preceding_newline = text.rfind('\n', 0, comma_index)
            
            start_index = preceding_newline + 1 if preceding_newline != -1 else 0
        else:
            return ''  # If fewer than two occurrences, return empty string
        
    
    # find the closing signature
    letter_end_pattern = r'(?:(Sincerely|Best\s+regards|Warm\s+regards|Regards|Thank\s+you|Cheers)\s*,?\s*(?=\s*$|\n))' 

    end_match = re.search(letter_end_pattern, text, re.DOTALL | re.IGNORECASE)

    # Append name at the end
    if os.path.exists("info.json"):
        with open("info.json", 'r') as file:
            info = json.load(file)
        name = info["name"].strip()
    else:
        name = None

    if end_match:
        end_index = end_match.end(1)  
        cover_letter = text[start_index:end_index+1]
        
        return f"{cover_letter} \n {name}" if name else cover_letter[-1]


    # Fail-safe: If no specific end pattern found, find the last comma and newline
    last_comma_index = text[start_index:].rfind(',')
    last_newline_index = text[start_index:].rfind('\n')

    # We take the smaller index of the two, and ensure they are valid
    if last_comma_index != -1 and last_newline_index != -1:
        end_index = min(last_comma_index, last_newline_index) + 1  
        cover_letter = text[start_index:start_index + end_index].strip()
        return f"{cover_letter} \n {name}" if name else cover_letter[-1]

    return ''
