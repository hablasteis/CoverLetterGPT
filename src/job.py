import json
import os
from abc import ABC

class Job(ABC):
    base_path = "jobs"
    def __init__(self, job_id, title, company, company_link, company_img_link, date, link, insights, description):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.company_link = company_link
        self.company_img_link = company_img_link
        self.date = date
        self.link = link
        self.insights = insights
        self.description = description

    def save_job(self):
        file_name = f"{hash(self.job_id)}.json"
        path = os.path.join(self.get_class_path(), file_name)
        
        with open(path, 'w') as file:
            json.dump(self.__dict__, file)  # Save object as a JSON

    @staticmethod
    def load_job(path):
        with open(path, 'r') as file:
            data = json.load(file)
            job = Job(**data)  
            return job
    @classmethod
    def exists(self, job_id):
        return os.path.exists(os.path.join(self.get_class_path(), f"{job_id}.pkl"))

    @classmethod
    def initialize(cls):
        if not os.path.exists(cls.get_class_path()):
            os.makedirs(cls.get_class_path())

    @classmethod
    def get_class_path(cls):
        return os.path.join(cls.base_path, cls.class_name)
    
    def __eq__(self, other):
        return (self.title == other.title and
                self.company == other.company and
                self.date == other.date and
                self.description == other.description)

class LinkedinJob(Job):
    class_name = "LinkedIn"

    def __init__(self, job_id, title, company, company_link, company_img_link, date, link, insights, description):
        super().__init__(job_id, title, company, company_link, company_img_link, date, link, insights, description)


class CustomJob(Job):
    class_name = "custom"