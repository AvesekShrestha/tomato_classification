from pathlib import Path
import os
import torch
from dotenv import load_dotenv
from utils.errors.index import InternalServerError
from utils.models.index import CNN


load_dotenv(Path(__file__).resolve().parents[2] / ".env")

file_path = Path(os.environ["MODEL_PATH"]).expanduser().resolve()
model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model() : 
    global model
    print("Hello from load model function")

    if not file_path.exists() : 
        raise InternalServerError(f"No model found at {file_path}")

    if not file_path.is_file() : 
        raise InternalServerError(f"MODEL_PATH must point to a model file, got {file_path}")

    if model is None :
        model = CNN(num_classes=11)
        model.load_state_dict(torch.load(file_path, map_location=device, weights_only=True))
        return model

def get_model() : 

    if model is None:
        raise InternalServerError("Model is not loaded")

    return model
