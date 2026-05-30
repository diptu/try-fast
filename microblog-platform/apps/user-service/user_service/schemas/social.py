from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SocialBase(BaseModel):
    links: dict[str, HttpUrl] = Field(default_factory=dict)

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        validate_by_name=True,
    )
