from os import getenv

from base62 import encode
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from redis import Redis
from starlette.responses import RedirectResponse

load_dotenv()
app = FastAPI()
db = Redis(host=getenv("REDIS_MASTER_SERVICE_HOST"), port=getenv("REDIS_MASTER_SERVICE_PORT"))


class URL(BaseModel):
    long_url: str


@app.get("/")
def read_all_short_urls():
    long_urls = db.hgetall("urls")
    return {"long_urls": long_urls}


@app.get("/{short_url}")
def read_short_url(short_url: str):
    long_url = db.hget("urls", short_url).decode("utf-8")
    return RedirectResponse(url=long_url)


@app.post("/")
def create_short_url(url: URL):
    count = db.incr("count", 0)
    short_url = encode(count)
    db.hset("urls", short_url, url.long_url)
    return {"short_url": short_url, "long_url": url.long_url}
