"""OpenAI Direct API"""
import os
import requests
from dotenv import load_dotenv
import logging
import json

logger = logging.getLogger("uvicorn")

load_dotenv()
completion_url = os.getenv("COMPLETION_URL")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_version = os.getenv("OPENAI_API_VERSION") or "2023-05-15"
openai_api_base = os.getenv("OPENAI_API_BASE") or "https://api.openai.com"
openai_api_type = os.getenv("OPENAI_API_TYPE")
gpt_35_turbo_16k_deployment = (
    os.getenv("GPT_35_TURBO_16K_DEPLOYMENT") or "GPT35Turbo16k"
)
azure_completion_url_gpt_35_turbo_16k = f"{openai_api_base}/openai/deployments/{gpt_35_turbo_16k_deployment}/chat/completions"
authorization = (
    f"Bearer {openai_api_key}"
    if openai_api_type == "openai"
    else f"{openai_api_key}"
)

openai_headers = {
    "Content-Type": "application/json",
    "Authorization": authorization,
}
azure_headers = {
    "Content-Type": "application/json",
    "api-key": "bd6603c266fc49389659225a451ff03d",
}

headers = openai_headers if openai_api_type == "openai" else azure_headers


async def system_completion_v1_turbo_t0(content: str):
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "messages": [
            {
                "content": content,
                "role": "system",
            }
        ],
    }
    raw = requests.post(completion_url, headers=headers, json=payload)
    response = raw.json()
    response = response["choices"][0]["message"]["content"]
    return response


async def system_user_v1_turbo_t0(system: str, user: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": authorization,
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "messages": [
            {
                "content": system,
                "role": "system",
            },
            {
                "content": user,
                "role": "user",
            },
        ],
    }
    raw = requests.post(completion_url, headers=headers, json=payload)
    response = raw.json()
    response = response["choices"][0]["message"]["content"]
    return response


async def system_user_v1_turbo_t0_full(system: str, user: str):
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 200,
        "messages": [
            {
                "content": system,
                "role": "system",
            },
            {
                "content": user,
                "role": "user",
            },
        ],
    }
    raw = requests.post(completion_url, headers=headers, json=payload)
    response = raw.json()
    content = None
    try:
        content = response["choices"][0]["message"]["content"]
    except KeyError:
        logger.error("The key 'choices' is not present in the response")

    try:
        usage = response["usage"]
    except KeyError:
        logger.error("Usage not present")
    return {
        "content": content,
        "usage": usage,
        # "openai_processing_ms": raw.headers["openai-processing-ms"],
        "openai_processing_ms": 99,
    }


async def markdown_filter(markdown: str):
    payload = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "messages": [
            {
                "content": (
                    "Given a full markdown text that has been obtained from a"
                    " web page, extract the copy and the tables that actually"
                    " talk about products, services, specs and benefits and"
                    " leave out the rest. Give your answer as markdown text."
                    f" \n\nMarkdown text: {markdown}"
                ),
                "role": "system",
            }
        ],
    }
    logger.error("markdown_filter")
    raw = requests.post(completion_url, headers=headers, json=payload)
    response = raw.json()
    logger.error(response)
    response = response["choices"][0]["message"]["content"]
    return response


async def text2markdown(text: str):
    payload = {
        "model": "gpt-3.5-turbo",
    }


def gpt35_system_user(
    system_message: str, user_message: str, openai_api_key: str
):
    """Para usar en notebooks"""
    # Hyper 2
    # POST https://yoizenia.openai.azure.com/openai/deployments/GPT35Turbo/chat/completions

    try:
        response = requests.post(
            url="https://api.openai.com/v1/chat/completions",
            params={
                "temperature": "0",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            data=json.dumps(
                {
                    "messages": [
                        {"content": system_message, "role": "system"},
                        {"content": user_message, "role": "user"},
                    ]
                }
            ),
            timeout=10,
        )
        choices = response.json()["choices"]
        answer = {
            "status_code": response.status_code,
            "text": choices[0]["message"],
        }
        return answer

    except requests.exceptions.RequestException:
        print("HTTP Request failed")
        return None


def azure_gpt35_system_user(system_message: str, user_message: str):
    # Hyper 2
    # POST https://yoizenia.openai.azure.com/openai/deployments/GPT35Turbo/chat/completions

    try:
        response = requests.post(
            url="https://yoizenia.openai.azure.com/openai/deployments/GPT35Turbo/chat/completions",
            params={
                "api-version": "2023-05-15",
                "temperature": "0",
            },
            headers={
                "Content-Type": "application/json",
                "api-key": "bd6603c266fc49389659225a451ff03d",
            },
            data=json.dumps(
                {
                    "messages": [
                        {"content": system_message, "role": "system"},
                        {"content": user_message, "role": "user"},
                    ]
                }
            ),
        )
        choices = response.json()["choices"]
        answer = {
            "status_code": response.status_code,
            "text": choices[0]["message"],
        }
        return answer

    except requests.exceptions.RequestException:
        print("HTTP Request failed")
        return None
