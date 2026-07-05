from fastapi import FastAPI, Response, status

import models
from database import engine, Base

app = FastAPI()

@app.on_event("startup")
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return Response(status_code=status.HTTP_200_OK)
