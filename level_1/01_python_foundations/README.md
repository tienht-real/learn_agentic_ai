# L1.01 — Python cho AI Engineer (2 tuần)

> JD VN: *"Thành thạo Python (xử lý dữ liệu, logic sạch, gọi API/JSON)"*, *"nền tảng cấu trúc dữ liệu & giải thuật vững"*.

Mọi thứ phía sau (gọi LLM, RAG, agent, FastAPI) đều là Python + Pydantic + async. Phase này không dạy Python từ số 0 — nó lấp đúng những mảng AI Engineer dùng hằng ngày.

## Kiến thức cần học

| Mức | Chủ đề |
|---|---|
| 🔴 | Python core: function, class, `dataclass`, type hints, exception, module/package, comprehension |
| 🔴 | **Pydantic**: `BaseModel`, validate, `field_validator`, `model_validator`, `model_dump_json`, `model_json_schema()` — là nền của structured output, tool schema, FastAPI |
| 🟡 | async/await: coroutine, `gather`, `Semaphore`, `asyncio.timeout`, `Queue` — đủ để gọi nhiều LLM request song song |
| 🟡 | `httpx`, JSON, `pathlib`, `logging` |
| 🟡 | Git: branch, commit, PR, tự review diff trước khi merge, `.gitignore` |
| 🟡 | `pytest`: test function, fixture, `parametrize` — công ty nước ngoài/toàn cầu coi test là mặc định |
| 🟡 | Cấu trúc dữ liệu & giải thuật cơ bản (big tech và một số công ty VN có vòng test thuật toán) |
| 🟢 | Type checker (`mypy` / `pyright`), linter (`ruff`) |
| 🟢 | `uv`, virtualenv, `pyproject.toml` |

**Tài liệu:** [Python Tutorial](https://docs.python.org/3/tutorial/) · [asyncio — Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) · [Pydantic docs](https://docs.pydantic.dev/)

## Bài tập

### Bài 1.1 — Concurrent fetcher (có skeleton: `exercises/ex01_concurrent_fetcher.py`, bài làm: `exercises/ex01_student.py`)
Tải N URL đồng thời với: giới hạn concurrency (Semaphore), timeout mỗi request, retry + exponential backoff + jitter khi lỗi mạng/5xx.
- **DoD:** tải 50 URL với max 10 concurrent; in tổng thời gian so với chạy tuần tự; một URL hỏng không làm sập cả batch; kết quả giữ đúng thứ tự input.
- Đây chính là pattern bạn sẽ dùng khi gọi LLM hàng loạt (embed 1000 chunk, chạy eval 100 câu) mà không bị rate limit.

### Bài 1.2 — Producer/consumer với backpressure
Pipeline 3 giai đoạn: `producer → transformer (xN worker) → writer`, nối bằng `asyncio.Queue(maxsize=...)`. Producer nhanh, writer chậm — quan sát backpressure. Hỗ trợ dừng sạch: gửi tín hiệu dừng, chờ queue cạn, huỷ worker.
- **DoD:** xử lý 1000 item không mất item nào; log cho thấy producer bị chặn khi queue đầy.
- Liên hệ: pipeline "đọc tài liệu → chunk → embed → lưu vector DB" ở phase 04 có đúng hình dạng này.

### Bài 1.3 — Pydantic: model hoá đơn
Viết model `Invoice` (số HĐ, ngày, người bán, danh sách `LineItem{tên, số lượng, đơn giá}`, tổng tiền). Validate: tổng tiền = tổng các dòng; ngày đúng định dạng; số lượng > 0. In `Invoice.model_json_schema()` và đọc hiểu nó.
- **DoD:** 5 test `pytest` pass (2 hợp lệ, 3 không hợp lệ với lỗi rõ ràng). Model này sẽ được dùng lại ở phase 03 (trích xuất hoá đơn bằng LLM).

### Bài 1.4 — Luyện giải thuật (duy trì suốt Level 1)
Mỗi tuần 3–5 bài LeetCode Easy/Medium: array, hash map, string, two pointers, stack/queue, BFS/DFS cơ bản.
- **DoD:** ghi lại trong `NOTES.md` số bài đã làm mỗi tuần.

## Câu hỏi diễn giải (tự trả lời được trước khi rời phase)

1. asyncio chạy trên **một thread** — vậy tại sao 50 request vẫn "chạy cùng lúc"? Điều gì xảy ra tại mỗi `await`? Vì sao `time.sleep(1)` trong coroutine là bug còn `await asyncio.sleep(1)` thì không?
2. Concurrency (asyncio) khác parallelism (threads/processes) chỗ nào? Task CPU-bound thì asyncio có giúp được không — vì sao?
3. `Semaphore` khác `Lock` thế nào — vì sao bài 1.1 dùng Semaphore?
4. Backpressure là gì? Nếu `Queue` ở bài 1.2 không có `maxsize`, chuyện gì xảy ra khi producer nhanh hơn writer 100 lần?
5. Vì sao bài 1.1 trả "kết quả lỗi" như một giá trị thay vì raise exception?
6. Pydantic validate ở đâu, khi nào? `model_json_schema()` liên quan gì đến việc khai báo tool cho LLM?

> Phần async nâng cao (event bus, middleware chain, `contextvars`) nằm ở [Level 2 — 01_async_advanced](../../level_2/01_async_advanced/README.md).
