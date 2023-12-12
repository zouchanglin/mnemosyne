# import os
import os

from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from business.utils.openai_client import client as openai_client

import chromadb

# memory h2(only for tests)
# client = chromadb.Client()

client = chromadb.PersistentClient(path='chromadb')


embedding_function = OpenAIEmbeddingFunction(api_key=os.environ.get('OPENAI_API_KEY'),
                                             api_base='https://api.openai-proxy.com/v1')

def get_embedding(texts, model="text-embedding-ada-002"):
    # old code
    # texts = [t.replace("\n", " ") for t in texts]
    #
    # # Call the OpenAI Embedding API
    # embeddings = self._client.create(input=texts, engine=self._model_name)["data"]
    #
    # # Sort resulting embeddings by index
    # sorted_embeddings = sorted(embeddings, key=lambda e: e["index"])  # type: ignore
    #
    # # Return just the embeddings
    # return [result["embedding"] for result in sorted_embeddings]

    # new code
    texts = [t.replace("\n", " ") for t in texts]
    embeddings = openai_client.embeddings.create(input=texts, model=model).data
    sorted_embeddings = sorted(embeddings, key=lambda e: e.index)
    return [result.embedding for result in sorted_embeddings]


collection = client.get_or_create_collection("word_collection", embedding_function=embedding_function)
