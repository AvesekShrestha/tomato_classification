from fastapi import APIRouter
from routes.v1.image.index import router as image_router

router = APIRouter()

router.include_router(image_router, prefix="/image")
