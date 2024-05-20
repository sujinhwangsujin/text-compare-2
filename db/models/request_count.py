from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

class RequestCount(Timestamp, Base):
    __tablename__ = "request_counts"

    email = Column(String(100), primary_key=True, nullable=False)
    count = Column(Integer, default=0)