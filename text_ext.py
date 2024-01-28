import PyPDF2 as pdf
from PyPDF2 import PdfReader, PdfWriter



### Function to Extract Text From PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path,"rb") as f:
        reader = PdfReader(f)
        results = []
        for i in range(0,len(reader.pages)): # prev read.getNumPages()
            selected_page = reader.pages[i]
            text = selected_page.extract_text()
            results.append(text)
        return ' '.join(results) # convert list to a single doc
    
#print(extract_text_from_pdf(pdf_path))

