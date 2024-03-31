from flask import Flask, jsonify, request, g
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from flask_cors import CORS
import torch
from torchvision import transforms
from PIL import Image
import torch.nn as nn
import os 
import torchvision.models as models
from torchvision.datasets import ImageFolder

load_dotenv()
app = Flask(__name__)
CORS(app)

#set config to debug based on .env debug status
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG")
  
@app.route("/")
def hello():
  return "Hello World!"

def transform_image(image):
    user_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    img = Image.open(BytesIO(image.read()))
    img = img.convert("RGB")

    return user_transform(img).unsqueeze(0)

def get_preds(image):
    model = models.resnet18()
    num_ftrs = model.fc.in_features

    transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    original_dataset = ImageFolder('../image-data', transform=transform)
    model.fc = nn.Linear(num_ftrs, len(original_dataset.classes))
    model.load_state_dict(torch.load('fine_tuned_model.pth'))
    model.eval()

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    predicted_class = original_dataset.classes[predicted.item()]
    return predicted_class


@app.route("/pred", methods=['POST'])
def pred():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    image = request.files['image']
    image = transform_image(image)
    prediction = get_preds(image)
    return jsonify({'prediction': prediction})





if __name__ == "__main__":
  app.run()