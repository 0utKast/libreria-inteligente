from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
import models
import os

def get_book_by_path(db: Session, file_path: str):
    return db.query(models.Book).filter(models.Book.file_path == file_path).first()

def get_books(db: Session, category: str | None = None, search: str | None = None, author: str | None = None):
    query = db.query(models.Book)
    if category:
        query = query.filter(models.Book.category == category)
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Book.title.ilike(search_term),
                models.Book.author.ilike(search_term),
                models.Book.category.ilike(search_term)
            )
        )
    return query.order_by(desc(models.Book.id)).all()

def get_categories(db: Session) -> list[str]:
    return [c[0] for c in db.query(models.Book.category).distinct().order_by(models.Book.category).all()]

def create_book(db: Session, title: str, author: str, category: str, cover_image_url: str, file_path: str):
    db_book = models.Book(
        title=title,
        author=author,
        category=category,
        cover_image_url=cover_image_url,
        file_path=file_path
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        # Eliminar archivos asociados
        if book.file_path and os.path.exists(book.file_path):
            os.remove(book.file_path)
        if book.cover_image_url and os.path.exists(book.cover_image_url):
            os.remove(book.cover_image_url)
        
        db.delete(book)
        db.commit()
    return book

def delete_books_by_category(db: Session, category: str):
    books_to_delete = db.query(models.Book).filter(models.Book.category == category).all()
    if not books_to_delete:
        return 0
    
    for book in books_to_delete:
        # Eliminar archivos asociados
        if book.file_path and os.path.exists(book.file_path):
            os.remove(book.file_path)
        if book.cover_image_url and os.path.exists(book.cover_image_url):
            os.remove(book.cover_image_url)
        db.delete(book)
        
    count = len(books_to_delete)
    db.commit()
    return count
