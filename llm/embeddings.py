import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.core import SimpleDirectoryReader
import os
from llama_index.readers.json import JSONReader

def create_or_load_index():
    try:
        mongo_uri = os.environ["MONGO_URI"]
        client = pymongo.MongoClient(mongo_uri)
        print("Connection to MongoDB successful")
        
        if "index" in client.list_database_names():
            print("Index already exists, loading...")
            store = MongoDBAtlasVectorSearch(client)
            storage_context = StorageContext.from_defaults(vector_store=store)
            return VectorStoreIndex.from_existing(storage_context=storage_context)
        
        store = MongoDBAtlasVectorSearch(client)
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

index = create_or_load_index()

# if index is not None:
    #  prompt = input("Enter your query: ")
    # query_vector = get_query_vector(model, prompt) //Place holder for semantic vector
    # results = index.query(query_vector, k=5)

    # for result in results:
    #     print(result)




