from datetime import datetime

from pydantic import BaseModel

class TextBase(BaseModel):
    email: str
    data: str


class Text(TextBase):
    id: int
    created_at: datetime


