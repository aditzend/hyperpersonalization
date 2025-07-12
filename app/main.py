from fastapi import FastAPI
from pydantic import BaseModel
import json
import time
import openai
import os
import logging
from tools.chat import chat
from schemas.chat import ChatDto
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("uvicorn")

if os.getenv("LOG_LEVEL") == "DEBUG":
    logger.setLevel(logging.DEBUG)

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


@app.get("/version")
async def version():
    version = {
        "date": "2023-07-03",
        "branch": "hyperpersonalization-by-prompting",
        "version": "0.1.0",
        "comments": (
            "hyperpersonalization done by storing conversation history in"
            " FAISS"
        ),
    }
    print(version)
    return version


@app.post("/v1/chat")
async def get_gpt(request: ChatDto):
    answer = await chat(request.user_input)
    return answer
