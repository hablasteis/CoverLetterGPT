import streamlit as st
import os
from src.generator import LinkedinLetterGenerator, CustomLetterGenerator
from src.job import LinkedinJob, CustomJob
from utils.general import split_by_dear

def display_cover_letter_comparison(job):
    """
    Displays the job description and cover letter side by side inside an expander for easy comparison.
    """
    with st.container():
        col1, col2, col3 = st.columns([1, 10, 2])

        with col1:
            if job.company_img_link:
                st.image(job.company_img_link, width=50)  # Company Icon

        with col2:
            st.markdown(f"### {job.title}")
            company_info = job.company.split(' · ')

            if len(company_info) == 2:
                company_name = company_info[0]
                location_info = company_info[1]
                st.write(f"**[{company_name}]({job.company_link})** · {location_info}")
            else:
                st.write(f"**[{job.company}]({job.company_link})**")

        with col3:
            if st.button("Open chat", key=job.job_id):
                st.session_state["edit_letter"]=job.job_id
                st.switch_page("src/chat.py")


        # Expander to compare job description and cover letter
        with st.expander("Compare Job Description and Cover Letter"):
            desc_col, cover_letter_col = st.columns([1, 1])

            with desc_col:
                # Display job description
                st.write("#### Job Description")
                st.markdown(job.description)
                if job.insights:
                    st.write(f"- {job.insights[0]}")

            with cover_letter_col:
                # Load and display the cover letter if it exists
                file_name = job.get_letter_path()

                if os.path.exists(file_name):
                    with open(file_name, 'r') as file:
                        cover_letter_content = file.read()

                    # Use the split_by_dear function to split the cover letter content
                    pre_dear_part, cover_letter_main = split_by_dear(cover_letter_content)


                    # Display the cover letter with 'Dear' and the main content editable
                    st.write("#### Cover Letter")
                    new_content = st.text_area(
                        "Edit Cover Letter", 
                        cover_letter_main,  # Only allow editing actual letter
                        height=800, 
                        key=job.job_id + "textarea_tab2"
                    )

                    # Save changes if the button is clicked
                    if st.button("Save Changes", key=job.job_id + "save_button_tab2"):
                        with open(file_name, 'w') as file:
                            # Combine the pre 'Dear' part and the edited content
                            file.write(pre_dear_part + new_content)
                        st.success("Cover letter updated!")

                    # Display the part before the 'Dear' line as info
                    if pre_dear_part.strip():
                        st.info(pre_dear_part.strip())

                else:
                    st.warning("No cover letter available.")


def display_cover_letters():

    exist_other_letters = False

    custom_jobs = [file for file in os.listdir(os.path.join(CustomLetterGenerator.get_class_path()))]

    if custom_jobs:
        st.subheader("")
        st.write("Custom Jobs")

        for file in custom_jobs:
            if file.endswith('.txt'):
                job_id = os.path.splitext(os.path.basename(file))[0]
                
                if CustomJob.exists(job_id):
                    job_path = os.path.join(CustomJob.get_jobs_path(), f"{job_id}.json")
                    job = CustomJob()
                    job.load_job_from_path(job_path) 
                    
                else:
                    job = CustomJob(
                        job_id = job_id, 
                        title = "Custom Job", 
                        company = "Custom Company", 
                        company_link = None, 
                        company_img_link = None, 
                        date = None, 
                        link = None, 
                        insights = None, 
                        description = None
                    )
                st.write("")
                display_cover_letter_comparison(job)
                st.write("---")
                exist_other_letters = True

    if "jobs" in st.session_state:
        st.write("From current session.")

        for index, job in enumerate(st.session_state.jobs):
            file_name = os.path.join(LinkedinLetterGenerator.get_class_path(), f"{job.job_id}.txt")
            if os.path.exists(file_name):
                st.write("")
                display_cover_letter_comparison(job)
                st.write("---")

                exist_other_letters = True

    current_session_files = [f"{job.job_id}" for job in st.session_state.jobs] if "jobs" in st.session_state else []
    old_letters = [os.path.splitext(file)[0] for file in os.listdir(LinkedinLetterGenerator.get_class_path()) if os.path.splitext(file)[0] not in current_session_files]

    if old_letters:
        st.write("LinkedIn jobs")
        for job_id in old_letters:
            job_path = os.path.join(LinkedinJob.get_jobs_path(), f"{job_id}.json")
            job = LinkedinJob()
            job.load_job_from_path(job_path)
            
            display_cover_letter_comparison(job)
            st.write("---")

            exist_other_letters = True


    if not exist_other_letters:
        st.write("There are no cover letters here!")