"""Shared NVIDIA API client dùng cho tất cả bài tập."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load .env từ root repo (2 cấp trên shared/)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"
BASE_URL = "https://integrate.api.nvidia.com/v1"


def get_client() -> OpenAI:
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY chưa được set. Thêm vào .env hoặc export trong shell.")
    return OpenAI(base_url=BASE_URL, api_key=api_key)
