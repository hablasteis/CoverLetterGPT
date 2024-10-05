import asyncio
import streamlit as st

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, \
    OnSiteOrRemoteFilters, SalaryBaseFilters
from linkedin_jobs_scraper.exceptions import InvalidCookieException

from src.job import LinkedinJob

class Retriever:
    RESULTS_PER_PAGE = 10


class LinkedinRetriever(Retriever):
    # Event listener for LinkedIn jobs data
    
    def __init__(self, jobs):
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