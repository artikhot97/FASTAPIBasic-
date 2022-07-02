from fastapi import APIRouter
from app.users import route_users

api_router = APIRouter()

api_router.include_router(route_users.router, tags=["users"])