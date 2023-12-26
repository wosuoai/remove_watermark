import datetime
from typing import Optional
from pydantic import BaseModel

class DouyinUrlDto(BaseModel):
    url:str
    proxies_status: int