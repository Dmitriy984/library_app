from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import decode_access_token, get_user_by_username, oauth2_scheme

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or payload.username is None:
        raise credentials_exception
    user = get_user_by_username(db, username=payload.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

async def get_librarian_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in ("admin", "librarian"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
