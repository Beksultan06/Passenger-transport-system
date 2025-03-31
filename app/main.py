from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, routes, schedules, users, gps, map

app = FastAPI(title="Passenger Transport System")

# Настройки CORS
origins = [
    "http://localhost:3000",  # Разрешить доступ с фронтенда на localhost
    "http://127.0.0.1:3000",  # Другой вариант localhost
    # "https://myfrontend.com",  # Продакшн-домен (замени на свой)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешённые методы: GET, POST, PUT, DELETE и т.д.
    allow_headers=["*"],  # Разрешённые заголовки
)

# Подключение маршрутов
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(routes.router, prefix="/api/v1/routes", tags=["Routes"])
app.include_router(schedules.router, prefix="/api/v1/schedules", tags=["Schedules"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(gps.router, prefix="/api/v1/gps", tags=["GPS"])
app.include_router(map.router, prefix="/api/v1/map", tags=["Map"])
