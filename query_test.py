from config import Settings
from query import SearchClient

settings = Settings()
search_client = SearchClient(
    atlas_host=settings.atlas_host,
    openai_api_key=settings.openai_api_key,
    database_name=settings.database,
    collection_name=settings.collection,
    index_name=settings.index_name
)

# print(search_client)
title, content = search_client.query2('how big is mongodb?')
# print(title)
print(content)
