from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List

import models
from database import engine, get_db
from auth import hash_password, verify_password, create_access_token
from rag import save_uploaded_file, extract_text_from_pdf, chunk_text

# Initialize FastAPI app
app = FastAPI(title="AI Chatbot API")

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    message: str

@app.post("/signup", response_model=Message, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create new user
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email, "id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to upload a PDF document, extract its text, and chunk it.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Save the file
    try:
        file_path = save_uploaded_file(file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save file: {str(e)}"
        )
    
    # Extract text
    text = extract_text_from_pdf(file_path)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract text from PDF or PDF is empty"
        )
    
    # Chunk text
    chunks = chunk_text(text)
    
    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "File uploaded and processed successfully"
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Chatbot API"}
