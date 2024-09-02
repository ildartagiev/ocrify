import os
from typing import Any

import pytesseract
from dotenv import load_dotenv
from nipype.interfaces.base import ImageFile

from src.extractors.pdf.pdf_extractor import PdfExtractor

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


def process_document(file_path):
    extractor = PdfExtractor()
    images = extractor.extract(file_path)

    text: str = ""

    for filename, image in images:
        extracted_text = extract_text_with_tesseract(image)
        text += extracted_text + os.linesep

    return text
