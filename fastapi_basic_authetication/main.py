from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import engine

from apps.user import models as user_models
from apps.user.routes import router as user_routes

from apps.post import models as post_models


user_models.Base.metadata.create_all(bind=engine)
post_models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    'http://localhost:5500',
    'http://127.0.0.1:5500',
]

# origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def main():
    return {'message': 'main route'}


app.include_router(user_routes)
