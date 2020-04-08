from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from .api.constants import URLS, SHORT_URL, LONG_URL
from .api.models import URL
from .api.utils import format_short_url, canonicalize_url, with_rotating_str, base62

load_dotenv()
app = FastAPI()
db = Redis(host=getenv("REDIS_MASTER_SERVICE_HOST", "0.0.0.0"), port=getenv("REDIS_MASTER_SERVICE_PORT", "6379"))
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_short_urls():
    urls = db.hgetall(URLS)
    urls_list = [{SHORT_URL: format_short_url(short.decode("utf-8")), LONG_URL: long} for short, long in urls.items()]

    return {URLS: urls_list}


@app.get("/{short_url}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def read_short_url(short_url: str):
    long_url = db.hget(URLS, short_url)

    if not long_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    return RedirectResponse(url=long_url.decode("utf-8"))


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_short_url(url: URL):
    long_url = canonicalize_url(url.long_url)

    if not long_url:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="URL invalid")

    ####################################
    # counter approach
    ####################################
    # count = db.incrby(COUNT, 1)
    # short_url = format_short_url(encode(count))
    # db.hset(URLS, short_url, long_url)

    ####################################
    # md5/base62 approach
    ####################################
    setter = lambda short_url: db.hsetnx(URLS, short_url, long_url)
    short_url = with_rotating_str(base62(long_url), setter)

    return {SHORT_URL: format_short_url(short_url), LONG_URL: long_url}
