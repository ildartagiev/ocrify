import asyncio
import os
import shutil
import zipfile
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
from typing import List
from uuid import uuid4

import aiofiles
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

from src.core import extract_text_from_pdf, extract_text_from_pdf_to_docx_as_bytes

app = FastAPI(
    title="OCRify",
    description="Ocr-ing pdf documents and returns text.",
    version="1.0.0"
)


def create_upload_directory():
    upload_dir = './tmp/upload/' + str(uuid4())

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    return upload_dir


@app.get("/", status_code=200)
def index() -> str:
    return "ok"


@app.post("/ocr/")
async def extract_text_from_pdf(files: List[UploadFile] = File(...)):
    upload_dir = create_upload_directory()

    tmp_files = []

    async def process_file(file):
        file_path = os.path.join(upload_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        tmp_files.append(file_path)

    await asyncio.gather(*[process_file(file) for file in files])

    result: dict[str, str] = {}

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(extract_text_from_pdf, file_path) for file_path in tmp_files]
        for future, file_path in zip(futures, tmp_files):
            result[os.path.basename(file_path)] = await asyncio.wrap_future(future)

    shutil.rmtree(upload_dir)

    return result


@app.post("/ocr/to-docx")
async def extracted_text_from_pdf_to_docx(files: List[UploadFile] = File(...)):
    upload_dir = create_upload_directory()

    tmp_files = []

    async def process_file(file):
        file_path = os.path.join(upload_dir, file.filename)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        tmp_files.append(file_path)

    await asyncio.gather(*[process_file(file) for file in files])

    documents = {}

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(extract_text_from_pdf_to_docx_as_bytes, file_path) for file_path in tmp_files]
        for future, file_path in zip(futures, tmp_files):
            documents[f'{os.path.splitext(os.path.basename(file_path))[0]}.docx'] = await asyncio.wrap_future(future)

    zip_bytes = BytesIO()
    with zipfile.ZipFile(zip_bytes, 'w') as zip_file:
        for document in documents:
            zip_file.writestr(document, documents[document].getvalue())
    zip_bytes.seek(0)

    shutil.rmtree(upload_dir)

    return StreamingResponse(zip_bytes,
                             media_type='application/zip',
                             headers={"Content-Disposition": "attachment; filename=documents.zip"})


if __name__ == '__main__':
    if not os.path.exists('./tmp/upload'):
        os.makedirs('./tmp/upload')

    import uvicorn

    uvicorn.run("main:app", port=8080, log_level="info")
