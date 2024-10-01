from openai import OpenAI
from prompts import cover_letter_prompt
import os
from src.job import LinkedinJob, CustomJob

class LetterGenerator():
    client = OpenAI()
    cv = None
    base_path = "generated_letters"
    
    def __init__(self, job_id, title, description):
        self.job_id = job_id
        self.title = title
        self.description = description
         
    def build_prompt(self):
        return cover_letter_prompt.format(job_title=self.title, job_ad=self.description, cv=LetterGenerator.cv)

    def generate(self, model_name):
        prompt = self.build_prompt()

        # Send the API request
        completion = LetterGenerator.client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
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
        file_name = os.path.join(self.get_class_path(), f"{hash(self.job_id)}.txt")
        
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
