from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/library", tags=["Library"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/books/", response_model=schemas.Book)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(**book.dict(), available_copies=book.total_copies)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/books/", response_model=list[schemas.Book])
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router.post("/borrow/", response_model=schemas.Borrow)
def borrow_book(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    if not book or book.available_copies < 1:
        raise HTTPException(status_code=400, detail="Book not available")
    
    book.available_copies -= 1
    db_borrow = models.Borrow(**borrow.dict())
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

@router.post("/return/{borrow_id}")
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if not borrow or borrow.returned:
        raise HTTPException(status_code=404, detail="Invalid borrow record")
    
    borrow.return_date = date.today()
    borrow.returned = True

    book = db.query(models.Book).filter(models.Book.id == borrow.book_id).first()
    book.available_copies += 1

    db.commit()
    return {"message": "Book returned successfully"}
