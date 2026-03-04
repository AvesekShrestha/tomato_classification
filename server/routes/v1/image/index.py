from fastapi import APIRouter, File, UploadFile
from utils.response.index import ResponseModel
from routes.v1.image.image_service import ImageService
from routes.v1.image.dto.image_response import ImageResponse


router = APIRouter()
image_service = ImageService() 

@router.post("/predict/")
async def predict_image(file: UploadFile = File(...)):

    disease_class = await image_service.predict(file)
    disease_info = image_service.get_diesase_info(disease_class)

    return ResponseModel[ImageResponse](
        success=True,
        data=disease_info,
        message="Successfully predicted and analyzed the disease"
    )
