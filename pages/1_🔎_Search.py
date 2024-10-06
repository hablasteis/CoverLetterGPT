import streamlit as st
import os
import asyncio

from src.generator import LinkedinLetterGenerator
from src.job import LinkedinJob
from src.retriever import LinkedinRetriever
from utils.general import split_by_dear, show_model_selection, init_model_selection, initialize_app


def generate_cover_letter(index):
    import threading
    job = st.session_state.jobs[index]

    generator = LinkedinLetterGenerator(job_id=job.job_id, title=job.title, description=job.description)

    st.session_state.cover_letters[job.job_id] = "generating"

    # Start a new thread for generating the cover letter
    thread = threading.Thread(target=generator.generate, args=[st.session_state.model])
    thread.start()
    job.save_job()
    

def display_job_ad(job, index):
    st.write("")
    with st.container():
        col1, col2 = st.columns([3, 1])

        with col1:
            col3, col4 = st.columns([1, 10])

            with col3:
                st.image(job.company_img_link, width=50)

            with col4:
                st.markdown(f"#### [{job.title}]({job.link})")  

            # Split the company string and format
            company_info = job.company.split(' · ')

            if len(company_info) == 2:
                company_name = company_info[0]
                location_info = company_info[1]
                st.write(f"**[{company_name}]({job.company_link})** · {location_info}")
            else:
                st.write(f"**[{job.company}]({job.company_link})**")  # Fallback in case of unexpected format

        with col2:
            file_name = os.path.join(LinkedinLetterGenerator.get_class_path(), f"{job.job_id}.txt")
            # Check if the file exists

            if os.path.exists(file_name) or (job in old_jobs and job not in st.session_state.jobs):
                st.success("Cover letter available! ✅", icon="✅")
            elif job.job_id in st.session_state.cover_letters:
                generated = st.session_state.cover_letters[job.job_id]

                if generated == "generating":
                    st.write("Processing...")
            else:
                st.button("Generate", key="button" + job.job_id, on_click=generate_cover_letter, args=[index])

            st.write(index+1)

        if os.path.exists(file_name):
            # Tabs for Description, View Cover Letter, and Edit Cover Letter
            tab1, tab2 = st.tabs(["Description", "View Cover Letter"])

            with open(file_name, 'r') as file:

                with tab1:
                    with st.expander("..."):
                        st.write(job.description)
                        st.write("---")
                        if job.insights:  
                            st.write(f"- {job.insights[0]}")  
                        
                with tab2:    
                    cover_letter_content = file.read()
                    # Use the split_by_dear function to split the cover letter content
                    _, cover_letter_main = split_by_dear(cover_letter_content)

                    new_content = st.text_area("Edit Cover Letter", cover_letter_main, height=200, key=job.job_id+"textarea")
                    if st.button("Save Changes", key=job.job_id+"save_button"):
                        with open(file_name, 'w') as file:
                            file.write(new_content)
                        st.success("Cover letter updated!")

        else:
            with st.expander("..."):
                st.write(job.description)
                st.write("---")
                if job.insights:  
                    st.write(f"- {job.insights[0]}")  
        st.markdown("---")

st.set_page_config(page_title="Search", page_icon="🔎", layout="wide")

if "initialized" not in st.session_state:
    initialize_app()

init_model_selection()


old_jobs = []
for path in os.listdir(LinkedinJob.get_jobs_path()):
    test = os.path.join(LinkedinJob.get_jobs_path(), path)
    job = LinkedinJob()
    job.load_job_from_path(test)
    old_jobs.append(job)

# old_jobs = [LinkedinJob().load_job_from_path(os.path.join(LinkedinJob.get_jobs_path(),path)) for path in os.listdir(LinkedinJob.get_jobs_path())]


st.header("Search Jobs")
st.write("")

job_board = st.empty()

# To store retrieved job data
jobs = []

retriever = LinkedinRetriever(jobs)

options = {}

with st.container(border=True):
    col1, col2, _, col3 = st.columns([2, 2, 1, 1], vertical_alignment="bottom")
    with col1:
        options["job_title"] = st.text_input("Job Title", value="Data Scientist", label_visibility="hidden")
    
    with col2:
        options["location"] = st.text_input("Location", value="Sweden")
    # options["limit"] = st.number_input("Show", value=10, step=5)

    with col3:
        search = st.button("Search")
        

    with st.expander("More filters"):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        with col1:
            options["time"] = st.selectbox(
                'Select Time Filter',
                ['Anytime', 'Past 24 hours', 'Past Week', 'Past Month']  
            )

        with col2:
            options["type_filter"] = st.multiselect(
                'Select Job Type',
                ['Full-Time', 'Internship', 'Part-Time', 'Contract']  
            )
        with col3:
            options["on_site_or_remote"] = st.multiselect(
                'Select Work Type',
                ['On-Site', 'Remote', 'Hybrid'],
            )
        with col4:
            options["experience"] = st.multiselect(
                'Select Experience Level',
                ['Internship', 'Entry-Level', 'Mid-Senior'],
                default= ['Internship', 'Entry-Level']
            )
        
        options["relevance"] = st.selectbox(
            'Sorting',
            ['Most Relevant', 'Most Recent']  
        )
    

with st.sidebar:
    show_model_selection()


if search:
    if options["job_title"] == "":
        st.warning("Please enter a job title")
    elif options["location"] == "":
        st.warning("Please enter a location")
    else:

        jobs.clear()  # Clear previous job results

        if "jobs" in st.session_state:
            currently_showing = len(st.session_state.jobs)
        else:
            currently_showing = 0

        with st.spinner('Fetching results, please wait this could take a while...'):
            asyncio.run(retriever.scrape_jobs(currently_showing))

        st.session_state.jobs = jobs


if "jobs" in st.session_state:
    
    st.write(f'Currently showing {len(st.session_state.jobs)} jobs')

    for index, job in enumerate(st.session_state.jobs):
        display_job_ad(job, index)

    
    if st.button("Load more"):
        if "jobs" in st.session_state:
            currently_showing = len(st.session_state.jobs)
        else:
            currently_showing = 0

        with st.spinner('Fetching more results, please wait...'):
            asyncio.run(retriever.scrape_jobs(currently_showing))

        st.session_state.jobs = jobs
        st.rerun() # Need to rerun otherwise it will show the old results
