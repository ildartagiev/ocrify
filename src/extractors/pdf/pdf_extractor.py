import io
from typing import List, Tuple

import fitz
from PIL import Image
from PIL.ImageFile import ImageFile

from src.extractors.extractor import Extractor


class PdfExtractor(Extractor):
    def __init__(self):
        pass

    def extract(self, file_path) -> List[Tuple[str, ImageFile]]:
        """Извлекает изображения из PDF-документа."""
        images = []
        pdf_document = fitz.open(file_path)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # Извлекаем изображения
            image_list = page.get_images(full=True)

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"page_{page_number + 1}_img_{img_index + 1}.{image_ext}"

                # Создаем изображение из байтов
                image = Image.open(io.BytesIO(image_bytes))

                # Поворачиваем изображение в зависимости от матрицы трансформации
                image = image.rotate(-page.rotation, expand=True)

                # Добавляем кортеж (имя файла, изображение) в список
                images.append((image_filename, image))

        pdf_document.close()
        return images
