from fastapi import FastAPI, Response, status

app = FastAPI()

@app.get("/health")
def health():
    return Response(status_code=status.HTTP_200_OK)
