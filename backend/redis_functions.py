from langchain_community.vectorstores.redis import Redis
from langchain_community.embeddings.cloudflare_workersai import (
    CloudflareWorkersAIEmbeddings,
)
import os
import dotenv

dotenv.load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]
CLOUDFLARE_API_KEY = os.environ['CLOUDFLARE_API_KEY']
CLOUDFLARE_ACCOUNT_ID = os.environ["CLOUDFLARE_ACCOUNT_ID"]
embeddings = CloudflareWorkersAIEmbeddings(
    account_id=CLOUDFLARE_ACCOUNT_ID,
    api_token=CLOUDFLARE_API_KEY,
    model_name="@cf/baai/bge-small-en-v1.5",
)


def initialize_database(index: str):
    """
    Initializes the Redis database with sample texts and metadata.

    :param index: The name of the index to be created in the Redis database.
    :return: The initialized Redis database object.
    """
    texts = [
        "MUNCHY DMBEL",
        "LIPTON"
    ]
    metadata = [
        {
            "description": "MUNCHY DMBEL",
            "merchant_name": "Walmart",
            "transaction_date": "2017-07-28",
        },
        {
            "description": "LIPTON",
            "merchant_name": "Walmart",
            "transaction_date": "2017-07-28",
        }
    ]

    rds = Redis.from_texts(
        texts,
        embeddings,
        metadatas=metadata,
        redis_url=REDIS_URL,
        index_name=index,
    )
    rds.write_schema("redis_schema.yaml")
    return rds


def existing_database(index: str):
    """
    Create a Redis database object from an existing index.

    :param index: The name of the index to use.
    :return: The Redis database object.
    """
    rds = Redis.from_existing_index(
        embeddings,
        index_name=index,
        redis_url=REDIS_URL,
        schema="redis_schema.yaml",
    )
    return rds


def similarity_search(rds, query: str):
    """
    Perform a similarity search with a given query.

    :param rds: The Redis instance to perform the search on.
    :param query: The query string to search for.
    :return: The results of the similarity search.
    """
    results = rds.similarity_search_with_score(query)
    return results


def add_vectors(rds, document: list, metadata: list):
    """
    Add vectors to Redis.

    :param rds: Redis connection object.
    :param document: List of vectors representing the document.
    :param metadata: List of metadata associated with the document.
    :return: None
    """
    rds.add_texts(document, metadata)
    return None


if __name__ == "__main__":
    user_id = "1"
    initialize_database(user_id)
