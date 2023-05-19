import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form
from models import Video, User
from schemas import UploadVideo, GetVideo, User

video_router = APIRouter()


@video_router.get("/")
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_name": file.filename, "info": info}


@video_router.post("/image")
async def upload_image(file: List[UploadFile] = File(...)):
    for img in file:
        with open(f'{img.filename}', 'wb') as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": "GOOD"}


@video_router.post("/video")
async def create_video(video: Video):
    await video.save()
    return video


@video_router.get("/video/{video_pk}", response_model=Video)
async def get_video(video_pk: int):
    return await Video.objects.select_related('user').get(pk=video_pk)
