from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import LoginRequest, Token
from auth import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return Token(access_token=access_token)
