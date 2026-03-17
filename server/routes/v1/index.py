from fastapi import APIRouter, Depends
from middlewares.auth_middleware import authenticate
from routes.v1.image.index import router as image_router
from routes.v1.auth.index import router as auth_router
from routes.v1.user.index import router as user_router
from routes.v1.post.index import router as post_router

router = APIRouter()

router.include_router(image_router, prefix="/image", dependencies=[Depends(authenticate)])
router.include_router(auth_router, prefix="/auth")
router.include_router(user_router, prefix="/user", dependencies=[Depends(authenticate)])
router.include_router(post_router, prefix="/post", dependencies=[Depends(authenticate)])
