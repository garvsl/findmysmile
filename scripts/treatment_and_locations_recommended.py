'''
Based on the treatment, it will determine the recommended treatment, the user's location using some form of geolocation tracker and determine the nearby places that are around for the user
'''
import json
import os
import urllib3
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()
from llama_index.embeddings.nomic import NomicEmbedding
from llama_index.core import settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain.embeddings import HuggingFaceEmbeddings 

load_dotenv()
lc_embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
langchain_embed_model = LangchainEmbedding(lc_embed_model)

llm = OpenAI(model="gpt-4", max_tokens=3000)  # adjust this as needed
settings.llm = llm  #set the llm to openAI
settings.embed_model = langchain_embed_model  #set the embedding model to nomic

# read the json data on the locationss
location_data = SimpleDirectoryReader(input_files=["../prompt-data/MA-Data-Organized.json", "../prompt-data/NJ-Data-Organized.json", "../prompt-data/NY-Data-Organized.json"]).load_data()

#print(location_data)   # successfully able to process the json data

#creating the pool manaer instnace for sending requests
http = urllib3.PoolManager()

def location_lookup():
    try:  # you need to look into proper json response handling 
        response = http.request("GET", "http://ipinfo.io/json")
         # Decode response data from bytes to string and load into a Python dictionary
        data = json.loads(response.data.decode('utf-8'))
        print (data)
        json_response = str(response.data)
        json_response.replace("\n", " ")
        # save the data to a json format
         # Save the data to a JSON file with formatting
        with open("../prompt-data/user-location.json", 'w') as location_file:
            json.dump(data, location_file, indent=4, sort_keys=True)  # Pretty print the JSON
        return data
    except urllib3.exceptions.MaxRetryError as e:
        print(f"Max retries exceeded with url: {e.reason}")
    except urllib3.exceptions.TimeoutError as e:
        print(f"Request timed out: {e}")
    
location_lookup()  # test the function
    







# get API key to create embeddings
