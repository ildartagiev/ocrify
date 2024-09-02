### Запуск в docker

build проекта
```
docker build -t ocrify:latest .
```

Запуск проекта
```
docker run --rm -p 8080:8080 -e TESSERACT_CMD='/usr/bin/tesseract' --name ocrify ocrify:latest
```

API

```
http://localhost:8080/ocr
```

Принимает список файлов (сейчас работает только с pdf) \
И возвращает ответ в видео словаря, где ключ - это имя файла, а значение - извлеченный текст

### Запуска локально

Потребуется [Скачать](https://github.com/UB-Mannheim/tesseract/wiki) установить tesseract \
Прямая [ссылка](https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe) на файл

При установке, нужно будет выбрать русский и английский языки в tessdata

TODO