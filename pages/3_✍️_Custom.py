import streamlit as st
import os

from src.generator import CustomLetterGenerator
from src.job import CustomJob
from utils.general import show_model_selection, init_model_selection, initialize_app, split_by_dear

st.set_page_config(page_title="Custom", page_icon="✍️", layout="wide")

if "initialized" not in st.session_state:
    initialize_app()

with st.sidebar:
    init_model_selection()
    show_model_selection()


col1, col2 = st.columns([4, 1])

with col1:
    st.header("Create Custom Cover Letter")

with col2:
    if st.button("New Letter"):
        if "job_id" in st.session_state:
            del st.session_state.job_id

st.write("")

col3, col4 = st.columns([1, 1])
with col3:
    st.subheader(" (Optional) Role")    
    role = st.text_input("e.g. \"Software Engineer\"")
with col4:
    st.subheader(" (Optional) Company Name")    
    company = st.text_input("e.g. \"Microsoft\"")

st.subheader("1. Provide Job Description")
job_description = st.text_area("Paste the job description here:")

generate_button = st.button("Generate Cover Letter")

job_id = None

if generate_button and job_description:
    st.session_state.job_id = f"{hash(job_description)}"
    job_id = st.session_state.job_id

    job = CustomJob(
            job_id = job_id,
            description = job_description,
            company = company,
            title = role
        )

    generator = CustomLetterGenerator(job_id=job_id, title=None, description=job_description)

    with st.spinner("Please wait..."):
        generator.generate(st.session_state.model)
    
    with open(os.path.join(CustomLetterGenerator.get_class_path(), str(job_id)) + ".txt", "r") as file:
        letter = file.read()
        _, letter = split_by_dear(letter)

    job.save_job()

    st.session_state.messages[job_id] = [{"role": "assistant", "content": letter}]

    st.session_state["edit_letter"]=job_id
    st.switch_page("pages/0_💬_Chat.py")