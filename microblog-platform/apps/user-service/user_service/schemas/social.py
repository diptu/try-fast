
from pydantic import BaseModel, Field, HttpUrl


class SocialBase(BaseModel):
    links: dict[str, HttpUrl] = Field(default_factory=dict)

    model_config = {"extra": "ignore"}
