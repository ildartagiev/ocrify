import os
from io import BytesIO
from typing import Any

import pytesseract
from docx import Document
from dotenv import load_dotenv
from nipype.interfaces.base import ImageFile

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD')


def extract_text_with_tesseract(image: ImageFile,
                                lang: Any = 'rus',
                                config: str = '',
                                nice: int = 0,
                                output_type: str = pytesseract.Output.STRING,
                                timeout: int = 0) -> Any:
    """Извлекает текст с помощью Tesseract."""
    # Используем pytesseract для извлечения текста
    result = pytesseract.image_to_string(image,
                                         lang=lang,
                                         config=config,
                                         nice=nice,
                                         output_type=output_type,
                                         timeout=timeout)
    return result


def extract_text_from_pdf(file_path):
    from src.extractors.pdf.pdf_extractor import PdfExtractor
    extractor = PdfExtractor()
    images = extractor.extract(file_path)

    text: str = ""

    for filename, image in images:
        extracted_text = extract_text_with_tesseract(image)
        text += extracted_text + os.linesep

    return text


def create_docx_document(text: str) -> Document:
    """Создает Word документ с заданным текстом."""
    # Создаем новый документ
    doc = Document()
    # Добавляем текст в документ
    doc.add_paragraph(text)
    return doc


def extract_text_from_pdf_to_docx_as_bytes(file_path):
    extracted_text = extract_text_from_pdf(file_path)
    doc = create_docx_document(extracted_text)
    docx_bytes = BytesIO()
    doc.save(docx_bytes)
    docx_bytes.seek(0)
    return docx_bytes
