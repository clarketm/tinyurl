from fastapi import FastAPI

app = FastAPI()


@app.get("/{short_url}")
def read_short_url(short_url: str):
    return {"short_url": short_url}


@app.post("/{short_url}")
def create_short_url(short_url: str):
    return {"short_url": short_url}
