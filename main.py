from fastapi import FastAPI, Response, status

from database import engine
from models import Base

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return Response(status_code=status.HTTP_200_OK)
