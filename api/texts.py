from typing import List

import fastapi 
from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.db_setup import get_db
from pydantic_schemas.text import Text
from pydantic_schemas.request import TwoTexts
from api.utils.texts import get_texts, save_text 
from api.utils.comparisons import save_comparison, save_comparison_stats
from api.utils.similarities import jaccard_similarity, tfidf_similarity, embeddings_similarity
from api.utils.request_count import update_count

router = fastapi.APIRouter()

"""show all data in <texts> table"""
@router.get("/texts", response_model=List[Text])
async def read_texts(skip: int = 0, limit: int = 100, db: Session=Depends(get_db)):
    texts = get_texts(db, skip=skip, limit=limit)
    return texts

"""upload two texts and get comparison statistics result"""
@router.post("/texts")
async def create_texts(request: Request, item: TwoTexts, db: Session=Depends(get_db)):  
    model = request.app.state.MODEL
    tokenizer = request.app.state.TOKENIZER
    email = item.email
    text1 = item.text1
    text2 = item.text2
    try:
        #1. check and update request count from the email
        if update_count(db=db, email=email) > 100:
            db.commit()
            raise HTTPException(status_code=429, detail="Requests per email is limited to 100.")
        #2. calculate stats : define calculation function in utils.texts.py
        jaccard_score = jaccard_similarity(text1, text2)
        tfidf_score = tfidf_similarity(text1, text2)
        embeddings_score = embeddings_similarity(text1, text2, model=model, tokenizer=tokenizer)


        #3. save the texts to table <texts>
        db_text1 = save_text(db=db, email=email, data=text1)
        db_text2 = save_text(db=db, email=email, data=text2)

        #4. save comparison info to table <comparisons>
        text1_id = db_text1.id
        text2_id = db_text2.id
        db_comp = save_comparison(db=db, text1_id=text1_id, text2_id=text2_id)

        #5. save comparison statistics to table <comparison_stats>
        comp_id = db_comp.id
        db_stat = save_comparison_stats(
            db=db, comp_id=comp_id, 
            jaccard_score=jaccard_score, 
            tfidf_score=tfidf_score, 
            embeddings_score=embeddings_score
        )
        if embeddings_score >= 0.6:
            print("cv: ", text1)
            print("job: ", text2)
        
        #6. commit changes to the database
        db.commit()   

        #7. redirect to stats page
        return RedirectResponse(url=f"/stats/{db_stat.comp_id}", status_code=303)

    except Exception as e:
        # Catch general exceptions
        db.rollback()   
        raise HTTPException(status_code=500, detail=f'{e}')


