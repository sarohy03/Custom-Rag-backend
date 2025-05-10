from fastapi import FastAPI
from api.upload import router as upload
app = FastAPI()

app.include_router(upload)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
