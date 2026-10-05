"""Smoke test — xác nhận NVIDIA API key và client hoạt động."""

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Tìm root repo (thư mục chứa pyproject.toml) — chạy đúng dù file nằm sâu bao nhiêu cấp
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())
sys.path.insert(0, str(ROOT))

from shared.client import DEFAULT_MODEL, get_client


def main() -> None:
    client = get_client()
    resp = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "user", "content": "Trả lời đúng 1 từ: Xin chào bằng tiếng Anh là gì?"}],
        max_tokens=512,
    )
    print(resp.choices[0].message.content)
    print(f"usage: {resp.usage.prompt_tokens} in / {resp.usage.completion_tokens} out")


if __name__ == "__main__":
    main()
