import streamlit as st
from openai import OpenAI

from src.job import CustomJob, Job
from src.letter import CoverLetter
from src.generator import ChatLetterGenerator
from utils.general import show_model_selection, init_model_selection, initialize_app, split_by_dear

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

if "edit_letter" in st.session_state:
    st.query_params["job"] = st.session_state["edit_letter"]
    del st.session_state.edit_letter
    
if "initialized" not in st.session_state:
    initialize_app()

with st.sidebar:
    init_model_selection()
    show_model_selection()

client = OpenAI()


st.header("Chat with a cover letter")


if "job" not in st.query_params and "job_id" not in st.session_state:
    st.subheader("Ops... There is nothing here!")
    st.write("Please select a cover letter to chat with")

if "job" in st.query_params:
    # Might be LinkedinJob
    job_id = st.query_params["job"]

    job = Job.load(job_id)

    st.session_state.job_id = job_id

    letter = job.get_letter_path()
    with open(letter, "r") as file:
        letter = file.read()
        _, letter = split_by_dear(letter)

    st.session_state.messages[job_id] = [{"role": "assistant", "content": letter}]
    del st.query_params.job

if "job_id" in st.session_state:
    job_id = st.session_state["job_id"]
    job = Job.load(job_id)


    generator = ChatLetterGenerator(job_id)
    cl = CoverLetter(job.job_id, job.get_letter_path())

    st.write("Improve your letter with GPT")

    if st.session_state.job_id in st.session_state.messages:
        
        for index, message in enumerate(st.session_state.messages[job_id]):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

                if message["role"] == "assistant":
                    col1, _, col2, col3 = st.columns([1, 1, 1, 1])
                    if col1.button("De-formalize", icon=":material/trending_down:", use_container_width=True , key=f"dumb_{index}"):
                        # generator.dumb_down()
                        None                        

                    if col2.button("Save", icon=":material/save:", use_container_width=True , key=f"save_{index}"):
                        cl.save(message["content"])
                    with col3:    

                        if not cl.exists_pdf(index):
                            if st.button("Export", icon=":material/picture_as_pdf:", use_container_width=True, key=f"export_{index}"):
                                cl.export_to_pdf(message["content"], index)
                        else:
                            st.button("✅", icon=":material/picture_as_pdf:", use_container_width=True, key=f"export_{index}")


        if prompt := st.chat_input("Hi! What should I change?"):
            st.session_state.messages[job_id].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # stream = client.chat.completions.create(
                #     model=st.session_state.model_name,
                #     messages=[
                #         {"role": m["role"], "content": m["content"]}
                #         for m in st.session_state.messages[job_id]
                #     ],
                #     stream=True,
                # )
                # response = st.write_stream(stream)
                response = st.write_stream(
                    generator.generate(
                        model_name = st.session_state.model_name, 
                        messages = st.session_state.messages[job_id]
                        )
                    )
            st.session_state.messages[job_id].append({"role": "assistant", "content": response})
            st.rerun()
