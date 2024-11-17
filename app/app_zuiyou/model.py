from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class ZuiyouVideo(Base, DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "zuiyou_image"
