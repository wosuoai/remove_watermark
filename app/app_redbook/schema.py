import datetime
from typing import Optional
from pydantic import BaseModel

class RedbookDto(BaseModel):
    url:str
    proxies_status:int