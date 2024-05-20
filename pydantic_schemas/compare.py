from datetime import datetime
from pydantic import BaseModel


class ComparisonStats(BaseModel):
    comp_id : int
    jaccard_score : float
    tfidf_score : float
    embeddings_score : float
