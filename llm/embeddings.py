import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
import os
from llama_index.readers.json import JSONReader
import openai
from dotenv import load_dotenv
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import getpass, os, pymongo, pprint
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, ExactMatchFilter, FilterOperator
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch


# Load your API key from an environment variable or .env file
load_dotenv()
def create_or_load_index():
    try:
        mongo_uri = "mongodb+srv://garv:dbuserpass123$$$123asd@cluster0.h9u4qgi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = pymongo.MongoClient(mongo_uri)
        print("Connection to MongoDB successful")

        # Use the default database and collection names
        DB_NAME = "default_db"
        COLLECTION_NAME = "default_collection"

        if "index" in client[DB_NAME].list_collection_names():
            print("Index already exists, loading...")
            store = MongoDBAtlasVectorSearch(client, db_name=DB_NAME, collection_name=COLLECTION_NAME, index_name="vector_index")
            storage_context = StorageContext.from_defaults(vector_store=store)
            return VectorStoreIndex.from_existing(storage_context=storage_context)
        
        store = MongoDBAtlasVectorSearch(client, db_name=DB_NAME, collection_name=COLLECTION_NAME, index_name="vector_index")
        storage_context = StorageContext.from_defaults(vector_store=store)
        
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

        index = VectorStoreIndex.from_documents(
            docs + docs2 + docs3 + docs4 + docs5 + docs6 + docs7 + docs8 + docs9, storage_context=storage_context
        )
        
        print("Index created successfully")
        return index

    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None

openai.api_key = os.getenv('OPENAI_API_KEY')

def classify_and_elaborate_prompt(prompt):
    """
    Classifies the given prompt into one of four categories and provides an extended response.
    
    Parameters:
    - prompt: A string containing the user's prompt.
    
    Returns:
    - A string with the classification and an extended response.
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI()

        # Template for the system message to guide the AI's response
        system_message = "Classify the following prompt into one of these categories: Urgency, Anxiety/concern, Inquiry, Satisfaction/Dissatisfaction. Then, provide an extended response related to the prompt and its classification. Note that this does not mean you are to provide advice but rather reformat the prompt so that in one line you specify the sentiment of the prompt and then in the next line, you rewrite the prompt in an extended manner, but don't offer medical advice, simply expand upon the prompt since this prompt will be fed onto another model."

        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-4",  # Use the GPT-4 model
            max_tokens=3000,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ]
        )

        return response.choices[0].message.content  #note that this is the right syntax for the response (should have just looked at the documentation)

    except Exception as e:
        return str(e)

# Example usage
user_prompt = "I'm really worried about my toothache, what should I do?"
result = classify_and_elaborate_prompt(user_prompt)
print(result)

# save the resulting output:
# output_dir = "../sentiment-analysis-output"
# os.makedirs(output_dir, exist_ok=True)

# response_text = str(result)

# Define the filepath for the text file
# txt_file_path = os.path.join(output_dir, "Sentiment_And_Extended_Output.txt")

# # Save the response in text format
# with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
#     txt_file.write(response_text)

index = create_or_load_index()


if index is not None:
    # Use the HuggingFaceEmbedding model to get text embeddings for the result
# Use the HuggingFaceEmbedding model to get text embeddings for the result
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embeddings = embed_model.get_text_embedding(result)[0]

    # Convert embeddings to numpy array if it's not already
    if not isinstance(embeddings, np.ndarray):
        embeddings = np.array(embeddings)

    # Query the index with the embeddings
    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query(embeddings)

    # Display the response
    for result in response:
        print(result)






