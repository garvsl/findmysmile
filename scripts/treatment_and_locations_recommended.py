'''
Based on the treatment, it will determine the recommended treatment, the user's location using some form of geolocation tracker and determine the nearby places that are around for the user
'''
import json
import os
import urllib3
from dotenv import load_dotenv
import nest_asyncio
from prompt_response import treatment_recommendation
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

llm = OpenAI(model="gpt-4", max_tokens=4000)  # adjust this as needed
settings.llm = llm  #set the llm to openAI
settings.embed_model = langchain_embed_model  #set the embedding model to nomic

#print(location_data)   # successfully able to process the json data

#creating the pool manaer instnace for sending requests
http = urllib3.PoolManager()

def location_lookup():
    try:  # you need to look into proper json response handling 
        response = http.request("GET", "http://ipinfo.io/json")
         # Decode response data from bytes to string and load into a Python dictionary
        data = json.loads(response.data.decode('utf-8'))
        #print (data)
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
    
user_location = location_lookup()  # test the function

# now that we hvae the data, we will need to read  that data alongside the data based on the locatons, and retrieve the treatment and recommended locations using the model

location_data = SimpleDirectoryReader(input_files=["../prompt-data/MA-Data-Organized.json", "../prompt-data/NJ-Data-Organized.json", "../prompt-data/NY-Data-Organized.json"]).load_data()

#index creation
index = VectorStoreIndex.from_documents(location_data)  # embed the pdf content

#embedding = nomic_embded_model.get_text_embedding("crossbite.pdf")

#query engine
query_engine = index.as_query_engine()

location_recommendation = query_engine.query(f"Based on the following prompt as provided below:\n{treatment_recommendation}\n as well as the information obtained pertaining to the user's location: {user_location}, provide a list of 15-20 places of the nearby locations for the user based on the location data that you have available at {index}. Particualrly provide information of the name of the clinic, the price, the location, rating (optional), phone contact information, and full address of the individual clinics.")
print("\n\n")  #create some spacings
print("Procedure Recommendation:")
print(treatment_recommendation) 
print("\nLocations Recommended:")
print(location_recommendation)  # this should cause an error

#save the resulting output in a json format
#response_data = {"response" : response}

'''
output_dir = "../embedding_output"
os.makedirs(output_dir, exist_ok=True)

response_text = str(response)

# Define the filepath for the text file
txt_file_path = os.path.join(output_dir, "zirconium_query_response.txt")

# Save the response in text format
with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response_text)

    '''



