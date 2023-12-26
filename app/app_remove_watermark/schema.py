import datetime
from typing import Optional
from pydantic import BaseModel

class RemoveWatermarkDto(BaseModel):
    roi_list:str
    threshold:int
    kernel_size:int
    video_path:str
    save_path:str