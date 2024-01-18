from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from config import Settings

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


