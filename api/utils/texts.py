from sqlalchemy.orm import Session

from db.models.text import Text


def get_text(db: Session, text_id: int):
    """get text by id"""
    return db.query(Text).filter(Text.id == text_id).first()


def get_text_by_content(db: Session, data: str):
    """get text by content"""
    return db.query(Text).filter(Text.data == data).first()


def get_texts(db: Session, skip: int = 0, limit: int = 100):
    """get all texts"""
    return db.query(Text).offset(skip).limit(limit).all()


def save_text(db: Session, email:str, data: str):
    """save text in the database"""
    db_text = Text(email=email, data=data)
    db.add(db_text)
    db.flush()
    return db_text
