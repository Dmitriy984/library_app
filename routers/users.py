from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserResponse, UserCreate, PasswordChangeRequest
from dependencies.auth_deps import get_current_active_user, get_admin_user
from auth import get_password_hash, get_user_by_username

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me/password")
async def change_password(password_data: PasswordChangeRequest,
                          current_user: User = Depends(get_current_active_user),
                          db: Session = Depends(get_db)):
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(400, "Old password is incorrect")
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db),
                      _=Depends(get_admin_user)):
    if get_user_by_username(db, user_data.username):
        raise HTTPException(400, "Username already taken")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(username=user_data.username, email=user_data.email,
                password_hash=get_password_hash(user_data.password), role=user_data.role)
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.patch("/{user_id}/deactivate")
async def deactivate_user(user_id: int, db: Session = Depends(get_db),
                          _=Depends(get_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.is_active = False
    db.commit()
    return {"message": "User deactivated"}
