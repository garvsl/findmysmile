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
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, ExactMatchFilter, FilterOperator
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.readers.json import JSONReader
import getpass, os, pymongo, pprint

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



@app.route('/llm', methods=['POST'])
def predi():
   
    data = request.json
    text_prompt = data.get('text_prompt', '')

   

    Settings.llm = OpenAI()
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    Settings.chunk_size = 100
    Settings.chunk_overlap = 10

    reader = JSONReader()
    docs = reader.load_data("./data/proc.json")
    docs2 = SimpleDirectoryReader(input_files=["./data/crossbite.pdf"]).load_data()
    docs3 = SimpleDirectoryReader(input_files=["./data/emax-veneer.pdf"]).load_data()
    docs4 = SimpleDirectoryReader(input_files=["./data/emax-veneer2.pdf"]).load_data()
    docs5 = SimpleDirectoryReader(input_files=["./data/gap.pdf"]).load_data()
    docs6 = SimpleDirectoryReader(input_files=["./data/openbite.pdf"]).load_data()
    docs7 = SimpleDirectoryReader(input_files=["./data/zirconium-veneer.pdf"]).load_data()
    docs8 = SimpleDirectoryReader(input_files=["./data/overjet.pdf"]).load_data()
    docs9 = SimpleDirectoryReader(input_files=["./data/underbite.pdf"]).load_data()

    mongodb_client = pymongo.MongoClient(ATLAS_CONNECTION_STRING)
    atlas_vector_search = MongoDBAtlasVectorSearch(
        mongodb_client,
        db_name = "default_db",
        collection_name = "default_collection",
        index_name = "vector_index"
    )
    vector_store_context = StorageContext.from_defaults(vector_store=atlas_vector_search)

    vector_store_index = VectorStoreIndex.from_documents(
        docs + docs2 + docs3 + docs4 + docs5 + docs6 + docs7 + docs8 + docs9, storage_context=vector_store_context, show_progress=True
    )

    vector_store_retriever = VectorIndexRetriever(index=vector_store_index, similarity_top_k=5)

    query_engine = RetrieverQueryEngine(retriever=vector_store_retriever)

    response = query_engine.query(text_prompt)

    return response


if __name__ == "__main__":
  app.run()