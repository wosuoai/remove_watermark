# 导入 declarative，方便 alembic 直接从这个文件导入数据
from models.base import Base
from pydantic import BaseModel

# 导入 models
from app_user.model import *

class CookiesItem(BaseModel):
    name:str # cookie名称
    value:str # cookie值
    domain:str # cookie指向的域名
    path:str # cookie指向郁域名路径
    
item = CookiesItem
item.name= "1"
item.value="2"
print(item)