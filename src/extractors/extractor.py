from abc import ABC, abstractmethod
from typing import List, Tuple

from PIL.ImageFile import ImageFile


class Extractor(ABC):
    @abstractmethod
    def extract(self, file) -> List[Tuple[str, ImageFile]]:
        """Извлекает изображения и возвращает их в виде списка кортежей (имя файла, изображение)."""
        pass
