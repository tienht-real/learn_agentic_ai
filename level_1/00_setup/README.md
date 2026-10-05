# L1.00 — Setup môi trường

## Mục tiêu
Chuẩn bị toolchain cho toàn bộ Level 1: Python hiện đại, Git, Docker, và API key để gọi LLM.

## Cài đặt

### 1. Python với `uv`
```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

uv python install 3.12
```
Dùng `uv` thay cho pip/venv thủ công. Repo có sẵn `pyproject.toml` ở root — chạy `uv sync` để cài dependency chung, `uv add <pkg>` khi cần thêm.

### 2. Git & GitHub
Tạo repo GitHub cho thư mục này, commit từ ngày đầu. Kiểm tra `.gitignore` đã có `.env` — **không bao giờ** commit API key.

### 3. Docker
Cần từ phase 06 (Backend & Deploy). Cài Docker Desktop, kiểm tra: `docker run hello-world`.

### 4. API key
Repo đang dùng **NVIDIA API** (miễn phí ở mức thử nghiệm) qua giao thức **tương thích OpenAI** — xem [`shared/client.py`](../../shared/client.py). Lợi ích: đổi sang OpenAI / Azure OpenAI / Gemini / Ollama chỉ cần đổi `base_url` + key + tên model, code không đổi.

```bash
# .env ở root repo
NVIDIA_API_KEY=nvapi-...
```

Tuỳ chọn (🟢): cài [Ollama](https://ollama.com) để chạy model local — hữu ích khi hết quota hoặc muốn thử model mở.

> Rust (dùng ở Level 3) chưa cần cài.

## Bài tập 0.1 — Smoke test

```bash
uv run python level_1/00_setup/smoke_test.py
```

**DoD:** in ra câu trả lời + số token in/out; `docker run hello-world` chạy được; repo đã push lên GitHub (không có `.env`).
