# L1.06 — Backend & Deploy (2 tuần)

> JD VN: *"FastAPI"*, *"phát triển backend và API để hỗ trợ tương tác và điều phối giữa các agent"*, *"Docker, Linux, logging"*.

Agent chạy trong terminal chưa phải sản phẩm. Phase này biến nó thành **service** người khác gọi được và chạy được bằng một lệnh.

## Kiến thức cần học

| Mức | Chủ đề |
|---|---|
| 🔴 | **FastAPI**: route, request/response model Pydantic, async endpoint, status code & xử lý lỗi, dependency injection, docs tự sinh `/docs` |
| 🟡 | Streaming response: `StreamingResponse` / Server-Sent Events — UI hiện chữ dần |
| 🟡 | Upload file (`UploadFile`), background task cho việc index tài liệu |
| 🟡 | **Docker**: Dockerfile, image vs container, volume, `docker compose` nhiều service |
| 🟡 | Config & secret qua biến môi trường (`pydantic-settings`); logging có cấu trúc |
| 🟡 | SQL cơ bản + PostgreSQL: lưu user, lịch sử hội thoại |
| 🟡 | Linux cơ bản: shell, xem log, process, port, `curl` |
| 🟡 | **CI với GitHub Actions**: chạy lint + test mỗi khi push/PR |
| 🟢 | UI demo nhanh: Streamlit hoặc Gradio |
| 🟢 | Cloud: AWS / Azure / GCP; dịch vụ LLM managed (Azure OpenAI, AWS Bedrock, GCP Vertex AI) |
| 🟢 | Deploy lên VM hoặc PaaS (Render, Railway, Fly.io…) |

**Tài liệu:** [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) · [Docker — Get started](https://docs.docker.com/get-started/) · [Streamlit — Build a chat app](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps)

## Bài tập

### Bài 6.1 — API cho agent
Bọc agent phase 05 thành FastAPI:
- `POST /chat` — nhận `{session_id, message}`, trả câu trả lời; có biến thể streaming
- `POST /documents` — upload PDF/DOCX, index ở background
- `GET /sessions/{id}` — xem lịch sử hội thoại
- `GET /health`
- **DoD:** request sai schema trả 422 có thông báo rõ; lỗi LLM/tool trả 5xx có message, không lộ stack trace; `/docs` dùng thử được mọi endpoint.

### Bài 6.2 — Lưu trữ
Lịch sử hội thoại lưu PostgreSQL (SQLAlchemy hoặc `psycopg`). Vector store dùng Chroma chế độ server hoặc pgvector.
- **DoD:** restart service, hội thoại cũ vẫn còn.

### Bài 6.3 — Docker Compose
`Dockerfile` cho API + `docker-compose.yml` gồm `api`, `postgres`, vector DB. Secret đọc từ `.env`, có `.env.example`.
- **DoD:** người khác clone repo → `cp .env.example .env` → điền key → `docker compose up` là dùng được.

### Bài 6.4 — UI demo
Streamlit/Gradio gọi API (không gọi thẳng LLM): chat, upload tài liệu, hiển thị trích dẫn nguồn.
- **DoD:** demo được end-to-end trong 2 phút.

### Bài 6.5 — CI
Workflow GitHub Actions: cài dependency bằng `uv`, chạy `ruff check` và `pytest` (test endpoint dùng `TestClient` với LLM được mock — CI không gọi API thật). Build Docker image để chắc Dockerfile không hỏng.
- **DoD:** PR làm hỏng một test → CI đỏ; sửa → CI xanh. Badge CI hiển thị trên README.

## Câu hỏi diễn giải

1. Vì sao endpoint gọi LLM nên là `async def`? Nếu viết `def` thường và gọi client sync thì server xử lý 50 người dùng cùng lúc ra sao?
2. Index tài liệu 100 trang mất 2 phút — vì sao không nên bắt request upload chờ xong? Có những cách nào xử lý?
3. Image khác container thế nào? Vì sao dữ liệu Postgres phải nằm trong volume?
4. Vì sao không được hard-code API key trong code hay Dockerfile? Key nằm ở đâu trong môi trường production?
5. Mô tả một request đi từ UI → API → agent → tool → LLM → quay về UI. Mỗi bước có thể lỗi gì?
6. Vì sao test trong CI nên mock LLM thay vì gọi API thật? Vậy cái gì kiểm tra chất lượng câu trả lời thật? (Gợi ý: phase 07.)
