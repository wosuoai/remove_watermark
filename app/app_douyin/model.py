from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class DouyinVideo(Base, DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "douyin_video"
