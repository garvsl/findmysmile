'''
This file will use nomic embeddings to embed the crossite.pdf data
'''
import json
import os
import nest_asyncio
nest_asyncio.apply()
from llama_index.embeddings.nomic import NomicEmbedding
from llama_index.core import settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

# Note: SimpleDirectoryReader needs to point to a directory, and it will read whatever file is within that specific directory, don't point it to a file, it will cause an error

#print(os.listdir("/Users/ayandas/Desktop/VS_Code_Projects/findmysmile/scripts/data"))

nomic_api_key = "nk-HIAdG-oqcxQ9TBsYdhQ4ygRsgp-Lr7D_I6Y4Q_eBZP8"
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

nomic_embded_model = NomicEmbedding(
    api_key=nomic_api_key,
    #dimensionality=256,  # play around with this value as needed (768 default)
    model_name="nomic-embed-text-v1.5"  #embedding model version we will be suing
)

llm = OpenAI(model="gpt-4", max_tokens=1000)
settings.llm = llm  #set the llm to openAI
settings.embed_model = nomic_embded_model  #set the embedding model to nomic

#load the data
openbite = SimpleDirectoryReader(input_dir="../data/openbite").load_data() #read the content within the crossbite directory

 # only read one file for one procedure
print(openbite)  # print out the data to see what it looks like raw

#index creation
index = VectorStoreIndex.from_documents(openbite)  # embed the pdf content

#embedding = nomic_embded_model.get_text_embedding("crossbite.pdf")

#query engine
query_engine = index.as_query_engine()
response = query_engine.query("Provide me details pertaining to the openbite dental procedure based on the data you have been provided.")
print("\n\n")  #create some spacings
print("Query Response For Openbite:")
print(response)  # this should cause an error

#save the resulting output in a json format
#response_data = {"response" : response}
output_dir = "../embedding_output"
os.makedirs(output_dir, exist_ok=True)

response_text = str(response)

# Define the filepath for the text file
txt_file_path = os.path.join(output_dir, "Openbite_query_response.txt")

# Save the response in text format
with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response_text)



'''
# define the filepath for json
json_file_path = os.path.join(output_dir, "crossbite_query_response.json")

#save the response in json format
with open(json_file_path, 'w') as json_file:
    json.dump(response_data, json_file, indent=4)
'''