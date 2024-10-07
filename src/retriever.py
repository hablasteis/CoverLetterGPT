import asyncio
import os
import streamlit as st

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters, SalaryBaseFilters
from linkedin_jobs_scraper.exceptions import InvalidCookieException

from src.generator import LinkedinLetterGenerator , CustomLetterGenerator
from src.job import LinkedinJob, CustomJob
from src.chat import is_chat_visible, set_chat_type
from utils.general import split_by_dear

class Retriever:
    RESULTS_PER_PAGE = 10

def generate_cover_letter(index):
    import threading
    job = st.session_state.jobs[index]

    generator = LinkedinLetterGenerator(job_id=job.job_id, title=job.title, description=job.description)

    st.session_state.cover_letters[job.job_id] = "generating"

    # Start a new thread for generating the cover letter
    thread = threading.Thread(target=generator.generate, args=[st.session_state.model])
    thread.start()
    job.save_job()




class LinkedinRetriever(Retriever):
    # Event listener for LinkedIn jobs data
    
    def __init__(self, jobs = []):
        self.jobs = jobs

        # Initialize LinkedIn scraper
        self.scraper = LinkedinScraper(
            chrome_executable_path=None,
            chrome_binary_location=None,
            chrome_options=None,
            headless=True,
            max_workers=1,
            slow_mo=0.5,
            page_load_timeout=40
        )

        # Add event listener for job data
        self.scraper.on(Events.DATA, lambda data: self.on_data(data))

    def on_data(self, data: EventData):
        job_id = hash(data.description)

        if not job_id in [job.job_id for job in self.jobs]:
            job = LinkedinJob(
                job_id = job_id,
                title = data.title, 
                company = data.company, 
                company_link = data.company_link, 
                company_img_link = data.company_img_link, 
                date = data.date, 
                link = data.link, 
                insights = data.insights, 
                description = data.description
                # linkedin_id = data.job_id # basically useless
            )
        
            self.jobs.append(job)
        # Update job data in Streamlit

    
    async def gather_scrapes(self, currently_showing):
        queries = [
            Query(
                query='Data Scientist',
                options=QueryOptions(
                    locations=['Sweden'],
                    apply_link=True,  # Try to extract apply link (easy applies are skipped). If set to True, scraping is slower because an additional page must be navigated. Default self, to False.
                    skip_promoted_jobs=False,  # Skip promoted jobs. Default self, to False.
                    limit=currently_showing + self.RESULTS_PER_PAGE,
                    page_offset=0,
                    filters=QueryFilters(
                        relevance=RelevanceFilters.RELEVANT,
                        time=TimeFilters.WEEK,
                        type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                    )
                )
            ),
        ]
            
        await asyncio.to_thread(self.scraper.run, queries)

    # To run async function in the background
    async def scrape_jobs(self, currently_showing):  
        # TODO: When the cookie is not valid, this might continue indefinetly, please fix   
        try:
            await asyncio.gather(self.gather_scrapes(currently_showing))
        except InvalidCookieException:
            st.warning("Your LinkedIn cookie is expired or invalid, please update your cookie! (Check the guide on GitHub)")

    def display_job_ad(self, job, index):
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

                if os.path.exists(file_name) or (job in self.old_jobs and job not in st.session_state.jobs):
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

    def display_search_bar(self):
        self.old_jobs = []
        for path in os.listdir(LinkedinJob.get_jobs_path()):
            test = os.path.join(LinkedinJob.get_jobs_path(), path)
            job = LinkedinJob()
            job.load_job_from_path(test)
            self.old_jobs.append(job)

        self.options = {}
        self.jobs = []

        col1, col2, _, col3 = st.columns([2, 2, 1, 1], vertical_alignment="bottom")
        with col1:
            self.options["job_title"] = st.text_input("Job Title", placeholder="Data Scientist")
        
        with col2:
            self.options["location"] = st.text_input("Location", placeholder="Sweden")
        # self.options["limit"] = st.number_input("Show", value=10, step=5)

        with col3:
            search = st.button("Search")
            

        with st.expander("More filters"):
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

            with col1:
                self.options["time"] = st.selectbox(
                    'Select Time Filter',
                    ['Anytime', 'Past 24 hours', 'Past Week', 'Past Month']  
                )

            with col2:
                self.options["type_filter"] = st.multiselect(
                    'Select Job Type',
                    ['Full-Time', 'Internship', 'Part-Time', 'Contract']  
                )
            with col3:
                self.options["on_site_or_remote"] = st.multiselect(
                    'Select Work Type',
                    ['On-Site', 'Remote', 'Hybrid'],
                )
            with col4:
                self.options["experience"] = st.multiselect(
                    'Select Experience Level',
                    ['Internship', 'Entry-Level', 'Mid-Senior'],
                    default= ['Internship', 'Entry-Level']
                )
            
            self.options["relevance"] = st.selectbox(
                'Sorting',
                ['Most Relevant', 'Most Recent']  
            )


        if search:
            if self.options["job_title"] == "":
                st.warning("Please enter a job title")
            elif self.options["location"] == "":
                st.warning("Please enter a location")
            else:

                self.jobs.clear()  # Clear previous job results

                if "jobs" in st.session_state:
                    currently_showing = len(st.session_state.jobs)
                else:
                    currently_showing = 0

                with st.spinner('Fetching results, please wait this could take a while...'):
                    asyncio.run(self.scrape_jobs(currently_showing))

                st.session_state.jobs = self.jobs



        if "jobs" in st.session_state:
            st.write(f'Currently showing {len(st.session_state.jobs)} jobs')

            for index, job in enumerate(st.session_state.jobs):
                self.display_job_ad(job, index)

            
            if st.button("Load more"):
                if "jobs" in st.session_state:
                    currently_showing = len(st.session_state.jobs)
                else:
                    currently_showing = 0

                with st.spinner('Fetching more results, please wait...'):
                    asyncio.run(self.scrape_jobs(currently_showing))

                st.session_state.jobs = self.jobs
                st.rerun() # Need to rerun otherwise it will show the old results


class CustomRetriever():
    def display_search_bar(self):

        col1, col2, _, col3 = st.columns([2, 2, 1, 1], vertical_alignment="bottom")
        with col1:
            role = st.text_input("Role", placeholder="e.g. Data Scientist")
        
        with col2:
            company = st.text_input("Company", placeholder="e.g. Microsoft")

        with col3:
            generate_button = st.button("Generate", type = "primary")

        height = 250
        if is_chat_visible():
            height = 100
        job_description = st.text_area("Job ad", placeholder="Paste the job description here", height=height)


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

            st.session_state["edit_letter"] = job_id
            set_chat_type(self.__class__.__name__)

        