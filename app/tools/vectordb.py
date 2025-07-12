from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
import logging
import os
import redis


from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST") or "localhost"
redis_port = os.getenv("REDIS_PORT") or 6379
logger = logging.getLogger("uvicorn")

redis_host = os.getenv("REDIS_HOST") or "localhost"
redis_port = os.getenv("REDIS_PORT") or 6379


def connect_to_redis():
    return redis.Redis(host=redis_host, port=redis_port, db=0)


def check_index_existance(index="main") -> bool:
    redis_conn = connect_to_redis()
    index_key = f"indexes:{index}"
    if redis_conn.get(index_key) is None:
        return False
    else:
        return True


def add_message_to_db(message: str, index: str):
    """Add message to database."""
    index_exists = check_index_existance(index=index)
    # loader = TextLoader(message)
    # message_text = loader.load()

    embeddings = OpenAIEmbeddings()

    if not index_exists:
        index_db = FAISS.from_texts(message, embedding=embeddings)
    else:
        index_db = FAISS.load_local(index=index, embedding=embeddings)
        index_db.add_texts(message)

    index_db.save_local(f"indexes:{index}")
