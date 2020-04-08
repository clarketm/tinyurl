from hashlib import md5
from typing import Callable
from urllib.parse import urlparse

from base62 import encode

from .constants import ORIGIN


def rotate_until(s: str, f: Callable[[str], int]):
    i = 0
    char_len = 7
    hash_len = len(s)

    while (n := i // hash_len + char_len) <= hash_len:
        short_hash = s[:n]

        if f(short_hash):
            break

        s = rotate(s, 1)
        i += 1

    return short_hash


def base62(s: str) -> str:
    return encode(int(md5(s.encode("utf-8")).hexdigest(), 36))


def rotate(s: str, n: int):
    return s[n:] + s[:n]


def canonicalize_url(url: str) -> str:
    scheme, _, host = url.rpartition(r"//")
    url = urlparse(f"{scheme}//{host}", scheme="http")
    return url.geturl()


def format_short_url(url: str, scheme: str = "") -> str:
    return "/".join(filter(None, [scheme, ORIGIN, url]))
