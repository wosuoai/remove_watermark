from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class RemoveWatermark(Base, DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "remove_watermark"
