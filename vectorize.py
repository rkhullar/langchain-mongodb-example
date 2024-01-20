from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config import Settings
from util.mongo import build_atlas_client
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

settings = Settings()
loader = WebBaseLoader('https://en.wikipedia.org/wiki/MongoDB')
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    separators=['\n\n', '\n', '(?<=\. )', ' '],
    length_function=len
)

docs = text_splitter.split_documents(data)
print(docs)

embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
mongo_client = build_atlas_client(atlas_host=settings.atlas_host, local_mode=True)
collection = mongo_client.get_database(settings.database).get_collection(settings.collection)
print(collection)

collection.delete_many({})
docsearch = MongoDBAtlasVectorSearch.from_documents(
    docs, embeddings, collection=collection, index_name=settings.index_name
)

print(docsearch)
