from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/")
def get_map():
    file_path = os.path.join(os.path.dirname(__file__), "../static/index.html")
    return FileResponse(file_path)
