import shutil
import aiofiles
from fastapi import HTTPException
from models import Video, User
from schemas import UploadVideo, GetVideo
from uuid import uuid4
from fastapi import UploadFile, BackgroundTasks


async def save_video(user: User,
                     file: UploadFile,
                     title: str,
                     description: str,
                     background_tasks: BackgroundTasks):
    file_name = f'media/{user.id}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418, detail='Ay yay yay budet')
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())


def write_video(file_name: str, file: UploadFile):
    # async with aiofiles.open(file_name, "wb") as buffer:
    #     data = await file.read()
    #     await buffer.write(data)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
