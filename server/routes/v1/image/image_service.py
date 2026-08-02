from fastapi import HTTPException, status
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
import requests
from typing import cast
import torch.nn.functional as F
from utils.errors.index import AppException
import uuid
from pathlib import Path

class ImageService : 

    def __init__(self) -> None:
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
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                    },
                },
                timeout=60,
            )

            response.raise_for_status()

            ollama_data = response.json()
            text_response = ollama_data.get("response")

            if not text_response:
                raise BadGateway("Model returned empty response")

            parsed = json.loads(text_response)
            return ImageResponse(**parsed)
        except requests.exceptions.ConnectionError:
            raise ServiceUnavailable("Ollama is not running. Start it with: ollama serve")
        except requests.exceptions.Timeout:
            raise ServiceUnavailable("Ollama took too long to respond. Try again.")
        except AppException: 
            raise

        except Exception:
            raise BadGateway("AI Service Error. Failed to generate disease advice.")
