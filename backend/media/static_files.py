# static_files.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def mount_static_files(app: FastAPI):
    app.mount("/media/images", StaticFiles(directory="media/images"), name="images")
    # app.mount("/media/icons", StaticFiles(directory="media/icons"), name="icons")
    # app.mount("/media/videos", StaticFiles(directory="media/videos"), name="videos")
