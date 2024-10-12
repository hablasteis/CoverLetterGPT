from openai import OpenAI
from prompts import cover_letter_prompt, cover_letter_system_prompt, dumb_down_prompt
import os
from src.job import LinkedinJob, CustomJob

class LetterGenerator():
    client = OpenAI()
    cv = None
    base_path = "generated_letters"

    objective = """
    You are tasked with the following:
    1. Make a list of all key elements from the JOB AD i.e. what the company wants in the candidate
    2. Match these needs with my experiences and qualities in the CONTEXT. These can be vague matches too, but its critical to get as many quaities covered (however it's also critical to not lie in a way that they will find out)
    3. Write a cover letter tailored to the matches 
    """
    
    # TODO: Substitute job_id with the path where to save the cover letter  
    def __init__(self, job_id, title, description):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.system_prompt = self.build_prompt()


        if os.path.exists("cv.txt"):
            with open("cv.txt", "r") as file:
                existing_cv = file.read()
                LetterGenerator.cv = existing_cv
         
    def build_prompt(self):
        return cover_letter_prompt.format(job_title=self.title, job_ad=self.description, objective = self.objective, cv=LetterGenerator.cv)

    def generate(self, model_name):
        # Send the API request
        completion = LetterGenerator.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": cover_letter_system_prompt},
                {"role": "system", "content": self.system_prompt}
            ],
            max_tokens=None,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the response text
        letter = completion.choices[0].message.content
    
        # Save the generated letter to a text file
        file_name = os.path.join(self.get_class_path(), f"{self.job_id}.txt")
        
        with open(file_name, 'w') as file:
            file.write(letter)

    @classmethod
    def get_class_path(cls):
        return os.path.join(cls.base_path, cls.class_name)
    
    @classmethod
    def initialize(cls):
        if not os.path.exists(cls.get_class_path()):
            os.makedirs(cls.get_class_path())

class LinkedinLetterGenerator(LetterGenerator):
    class_name = LinkedinJob.class_name
   

class CustomLetterGenerator(LetterGenerator):
    class_name = CustomJob.class_name

class ChatLetterGenerator(LetterGenerator):
    objective = """
    You are tasked with the following

    1. Gather essential information from the user, including details from their CV, the job advertisement, and any previous cover letter drafts.
    2. Identify Key Elements: pinpoint the specific skills and experiences they possess that align with the job requirements.
    3. Based on the gathered information, work collaboratively with the user to revise or craft a more compelling cover letter that authentically represents their qualifications and will convince an employer.
    """

    chat_response_prompt = "Write only the cover letter content and always start with 'Dear' and end with 'Sincerely,'."

    def dumb_down(self, model_name, letter):
        prompt = dumb_down_prompt.format(cover_letter = letter)
        messages = [{"role": "system", "content": prompt}]

        return self.generate(model_name, messages)

    def generate(self, model_name, messages):
        print("LOG OF PROMPT")
        print([{"role": "system", "content": f"{self.system_prompt} \n {self.chat_response_prompt}"}] + [
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ])
        print("-------------------")
        
        stream = LetterGenerator.client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": f"{self.system_prompt} \n {self.chat_response_prompt}"}] + [
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ],
            stream=True,
        )

        return stream
