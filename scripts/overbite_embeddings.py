# imports
from dotenv import load_dotenv
from llama_index.embeddings.google import GooglePaLMEmbedding
import json
import os
import nest_asyncio
nest_asyncio.apply()
from llama_index.core import settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI


load_dotenv()
# get API key to create embeddings
model_name="models/embeddings-gecko-001"
api_key = os.getenv('GOOGLE_PALM_API_KEY')

Google_palm_embed_model = GooglePaLMEmbedding(model_name=model_name, api_key=api_key)

llm = OpenAI(model="gpt-4", max_tokens=1000)  # adjust this as needed
settings.llm = llm  #set the llm to openAI
settings.embed_model = Google_palm_embed_model  #set the embedding model to nomic

#load the data
overbite = SimpleDirectoryReader(input_dir="../data/overbite").load_data() #read the content within the crossbite directory

 # only read one file for one procedure
print(overbite)  # print out the data to see what it looks like raw

#index creation
index = VectorStoreIndex.from_documents(overbite)  # embed the pdf content

#embedding = nomic_embded_model.get_text_embedding("crossbite.pdf")

#query engine
query_engine = index.as_query_engine()
response = query_engine.query("Provide me details pertaining to the overbite dental procedure based on the data you have been provided.")
print("\n\n")  #create some spacings
print("Query Response For overvite:")
print(response)  # this should cause an error

#save the resulting output in a json format
#response_data = {"response" : response}
output_dir = "../embedding_output"
os.makedirs(output_dir, exist_ok=True)

response_text = str(response)

# Define the filepath for the text file
txt_file_path = os.path.join(output_dir, "overbite_query_response.txt")

# Save the response in text format
with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response_text)
