from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str
    url: str
    count_views: int
    rating: str