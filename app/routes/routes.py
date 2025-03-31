from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.db.models.route import Route
from app.db.schemas.route import RouteCreate, RouteResponse, RouteUpdate
from app.core.security import check_role

router = APIRouter()


# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получить все маршруты (Доступ для всех)
@router.get("/", response_model=List[RouteResponse])
def get_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()
    return routes


# Создать новый маршрут (Только для admin и dispatcher)
@router.post("/", response_model=RouteResponse, dependencies=[Depends(check_role(["admin", "dispatcher"]))])
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    new_route = Route(**route.dict())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route


# Получить маршрут по ID (Доступ для всех)
@router.get("/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return route


# Обновить маршрут (Только для admin и dispatcher)
@router.put("/{route_id}", response_model=RouteResponse, dependencies=[Depends(check_role(["admin", "dispatcher"]))])
def update_route(route_id: int, route_data: RouteUpdate, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    for key, value in route_data.dict(exclude_unset=True).items():
        setattr(route, key, value)

    db.commit()
    db.refresh(route)
    return route


# Удалить маршрут (Только для admin)
@router.delete("/{route_id}", response_model=RouteResponse, dependencies=[Depends(check_role(["admin"]))])
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    db.delete(route)
    db.commit()
    return route
