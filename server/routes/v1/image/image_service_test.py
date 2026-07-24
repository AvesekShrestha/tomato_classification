from google import genai
from torchvision.transforms import Resize, Normalize, ToTensor, Compose
from routes.v1.image.dto.image_response import ImageResponse
from utils.models.model_loader import get_model
from PIL import Image
import io
import torch
from utils.errors.index import InternalServerError
from utils.prompt.index import get_prompt
import json
from typing import cast
import torch.nn.functional as F

class ImageServiceTest : 

    def __init__(self) -> None:
        self.client = genai.Client()

    async def predict(self, file):
        print("Inside predict test function")

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
            'Tomato___healthy'
        ]

        transform = Compose([
            Resize((256, 256)),
            ToTensor(),
            Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        image_bytes = await file.read()

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            raise InternalServerError(str(e))

        input_tensor: torch.Tensor = cast(torch.Tensor, transform(image))
        input_tensor = input_tensor.unsqueeze(0)

        model = get_model()

        # Define Temperature and Threshold
        TEMPERATURE = 2.5  # T > 1 softens logits for out-of-distribution images
        THRESHOLD = 0.75   # Minimum required probability post-scaling

        with torch.no_grad():
            logits = model(input_tensor)

            # 1. Scale raw logits by Temperature BEFORE Softmax
            scaled_logits = logits / TEMPERATURE

            # 2. Compute softened probabilities
            probs = F.softmax(scaled_logits, dim=1)

            # 3. Get top class confidence and index
            confidence, prediction = torch.max(probs, 1)

            confidence_score = float(confidence.item())
            predicted_class = classes[int(prediction.item())]

        print(f"Confidence: {confidence_score:.2%}, Class: {predicted_class}")

        # Reject as "Unknown" if confidence doesn't clear the scaled threshold
        if confidence_score < THRESHOLD:
            return "Unknown"

        return predicted_class
