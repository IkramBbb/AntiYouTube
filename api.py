import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File

# from schemas import UploadVideo

video_router = APIRouter()


@video_router.post("/")
async def root(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_name": file.filename}


@video_router.post("/image")
async def upload_image(file: List[UploadFile] = File(...)):
    for img in file:
        with open(f'{img.filename}', 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": "GOOD"}
