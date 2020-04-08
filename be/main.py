from os import getenv
from urllib.parse import urlparse

from base62 import encode
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

URLS = "urls"
SHORT_URL = "short_url"
LONG_URL = "long_url"
COUNT = "count"

load_dotenv()
app = FastAPI()
db = Redis(host=getenv("REDIS_MASTER_SERVICE_HOST", "0.0.0.0"), port=getenv("REDIS_MASTER_SERVICE_PORT", "6379"))

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


class URL(BaseModel):
    long_url: str


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_short_urls():
    urls = db.hgetall(URLS)
    urls_list = [{SHORT_URL: short, LONG_URL: long} for short, long in urls.items()]

    return {URLS: urls_list}


@app.get("/{short_url}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def read_short_url(short_url: str):
    long_url = db.hget(URLS, short_url)

    if not long_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    url = urlparse(long_url.decode("utf-8"), scheme="http")

    return RedirectResponse(url=url.geturl())


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_short_url(url: URL):
    count = db.incrby(COUNT, 1)
    short_url = encode(count)

    db.hset(URLS, short_url, url.long_url)

    return {SHORT_URL: short_url, LONG_URL: url.long_url}
