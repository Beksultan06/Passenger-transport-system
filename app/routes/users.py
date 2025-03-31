from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import check_role, get_password_hash

router = APIRouter()


# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получить всех пользователей (Только для admin)
@router.get("/", response_model=List[UserResponse], dependencies=[Depends(check_role(["admin"]))])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# Получить пользователя по ID (Только для admin)
@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(check_role(["admin"]))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# Создать нового пользователя (Только для admin)
@router.post("/", response_model=UserResponse, dependencies=[Depends(check_role(["admin"]))])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        full_name=user.full_name,
        phone=user.phone,
        password=hashed_password,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Обновить данные пользователя (Только для admin)
@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(check_role(["admin"]))])
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    for key, value in user_data.dict(exclude_unset=True).items():
        if key == "password" and value:
            value = get_password_hash(value)
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# Удалить пользователя (Только для admin)
@router.delete("/{user_id}", response_model=UserResponse, dependencies=[Depends(check_role(["admin"]))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    db.delete(user)
    db.commit()
    return user
