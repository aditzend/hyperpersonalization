from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from tools.openaidirect import system_completion_v1_turbo_t0
from tools.stack import Session
import logging

logger = logging.getLogger("uvicorn")

load_dotenv()

index_name = "conversations"
index_path = "indexes/conversations"
embeddings = OpenAIEmbeddings()
session = Session()


db = FAISS.load_local(
    folder_path=index_path, index_name=index_name, embeddings=embeddings
)


async def chat(user_input: str):
    session.add(
        person_id="1", session_id="1234", role="user", content=user_input
    )
    status = session.get_session("1234")
    logger.debug(f"session: {status}")
    system = await system_completion_v1_turbo_t0(user_input)
    logger.debug(f"system: {system}")
    return system
