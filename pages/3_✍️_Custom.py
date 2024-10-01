from openai import OpenAI
import streamlit as st
import os

from src.generator import CustomLetterGenerator
from utils.general import show_model_selection, init_model_selection, initialize_app, split_by_dear

st.set_page_config(page_title="Custom", page_icon="✍️", layout="wide")

if "initialized" not in st.session_state:
    initialize_app()

with st.sidebar:
    init_model_selection()
    show_model_selection()

client = OpenAI()

st.header("Create Custom Cover Letter")
st.write("")

st.subheader("1. Provide Job Description")
job_description = st.text_area("Paste the job description here:")

generate_button = st.button("Generate Cover Letter")


job_id = None


if generate_button and job_description:

    st.session_state.job_id = f"custom_{hash(job_description)}"
    job_id = st.session_state.job_id

    generator = CustomLetterGenerator(job_id=job_id, title=None, description=job_description)

    with st.spinner("Please wait..."):
        generator.generate(st.session_state.model)
    
    with open(os.path.join(CustomLetterGenerator.get_class_path(), str(hash(job_id))) + ".txt", "r") as file:
        letter = file.read()
        _, letter = split_by_dear(letter)

    st.session_state.messages[job_id] = [{"role": "assistant", "content": letter}]
    

if "job_id" in st.session_state:
    job_id = st.session_state["job_id"]
    if st.session_state.job_id in st.session_state.messages:
        
        for message in st.session_state.messages[job_id]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Hi! What should I change?"):
            st.session_state.messages[job_id].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state.model_name,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages[job_id]
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages[job_id].append({"role": "assistant", "content": response})

