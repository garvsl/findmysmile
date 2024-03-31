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