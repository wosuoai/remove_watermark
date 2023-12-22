from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class KuaishouVideo(Base, DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "kuaishou_image"
