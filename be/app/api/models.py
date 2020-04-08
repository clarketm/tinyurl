from pydantic import BaseModel


class URL(BaseModel):
    long_url: str
