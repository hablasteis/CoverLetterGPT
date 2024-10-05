from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os



class CoverLetter():
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    def __init__(self, job_id, letter_path):
        self.job_id = job_id
        self.letter_path = letter_path

    def save(self, cover_letter_text):
        with open(self.letter_path, 'w') as file:
            file.write(cover_letter_text)

    def exists_pdf(self, index):
        return os.path.exists(os.path.join(CoverLetter.downloads_folder, f"{self.job_id}_{index}.pdf"))

    def export_to_pdf(self, cover_letter_text, index):
        file_name = f"{self.job_id}_{index}.pdf"

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

        applicant_info = [
            'John Doe', 
            '1234 Elm St, City, ST 56789', 
            'john.doe@example.com', 
            '(123) 456-7890'
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