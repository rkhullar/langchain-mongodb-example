import warnings
from dataclasses import dataclass, field

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAI, OpenAIEmbeddings

from util.mongo import build_atlas_client

warnings.filterwarnings('ignore', category=UserWarning, module='langchain.chains.llm')


@dataclass
class SearchClient:
    atlas_host: str = field(repr=False)
    openai_api_key: str = field(repr=False)
    database_name: str
    collection_name: str
    index_name: str

    def __post_init__(self):
        self.mongo_client = build_atlas_client(atlas_host=self.atlas_host)
        self.collection = self.mongo_client.get_database(self.database_name).get_collection(self.collection_name)
        self.vector_store = self.build_vector_store()
        self.compression_retriever = self.build_compression_retriever(self.vector_store)

    def build_vector_store(self):
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        return MongoDBAtlasVectorSearch(self.collection, embeddings, index_name=self.index_name)

    def build_compression_retriever(self, vector_store):
        llm = OpenAI(openai_api_key=self.openai_api_key, temperature=0)
        compressor = LLMChainExtractor.from_llm(llm)
        return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=vector_store.as_retriever())

    def query1(self, text: str) -> tuple[str, str]:
        docs = self.vector_store.max_marginal_relevance_search(text, K=1)
        return docs[0].metadata['title'], docs[0].page_content

    def query2(self, text: str) -> tuple[str, str]:
        compressed_docs = self.compression_retriever.get_relevant_documents(text)
        return compressed_docs[0].metadata['title'], compressed_docs[0].page_content
