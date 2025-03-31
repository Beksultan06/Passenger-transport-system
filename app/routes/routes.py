from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.orm import selectinload
from app.db.database import SessionLocal
from app.db.models.route import Route
from app.db.schemas.route import RouteCreate, RouteResponse, RouteUpdate

router = APIRouter()

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получить все маршруты с фильтрацией и пагинацией
@router.get("/", response_model=List[RouteResponse])
def get_routes(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Route).options(selectinload(Route.schedules))
    
    if name:
        query = query.filter(Route.name.ilike(f"%{name}%"))
    
    routes = query.offset(skip).limit(limit).all()
    return routes


# Получить маршрут по ID
@router.get("/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).options(selectinload(Route.schedules)).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return route


# Создать новый маршрут с проверкой уникальности
@router.post("/", response_model=RouteResponse)
def create_route(route: RouteCreate, db: Session = Depends(get_db)):
    existing_route = db.query(Route).filter(
        Route.name == route.name,
        Route.start_point == route.start_point,
        Route.end_point == route.end_point
    ).first()
    
    if existing_route:
        raise HTTPException(status_code=400, detail="Такой маршрут уже существует")

    new_route = Route(**route.dict())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route


# Обновить маршрут
@router.put("/{route_id}", response_model=RouteResponse)
def update_route(route_id: int, route_data: RouteUpdate, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    for key, value in route_data.dict(exclude_unset=True).items():
        setattr(route, key, value)

    db.commit()
    db.refresh(route)
    return route


# Удалить маршрут
@router.delete("/{route_id}", response_model=RouteResponse)
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    db.delete(route)
    db.commit()
    return route
