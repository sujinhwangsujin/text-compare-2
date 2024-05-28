from pydantic import BaseModel

class TwoTexts(BaseModel):
    email: str
    text1: str
    text2: str
