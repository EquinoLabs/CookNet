from fastapi import FastAPI
from api.router import api_router
from media.static_files import mount_static_files
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:5173", # frontend
    "http://localhost:3000", # frontend
]

FRONTEND_URL = os.getenv("FRONTEND_URL")
if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to CookNet"}

app.include_router(api_router, prefix="/api")
mount_static_files(app)

if __name__ == "__main__":
    port = int(os.getenv("URL_PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
