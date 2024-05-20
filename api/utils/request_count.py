from sqlalchemy.orm import Session

from db.models.request_count import RequestCount

def save_count(db:Session, email:str):
    """save the number of requests sent with the email address"""
    db_count = RequestCount(email=email)
    db.add(db_count)
    db.flush()
    return db_count

def get_count(db:Session, email:str):
    """get the number of requests sent with the email address"""
    return db.query(RequestCount).filter(RequestCount.email == email).one_or_none()


def update_count(db: Session, email: str):
    """check and update number of requests per email"""
    db_count = get_count(db=db, email=email) or save_count(db=db, email=email)
    db_count.count += 1
    db.flush()
    return db_count.count 


