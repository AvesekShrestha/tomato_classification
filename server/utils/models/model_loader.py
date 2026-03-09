from pathlib import Path
import torch
from utils.errors.index import InternalServerError
from utils.models.index import NeuralNet


file_path = Path("/home/avesek/Documents/workspace/collage/seventh/project/tomato_classification/model/tomato_state_dict.pth").resolve()
model = None

def load_model() : 
    global model
    print("Hello from load model function")

    if not file_path.exists() : 
        raise InternalServerError("No model found")

    if model is None : 
        model = NeuralNet()
        model.load_state_dict(torch.load(file_path, map_location=torch.device("cpu")))
        model.eval()
    return model

def get_model() : 

    if model is None:
        raise InternalServerError("Model is not loaded")

    return model
