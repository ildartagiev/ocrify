import asyncio
import os
from concurrent.futures import ProcessPoolExecutor
from typing import List

import aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile

from src.core import process_document

app = FastAPI(
    title="OCRify",
    description="Ocr-ing pdf documents and returns text.",
    version="1.0.0"
)


@app.get("/", status_code=200)
def index() -> str:
    return "ok"


@app.post("/ocr/")
async def extract_text_from_pdf(files: List[UploadFile] = File(...)):
    result: dict[str, str] = {}

    temp_files = []

    async def process_file(file):
        file_path = os.path.join(f"./tmp/upload/{file.filename}")
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        temp_files.append(file_path)

    await asyncio.gather(*[process_file(file) for file in files])

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_document, file) for file in temp_files]
        for future, file in zip(futures, temp_files):
            result[os.path.basename(file)] = await asyncio.wrap_future(future)

    for temp_file in temp_files:
        os.remove(temp_file)

    return result


if __name__ == '__main__':
    if not os.path.exists("./tmp/upload"):
        os.makedirs("./tmp/upload")

    # uvicorn.run("main:app", port=8080, log_level="info")