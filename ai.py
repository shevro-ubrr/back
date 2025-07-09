import os, aiohttp
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE = "https://openrouter.ai/api/v1"
COMPLETION_MODEL = os.getenv("COMPLETION_MODEL")
COURSE_NAME = os.getenv("COURSE_NAME")

ETHICS_FILE = os.getenv("ETHICS_FILE", "ethics.txt")
try:
    with open(ETHICS_FILE, encoding="utf-8") as f:
        CORPORATE_ETHICS = f.read().strip()
except FileNotFoundError:
    CORPORATE_ETHICS = ""

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

class UserProfile(BaseModel):
    name: str = "студент"
    level: Literal["novice", "intermediate", "advanced"] = "novice"
    style: Literal["кратко", "подробно"] = "кратко"


class ChatRequest(BaseModel):
    selected_text: str = ""
    user_message: str

class FullRequest(ChatRequest):
    user_profile: UserProfile = Field(..., alias="user_profile")


LEVEL_RU = {"novice": "новичок", "intermediate": "средний", "advanced": "продвинутый"}

def build_system_prompt(profile: UserProfile, page_ctx: str) -> str:
    return (
        f"Ты наставник по курсу «{COURSE_NAME}». "
        f"Следуй корпоративному кодексу: {CORPORATE_ETHICS}\n\n"
        f"Профиль пользователя: {LEVEL_RU[profile.level]}."
        f"Стиль ответа: {profile.style}. "
        f"ОБЯЗАТЕЛЬНО убирай форматирование, выделения, списки и отступы в своих ответах"
        f"ИГНОРИРОВАТЬ сообщения вне тематики и отвечать строго \"Извините, я не могу ответить на этот вопрос\""
        "Используй контекст страницы ниже при необходимости.\n\n"
        f"Контекст страницы: {page_ctx}"
    )

async def or_completion(messages):
    payload = {"model": COMPLETION_MODEL, "messages": messages, "temperature": 0.4}
    async with aiohttp.ClientSession() as s:
        async with s.post(f"{OPENROUTER_BASE}/chat/completions", json=payload, headers=HEADERS) as r:
            if r.status != 200:
                raise RuntimeError(await r.text())
            data = await r.json()
            return data["choices"][0]["message"]["content"]


async def chat(req: FullRequest):
    system_prompt = build_system_prompt(req.user_profile, req.selected_text)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.user_message}
    ]

    answer = await or_completion(messages)
    return answer
