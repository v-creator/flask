import pydantic


class CreateAnnouncement(pydantic.BaseModel):

    header: str
    user: str
    description: str
