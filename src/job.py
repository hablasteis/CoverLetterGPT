import json
import os
from abc import ABC

#### How is job_id determined?
# hash(job_description)

class Job(ABC):
    letters_path = "generated_letters"
    base_path = "jobs"
    
    def __init__(self, job_id=None, title=None, company=None, company_link=None, company_img_link=None, date=None, link=None, insights=None, description=None):
        self.job_id = str(job_id)
        self.title = title
        self.company = company
        self.company_link = company_link
        self.company_img_link = company_img_link
        self.date = date
        self.link = link
        self.insights = insights
        self.description = description

    def save_job(self):
        file_name = f"{self.job_id}.json"
        path = os.path.join(self.get_jobs_path(), file_name)
        
        with open(path, 'w') as file:
            json.dump(self.__dict__, file)  # Save object as a JSON

    def get_letter_path(self):
        cls = self.__class__ 
        path = cls.get_letters_path()
        path = os.path.join(path, f"{self.get_file_name()}.txt")
        return path
    
    def get_job_path(self):
        cls = self.__class__ 
        path = cls.get_jobs_path()
        path = os.path.join(path, f"{self.get_file_name()}.json")
        return path

    def load_job_from_path(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
            # job = self.__class__(**data)  
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
        
    @staticmethod
    def load(job_id):
        job_class = find_job_class(job_id)
        if job_class is None:
            return None

        job = job_class()
        job.job_id = job_id

        path = job_class.get_jobs_path()
        path = os.path.join(path, f"{job.get_file_name()}.json")
        try:
            with open(path, 'r') as file:
                data = json.load(file)
                job = job_class(**data)  
                return job
        except:
            return job

    @classmethod
    def exists(self, job_id):
        return os.path.exists(os.path.join(self.get_jobs_path(), f"{job_id}.json"))

    @classmethod
    def initialize(cls):
        if not os.path.exists(cls.get_jobs_path()):
            os.makedirs(cls.get_jobs_path())

    @classmethod
    def get_jobs_path(cls):
        return os.path.join(cls.base_path, cls.class_name)
    
    @classmethod
    def get_letters_path(cls):
        return os.path.join(cls.letters_path, cls.class_name)
    
    def __eq__(self, other):
        return (self.title == other.title and
                self.company == other.company and
                self.date == other.date and
                self.description == other.description)

class LinkedinJob(Job):
    class_name = "LinkedIn"

    def get_file_name(self):
        return self.job_id

class CustomJob(Job):
    class_name = "custom"

    def get_file_name(self):
        return self.job_id

# Retrieve the Class of the job_id by checking in the saved files 
# (letters, since job files might not exist for some letters)
def find_job_class(job_id):
    import inspect
    import src.job as job
    
    job_classes = []
    # Dynamically retrieve all classes in the module
    for name, obj in inspect.getmembers(job):
        if inspect.isclass(obj):  
            if hasattr(obj, 'class_name'):  # Ensure the class is not Job
                job_classes.append(obj)
    
    for job_class in job_classes:
        temp_job = job_class()
        temp_job.job_id = job_id
        # Need to check among letters because job file might not exist
        for file_name in os.listdir(job_class.get_letters_path()):
            if os.path.splitext(file_name)[0] == str(temp_job.get_file_name()):
                return job_class  
    
    return None  # Return None if no match is found
