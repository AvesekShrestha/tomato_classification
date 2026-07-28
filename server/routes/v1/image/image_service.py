from fastapi import HTTPException, status
from google import genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import exc
from torchvision.transforms import Resize, Normalize, ToTensor, Compose
from routes.v1.image.dto.image_response import ImageResponse
from routes.v1.image.dto.scan_request import ScanRequest
from routes.v1.image.image_repository import ImageRepository
from utils.models.model_loader import get_model
from PIL import Image
import io
import torch
from utils.errors.index import BadGateway, InternalServerError, ServiceUnavailable
from utils.prompt.index import get_prompt
import json
from typing import cast
import torch.nn.functional as F
from google.genai.errors import ServerError, APIError
from google.genai import types
from utils.errors.index import AppException
import uuid
from pathlib import Path

class ImageService : 

    def __init__(self) -> None:
        self.client = genai.Client()
        self.image_repository = ImageRepository()

    async def predict(self, user_id : int, file, db : AsyncSession) -> ImageResponse:

        classes = [
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___Unknown',
            'Tomato___healthy'
        ]

        transform = Compose([
            Resize((256, 256)),
            ToTensor(),
            Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        image_bytes = await file.read()

        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        filename = f"{uuid.uuid4()}_{file.filename}"

        file_path = upload_dir / filename

        with open(file_path, "wb") as f:
            f.write(image_bytes)

        image_url = f"/uploads/{filename}"

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            input_tensor: torch.Tensor = cast(torch.Tensor, transform(image))
            input_tensor = input_tensor.unsqueeze(0)

            model = get_model()

            with torch.no_grad():
                output = model(input_tensor)

                probs = F.softmax(output, dim=1)

                confidence, prediction = torch.max(probs, 1)

                confidence_score = float(confidence.item())
                predicted_class = classes[int(prediction.item())]

                print(confidence_score, predicted_class)

            THRESHOLD = 0.7

            if confidence_score < THRESHOLD:
                scan : ScanRequest = ScanRequest(
                    image_url=image_url,
                    predicted_class="Unknown"
                )
                await self.image_repository.create(user_id=user_id, data=scan, db=db)
                return ImageResponse(
                    predicted_class="Unknown"
                )


            disease_info : ImageResponse = self.get_diesase_info(predicted_class)
            
            scan : ScanRequest = ScanRequest(
                image_url=image_url,
                predicted_class=disease_info.predicted_class,
                cause=disease_info.cause,
                prescriptions=disease_info.prescriptions
            )
            await self.image_repository.create(user_id=user_id, data=scan, db=db)

            return disease_info
        except Exception as e:
            raise InternalServerError(str(e))



    def get_diesase_info(self, disease_class: str) -> ImageResponse:
        if disease_class in ["Unknown", "Tomato___Unknown"]:
            return ImageResponse(
                predicted_class="Unknown"
            )

        prompt = get_prompt(disease_class)

        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ImageResponse,
                ),
            )

            if response and response.parsed:
                text_response = response.text
                parsed = json.loads(str(text_response))
                return ImageResponse(**parsed)

            raise BadGateway("Model returned empty response") 
        except (ServerError, APIError) as e:
            error_msg = str(e)
            
            is_high_traffic = (
                getattr(e, "code", None) in [503, 500, 429] 
                or "UNAVAILABLE" in error_msg 
                or "high demand" in error_msg.lower() 
                or "overloaded" in error_msg.lower()
            )

            if is_high_traffic:
                raise ServiceUnavailable("The AI model is currently experiencing high traffic. Try later")
            raise BadGateway("AI Service Error. Failed to generate response.")

        except AppException: 
            raise

        except Exception:
            raise InternalServerError("An unexpected error occurred while processing the request.")
