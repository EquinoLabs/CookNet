from fastapi import FastAPI
# from apis.router import api_router
# from media.static_files import mount_static_files
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000", # frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Recipe App"}
# app.include_router(api_router, prefix="/api")
# mount_static_files(app)