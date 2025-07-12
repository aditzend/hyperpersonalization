import redis
from dotenv import load_dotenv
import logging
import os

logger = logging.getLogger("uvicorn")


load_dotenv()

redis_host = os.getenv("REDIS_HOST") or "localhost"
redis_port = os.getenv("REDIS_PORT") or 6379


class Session:
    def __init__(self, host=redis_host, port=redis_port, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def add(self, person_id: str, session_id: str, role: str, content: str):
        message = {
            "role": role,
            "content": content,
        }
        self.redis_client.json().set("person:1", "$", message)

    def get(self, session_id):
        return self.redis_client.json().get("person:1")
