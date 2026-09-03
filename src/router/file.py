from fastapi import APIRouter
from sqlalchemy import select, desc, or_, UUID
from pydantic import UUID4, EmailStr
from fastapi import Depends, UploadFile
from fastapi.responses import FileResponse, StrimingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters


router = APIRouter()


@router.post("/upload-file")
async def upload_file(upload_files: list[UploadFile]):
    if len(upload_files) < 1:
        return "Передайте файл"
    for a in upload_files:
        file = a.file
        filename = a.filename
        with open(f"files/{filename}", "wb") as f:
            f.write(file.read())
    return "Файлы загружен"

@router.get("/file/{filename}")
async def get_file(filename: str):
    return FileResponse(f"files/{filename}")

def iterate_file(filename: str ):
    with open(f"files/{filename}", "rb") as f:
        while file_chunk:= f.read(1024*1024):
            yield file_chunk

@router.get("/file-striming/{filename}")
async def get_file_striming(filename: str):
    return StrimingResponse(
        iterate_file(filename),
        media_type=get_filename_media_file(filename)
    )

def get_filename_media_file(filename: str) -> str:
    file_extension = filename.split(".")[-1]
    if file_extension == ".txt":
        return "text/txt"