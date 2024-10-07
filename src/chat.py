import streamlit as st
import os

from prompts import dumb_down_prompt
from src.job import Job
from src.letter import CoverLetter
from src.generator import ChatLetterGenerator
from utils.general import split_by_dear


@st.dialog("View PDF")
def view_pdf(index):
    from streamlit_pdf_viewer import pdf_viewer
    file_path = os.path.join(CoverLetter.downloads_folder, cl.get_file_name(index))
    st.markdown(f"Your cover letter is saved at:")
    st.code(f"file:///{file_path}", language="shell")

    with st.spinner("Loading..."):
        pdf_viewer(file_path,)

def is_chat_visible():
    return "display_chat" in st.session_state and st.session_state["display_chat"]

def set_chat_type(chat_type):
    st.session_state["display_chat"] = chat_type

def is_correct_chat(retriever):
    class_name = retriever.__class__.__name__
    return st.session_state["display_chat"] == class_name

def display_chat():

    if "edit_letter" in st.session_state:
        st.query_params["job"] = st.session_state["edit_letter"]
        del st.session_state.edit_letter


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

        # Get index of the cover letter which is saved on disk
        saved_index = cl.saved_in_messages(st.session_state.messages[job_id])

        st.write("Improve your letter with GPT")

        if st.session_state.job_id in st.session_state.messages:

            for index, message in enumerate(st.session_state.messages[job_id]):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

                    if message["role"] == "assistant":
                        col1, _, col2, col3 = st.columns([1, 2, 1, 1])

                        with col1:
                            if index == len(st.session_state.messages[job_id]) - 1:
                                dumber = st.button("Simplify", icon=":material/trending_down:", use_container_width=True , key=f"dumb_{index}")
                                if dumber:
                                    st.session_state.messages[job_id].append({"role": "user", "content": "Simplify the cover letter"})
                                    

                        with col2:
                            if saved_index != index:
                                if st.button("Save", 
                                            icon=":material/save:", 
                                            use_container_width=True , 
                                            key=f"save_{index}"
                                            ):
                                    cl.save(message["content"])
                            else:
                                st.button("Saved", 
                                            icon=":material/check:", 
                                            use_container_width=True , 
                                            key=f"save_{index}",
                                            type="primary"
                                            )

                        
                        with col3:    

                            if not cl.exists_pdf(index):
                                st.button(
                                    "Export", 
                                    icon=":material/picture_as_pdf:", 
                                    use_container_width=True, 
                                    key=f"export_{index}",
                                    on_click=cl.export_to_pdf,
                                    args=(message["content"], index)
                                    )
                            else:
                                if st.button(
                                    "View PDF", 
                                    icon=":material/download_done:", 
                                    use_container_width=True,
                                    key=f"view_{index}",
                                    type="primary"
                                    ):
                                    view_pdf(index)
                
                
            if dumber:

                messsage = st.session_state.messages[job_id][index]["content"]

                dumb_prompt = dumb_down_prompt.format(cover_letter=message)
                dumb_message = {"role": "assistant", "content": dumb_prompt}
                with st.chat_message("assistant"):
                    response = st.write_stream(
                        generator.generate(
                            model_name = st.session_state.model_name, 
                            messages = st.session_state.messages[job_id] + [dumb_message]
                            )
                        )

                st.session_state.messages[job_id].append({"role": "assistant", "content": response})
                st.rerun()

            if prompt := st.chat_input("Hi! What should I change?"):
                st.session_state.messages[job_id].append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    response = st.write_stream(
                        generator.generate(
                            model_name = st.session_state.model_name, 
                            messages = st.session_state.messages[job_id]
                            )
                        )

                st.session_state.messages[job_id].append({"role": "assistant", "content": response})
                st.rerun()