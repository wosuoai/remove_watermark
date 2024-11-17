import datetime
from typing import Optional
from pydantic import BaseModel

class ZuiyouDto(BaseModel):
    url:str
    proxies_status:int