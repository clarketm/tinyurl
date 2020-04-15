from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from .api.cassandra import Cassandra
from .api.constants import URLS, SHORT_URL, LONG_URL
from .api.models import URL

# from .api.redis import Redis
from .api.utils import format_short_url, canonicalize_url, rotate_until, base62

load_dotenv()
app = FastAPI()
# db = Redis(hash=URLS)
db = Cassandra(keyspace=URLS, table=URLS)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_short_urls():
    urls = db.get_all()
    urls_list = [{SHORT_URL: format_short_url(url[SHORT_URL]), LONG_URL: url[LONG_URL]} for url in urls]

    return {URLS: urls_list}


@app.get("/{short_url}", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def read_short_url(short_url: str):
    url = db.get(short_url)

    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    return RedirectResponse(url=url[LONG_URL])


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
    setter = lambda short_url: db.set(short_url, long_url)
    short_url = rotate_until(base62(long_url), setter)

    if not short_url:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="URL not hashable")

    return {SHORT_URL: format_short_url(short_url), LONG_URL: long_url}
