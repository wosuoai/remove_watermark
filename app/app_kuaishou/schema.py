import datetime
from typing import Optional
from pydantic import BaseModel

class KuaishouDto(BaseModel):
    url:str
