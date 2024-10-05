from openai import OpenAI
from prompts import cover_letter_prompt, cover_letter_system_prompt, dumb_down_prompt
import os
from src.job import LinkedinJob, CustomJob

class LetterGenerator():
    client = OpenAI()
    cv = None
    base_path = "generated_letters"
    
    # TODO: Substitute job_id with the path where to save the cover letter  
    def __init__(self, job_id, title, description):
        self.job_id = job_id
        self.title = title
        self.description = description

        if os.path.exists("cv.txt"):
            with open("cv.txt", "r") as file:
                existing_cv = file.read()
                LetterGenerator.cv = existing_cv
         
    def build_prompt(self):
        return cover_letter_prompt.format(job_title=self.title, job_ad=self.description, cv=LetterGenerator.cv)

    def generate(self, model_name):
        prompt = self.build_prompt()

        # Send the API request
        completion = LetterGenerator.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": cover_letter_system_prompt},
                {
                    "role": "user",
                    "content": prompt
                }
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
    def __init__(self, job_id):
        self.job_id = job_id

        if os.path.exists("cv.txt"):
            with open("cv.txt", "r") as file:
                existing_cv = file.read()
                LetterGenerator.cv = existing_cv

    def dumb_down(self, model_name, letter):
        prompt = dumb_down_prompt.format(cover_letter = letter)
        messages = [{"role": "system", "content": prompt}]

        return self.generate(model_name, messages)

    def generate(self, model_name, messages):
        stream = LetterGenerator.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ],
            stream=True,
        )

        return stream
