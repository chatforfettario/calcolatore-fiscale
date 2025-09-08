from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Ciao da FastAPI su Render!"}
