from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from utils.general import extract_cover_letter
import os
import json



class CoverLetter():
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    def __init__(self, job_id, letter_path):
        self.job_id = job_id
        self.letter_path = letter_path

    def save(self, cover_letter_text):
        cover_letter_text = extract_cover_letter(cover_letter_text)
        with open(self.letter_path, 'w') as file:
            file.write(cover_letter_text)

    def saved_in_messages(self, messages):
        if messages is None:
            return None
        
        with open(self.letter_path, 'r') as file:
            saved = file.read()
            for index, message in enumerate(messages):
                if message["content"] == saved:
                    return index
        
        return None

    def update_letter(self, new_letter, index):
        self.save(new_letter)
        self.export_to_pdf(new_letter, index)

    def exists_pdf(self, index):
        return os.path.exists(os.path.join(CoverLetter.downloads_folder, f"{self.job_id}_{index}.pdf"))

    def get_pdf_file_name(self, index):
        return f"{self.job_id}_{index}.pdf"
    
    def get_letter(self):
        with open(self.letter_path, "r") as file:
            letter = file.read()
        
        return letter.strip()
    
    def export_to_pdf(self, cover_letter_text, index):
        print("test", index)
        print(cover_letter_text)
        cover_letter_text = extract_cover_letter(cover_letter_text)

        file_name = self.get_pdf_file_name(index)

        # Set file path for saving the PDF
        file_path = os.path.join(CoverLetter.downloads_folder, file_name)
        
        doc = SimpleDocTemplate(file_path, pagesize=LETTER, 
                                rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)

        elements = []

        heading_style = ParagraphStyle(
            'Heading',
            fontSize=12,
            leading=14,
            spaceAfter=5,
            textColor=colors.black,
            alignment=0  # Left alignment
        )

        body_style = ParagraphStyle(
            'Body',
            fontSize=11,
            leading=14,
            spaceAfter=5,
            textColor=colors.black,
            alignment=0  # Left alignment
        )

        if os.path.exists("info.json"):
            with open("info.json", 'r') as file:
                info = json.load(file)
            
            applicant_info = [
                info["name"], 
                info["address"], 
                info["email"], 
                info["phone"]
            ]
            
            for info in applicant_info:
                paragraph = Paragraph(info, style=heading_style)
                elements.append(paragraph)

            # Add a spacer between the contact info and the cover letter body
            elements.append(Spacer(1, 12))
        

        for line in cover_letter_text.split("\n"):
            paragraph = Paragraph(line.strip() + "\n", style=body_style)
            elements.append(paragraph)

        # Build the PDF with the content
        doc.build(elements)

        return file_path 
