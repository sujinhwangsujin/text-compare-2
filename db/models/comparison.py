#from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Numeric

from ..db_setup import Base
from .mixins import Timestamp


class Comparison(Timestamp, Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    text1_id = Column(Integer, ForeignKey('texts.id'), nullable=False)
    text2_id = Column(Integer, ForeignKey('texts.id'), nullable=False)


class ComparisonStats(Timestamp, Base):
    __tablename__ = "comparison_stats"

    comp_id = Column(Integer, ForeignKey("comparisons.id"), primary_key=True)
    jaccard_score = Column(Numeric(precision=4, scale=3), default=0)
    tfidf_score = Column(Numeric(precision=4, scale=3), default=0)    
    embeddings_score = Column(Numeric(precision=4, scale=3), default=0)






