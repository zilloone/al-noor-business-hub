from fastapi import APIRouter

from app.api.routes import  login, users, products, orders


api_router = APIRouter()



api_router.include_router(users.router)
api_router.include_router(products.router)
api_router.include_router(login.router)
api_router.include_router(orders.router)

