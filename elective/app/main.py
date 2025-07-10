from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from . import models, auth, database
from .routes import students, courses, teachers 
from .routes import library 

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="College Management API",
    description="A RESTful API for managing college students, courses, and teachers",
    version="1.0.0"
)

app.include_router(students.router)
app.include_router(teachers.router) 
app.include_router(library.router)
app.include_router(courses.router)

@app.post("/login", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not auth.authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth.create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to College Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "college-management-api"}
