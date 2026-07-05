from fastapi import FastAPI, Response, status

import models
from database import Base, engine


app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return Response(status_code=status.HTTP_200_OK)
