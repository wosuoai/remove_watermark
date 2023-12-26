import datetime
from typing import Optional
from pydantic import BaseModel

class BilibiliDto(BaseModel):
    url:str
