from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# --- Student ---
class StudentBase(BaseModel):
    name: str
    department: str
    year: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    class Config:
        orm_mode = True

# --- Course ---
class CourseBase(BaseModel):
    name: str
    credit_hours: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    class Config:
        orm_mode = True


# --- Teacher ---
class TeacherBase(BaseModel):
    name: str
    department: str
    email: str
    phone: str

class TeacherCreate(TeacherBase):
    pass

class Teacher(TeacherBase):
    id: int
    class Config:
        orm_mode = True

# --- book library ---

class BookBase(BaseModel):
    title: str
    author: str
    total_copies: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available_copies: int
    class Config:
        orm_mode = True

class BorrowBase(BaseModel):
    student_id: int
    book_id: int
    due_date: date

class BorrowCreate(BorrowBase):
    pass

class Borrow(BorrowBase):
    id: int
    borrow_date: date
    return_date: Optional[date]
    returned: bool
    class Config:
        orm_mode = True