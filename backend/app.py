
from flask import Flask, jsonify, logging, request, g
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
import torch
from torchvision import transforms
from PIL import Image
import torch.nn as nn
import os 
import torchvision.models as models
from torchvision.datasets import ImageFolder
import random
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/Users/ayandas/Desktop/VS_Code_Projects/findmysmile/scripts/')
from treatment_and_locations_recommended import treatment_recommendation, location_recommendation, treatment_and_locations

load_dotenv()
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
#logging.getLogger('flask_cors').level = logging.DEBUG

#set config to debug based on .env debug status
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG")

treatment_procedures = ["crossbite", "emax-veneer","gap","makeover", "openbite", "overbite", "overjet", "underbite", "zirconium"]

selected_procedure = random.choice(treatment_procedures)
print(selected_procedure)  # check to see the procedure that was selected

@app.route("/")
def hello():
  return "Hello World!"   
# prints out "Hello World!" on the route http://127.0.0.1:5000/

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

# the methods specified are all related to data augmentation
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
    model.load_state_dict(torch.load('fine_tuned_model.pth'))   # this is the link where the model gets saved.
    model.eval()

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    predicted_class = original_dataset.classes[predicted.item()]
    return predicted_class

#test the function to see if it works as intended
#resulting_class = get_preds(transform_image('/Users/ayandas/Desktop/VS_Code_Projects/findmysmile/image-data/labeled/all-on-4-implant-150x150.webp'))

#print(resulting_class)

# api route to predict the treatment based on the image that is passed in, the pred() function calls upon the get_preds function to make the prediciton
@app.route("/pred", methods=['POST'])
@cross_origin()
def pred():
    print("Request received")  # add this during the function call invocation 
    if 'image' not in request.files:
        print("No Image part in this request")
        return jsonify({'error': 'No image part'}), 400
    try:
        image = request.files['image']
        print(f"Image received: {image.filename}")   # display the image that was recieved
        image_transformed = transform_image(image)
        prediction = get_preds(image_transformed)
        print(f"prediction: {prediction}")  # retrieve the resulting prediction
        return jsonify({'prediction': prediction})
    except Exception as e:
        print(f"Error: {e}")
        # in the case that an error occurs, instead, simply print out the randomly genereated treatment and return the error message
        print(f"Randomly generated treatment\n: {selected_procedure}\n\n")
        # Handle unexpected errors --> expect a bunch of error message after this message on the terminal
        return jsonify({'error': str(e)}), 500, selected_procedure  # function should return three things so that we can call upon it and save the resulting responses to compare the two models

#make a request to /pred
#curl -X POST -F "image-data/allon6/1003-1-768x768.jpg" http://localhost:5000/pred
@app.route("/treatments")
@cross_origin()
def treatments():
    try:
        treatment_recommendation, location_recommendation = treatment_and_locations()
        return jsonify({'treatment-recommendation': treatment_recommendation},
                       {'location-recommendation': location_recommendation})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
  app.run()

# TODO take the output of the image classification and use it to determine the correct proecudre to use. Also retrieve the procedure from the prompt of LLM model and then compare the outputs of the two models to determine which one performed more accurately (we may need some form of metric/evaluation to determine this),