from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from config.database.index import get_db
from middlewares.auth_middleware import current_user_id
from utils.response.index import ResponseModel
from routes.v1.image.image_service import ImageService
from routes.v1.image.dto.image_response import ImageResponse
from routes.v1.image.image_service_test import ImageServiceTest


router = APIRouter()
image_service = ImageService() 
image_service_test = ImageServiceTest()

@router.post("/predict/")
async def predict_image(user_id : int = Depends(current_user_id), file: UploadFile = File(...), db : AsyncSession = Depends(get_db)):

    disease_info : ImageResponse = await image_service.predict(user_id=user_id, file=file, db=db)

    return ResponseModel[ImageResponse](
        success=True,
        data=disease_info,
        message="Successfully predicted and analyzed the disease"
    )

