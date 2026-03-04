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

class ImageService : 

    def __init__(self) -> None:
        self.client = genai.Client()

    async def predict(self, file) :

        classes = ['Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
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

        input_tensor = transform(image).unsqueeze(0)

        model = get_model()
        with torch.no_grad():
            output = model(input_tensor)
            _, prediction = torch.max(output, 1)
            predicted_class = classes[prediction.item()]
        
        return predicted_class

    def get_diesase_info(self, disease_class) -> ImageResponse : 

        prompt = get_prompt(disease_class)
        response = self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"{prompt}",
        )

        text_response = response.text
        parsed = json.loads(str(text_response))

        return ImageResponse(**parsed)


