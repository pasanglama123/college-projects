from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from .database import Base
from datetime import date

# -------------------- Students --------------------
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    year = Column(Integer)
    
    borrow_records = relationship("Borrow", back_populates="student")  # For library

# -------------------- Courses --------------------
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    credit_hours = Column(Integer)

# -------------------- Teachers --------------------
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    department = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)

# -------------------- Books --------------------
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    total_copies = Column(Integer)
    available_copies = Column(Integer)

    borrow_records = relationship("Borrow", back_populates="book")

# -------------------- Borrow Records --------------------
class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrow_date = Column(Date, default=date.today)
    due_date = Column(Date)
    return_date = Column(Date, nullable=True)
    returned = Column(Boolean, default=False)

    student = relationship("Student", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
