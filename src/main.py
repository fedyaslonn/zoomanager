from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv

import os

import sys

from src.core.routers.animals import animal_router

load_dotenv()

app = FastAPI()

pythonpath = os.getenv('PYTHONPATH')


if pythonpath:
    sys.path.append(pythonpath)

from src.core.routers.users import user_router

app.include_router(user_router)
app.include_router(animal_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)