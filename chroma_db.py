import os

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# memory h2(only for tests)
# client = chromadb.Client()

client = chromadb.PersistentClient(path='chromadb')

embedding_function = OpenAIEmbeddingFunction(api_key=os.environ.get('OPENAI_API_KEY'))
# embedding_function = OpenAIEmbeddingFunction(api_key="1234")
collection = client.get_or_create_collection("word_collection", embedding_function=embedding_function)
