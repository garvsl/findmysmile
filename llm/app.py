import getpass, os, pymongo, pprint
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.settings import Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, ExactMatchFilter, FilterOperator
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.readers.json import JSONReader

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
ATLAS_CONNECTION_STRING = getpass.getpass("MongoDB Atlas SRV Connection String:")

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

response = query_engine.query('How can I make my teeth straight?')

print(response)
print("\nSource documents: ")
pprint.pprint(response.source_nodes)