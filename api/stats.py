import fastapi 
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.db_setup import get_db
from pydantic_schemas.compare import ComparisonStats
from api.utils.comparisons import get_comparison_stats

router = fastapi.APIRouter()

     
"""view similarity comparison statistics between two texts"""
@router.get("/stats/{comp_id}", response_model=ComparisonStats)
async def read_stats(comp_id: int, db: Session=Depends(get_db)):
    db_stats = get_comparison_stats(db=db, comp_id=comp_id)
    
    if db_stats is None:    
        #in case data with the stats_id doesn't exist
        raise HTTPException(status_code=404, detail="Stats not found")
    return db_stats