from sqlalchemy.orm import Session

from db.models.comparison import Comparison, ComparisonStats

def save_comparison(db: Session, text1_id:int, text2_id:int):
    """save text-comparison pair data"""
    db_comparison = Comparison(text1_id=text1_id, text2_id=text2_id)
    db.add(db_comparison)
    db.flush()
    return db_comparison

def get_comparison(db: Session, text1_id:int, text2_id:int):
    return db.query(Comparison).filter(Comparison.text1_id==text1_id and Comparison.text2_id==text2_id).first() #could be .all() 

def save_comparison_stats(db:Session, comp_id:int, jaccard_score:float, tfidf_score:float, embeddings_score:float):
    """save text-comparison statistics data"""
    db_comparison_stats = ComparisonStats(
        comp_id=comp_id, 
        jaccard_score=jaccard_score,
        tfidf_score=tfidf_score,
        embeddings_score=float(embeddings_score)
        )
    db.add(db_comparison_stats)
    try:
        db.flush()
    except Exception as e:
        print(f"db.flush error: {e}")
    return db_comparison_stats

def get_comparison_stats(db:Session, comp_id:int):
    """get comparison statistics"""
    return db.query(ComparisonStats).filter(ComparisonStats.comp_id == comp_id).first()







