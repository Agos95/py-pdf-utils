from io import BytesIO

import pdfplumber


class PDFInfo:
    pdf: pdfplumber.PDF
    last_page: int
    current_page: int

    def __init__(self, pdf: BytesIO):
        self.pdf = pdfplumber.open(pdf)
        self.last_page = len(self.pdf.pages)
        self.current_page = 0

    def prev_page(self):
        self.current_page = max(0, self.current_page - 1)

    def next_page(self):
        self.current_page = min(self.last_page, self.current_page + 1)
