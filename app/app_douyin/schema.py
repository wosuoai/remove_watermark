import datetime
from typing import Optional
from pydantic import BaseModel

class DouyinVideoDto(BaseModel):
    url:str
class DouyinUrlDto(BaseModel):
    url:str