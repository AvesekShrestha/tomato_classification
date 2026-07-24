from pathlib import Path
import torch
from utils.errors.index import InternalServerError
from utils.models.index import CNN


file_path = Path("/home/avesek/Documents/workspace/collage/seventh/project/tomato_classification/model/tomato_state_dict.pth").resolve()
model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model() : 
    global model
    print("Hello from load model function")

    if not file_path.exists() : 
        raise InternalServerError("No model found")

    if model is None :
        model = CNN(num_classes=11)
        model.load_state_dict(torch.load(file_path, map_location=device, weights_only=True))
        return model

def get_model() : 

    if model is None:
        raise InternalServerError("Model is not loaded")

    return model
