from fastapi import FastAPI
from app.routes import auth, routes, schedules, users, gps, map

app = FastAPI(title="Passenger Transport System")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(routes.router, prefix="/api/v1/routes", tags=["Routes"])
app.include_router(schedules.router, prefix="/api/v1/schedules", tags=["Schedules"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(gps.router, prefix="/api/v1/gps", tags=["GPS"])
app.include_router(map.router, prefix="/api/v1/map", tags=["Map"])
