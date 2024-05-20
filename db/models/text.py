from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Text(Timestamp, Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), ForeignKey('request_counts.email'), nullable=False)
    data = Column(Text, default='')




