from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class BilibiliVideo(Base, DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "bilibili_image"
