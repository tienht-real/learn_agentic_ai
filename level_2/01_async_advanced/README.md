# 01 — Async Python & Event-Driven Systems

> 📍 **Level 2 / 01.** Bài 1.1 (concurrent fetcher) và 1.3 (producer/consumer) đã chuyển sang [Level 1 / 01](../../level_1/01_python_foundations/README.md) — ở Level 2 học **bài 1.2, 1.4, 1.5** và các câu hỏi diễn giải 3, 4, 7, 8. Số module cũ trong bài → tra [bảng ở Level 2](../README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Solid understanding of asynchronous programming, callbacks, request lifecycles, and event-driven systems."*

Đây là nền móng. Toàn bộ agent harness, tracing, middleware ở các module sau đều là code async. Mục tiêu không phải "biết dùng `async/await`" mà là **hiểu event loop hoạt động thế nào** — đủ để debug được deadlock, task bị nuốt exception, hay cancellation không lan truyền.

## Kiến thức cần học

1. **Event loop & coroutines** — coroutine khác function thường thế nào; `await` nhường quyền điều khiển ra sao; sự khác nhau giữa concurrency (asyncio) và parallelism (threads/processes).
2. **Task lifecycle** — `asyncio.create_task`, `gather` vs `TaskGroup` (3.11+), exception trong task bị nuốt khi nào, tại sao phải giữ reference đến task.
3. **Cancellation & timeout** — `asyncio.timeout()`, `CancelledError` lan truyền thế nào, cleanup với `finally`, shielding.
4. **Đồng bộ hoá** — `Lock`, `Semaphore`, `Event`, `Queue`; backpressure là gì và vì sao quan trọng.
5. **Callbacks vs coroutines** — `loop.call_soon`, future callbacks; cầu nối code callback-style (thư viện cũ) sang async.
6. **`contextvars`** — cách truyền context xuyên qua async calls mà không truyền tham số. *Cực kỳ quan trọng*: đây chính là cơ chế OpenTelemetry propagate trace context (module 05).

**Tài liệu:** asyncio docs chính thức (đọc kỹ "Coroutines and Tasks" + "Streams"); bài "How the heck does async/await work in Python" của Brett Cannon; source của `asyncio.TaskGroup`.

## Bài tập

### Bài 1.1 — Concurrent fetcher (có skeleton: `exercises/ex01_concurrent_fetcher.py`)
Viết hàm tải N URL đồng thời với: giới hạn concurrency (Semaphore), timeout mỗi request, retry + exponential backoff + jitter khi lỗi mạng/5xx.
- **DoD:** tải 50 URL với max 10 concurrent; in tổng thời gian so với chạy tuần tự; một URL hỏng không làm sập cả batch; kết quả trả về giữ đúng thứ tự input.

### Bài 1.2 — Async Event Bus
Viết class `EventBus` pub/sub: `subscribe(pattern, handler)`, `emit(event_name, payload)`, hỗ trợ wildcard (`"agent.*"`), handler async lẫn sync, và **error isolation** (một handler ném exception không ảnh hưởng handler khác — exception được log, không nuốt im lặng).
- **DoD:** test chứng minh: 2 handler cùng nhận 1 event; wildcard match đúng; handler lỗi không chặn handler khác; `unsubscribe` hoạt động.

### Bài 1.3 — Pipeline producer/consumer với backpressure
Xây pipeline 3 giai đoạn: `producer → transformer (xN worker) → writer`, nối bằng `asyncio.Queue` có `maxsize`. Producer nhanh, writer chậm — quan sát backpressure. Hỗ trợ graceful shutdown: gửi tín hiệu dừng, chờ queue cạn, hủy worker sạch sẽ.
- **DoD:** xử lý 1000 item không mất item nào; Ctrl+C shutdown sạch (không traceback rác); log cho thấy producer bị chặn khi queue đầy.

### Bài 1.4 — Request lifecycle với middleware chain ⭐
Mô phỏng lifecycle của một request qua chuỗi middleware — pattern y hệt ASGI/Starlette và cũng là pattern module 09 sẽ dùng cho agent:

```python
async def logging_mw(request, call_next):
    print("before", request)
    response = await call_next(request)
    print("after", response)
    return response
```

Viết `Pipeline` nhận list middleware + handler cuối, compose thành 1 callable. Middleware phải có thể: sửa request, sửa response, chặn request (không gọi `call_next`), bắt exception từ tầng dưới.
- **DoD:** test với 3 middleware chứng minh thứ tự chạy đúng (onion model: A-before → B-before → handler → B-after → A-after); middleware chặn được request; middleware bắt được exception của handler.

### Bài 1.5 — Truyền context với `contextvars`
Thêm vào bài 1.4: mỗi request được gán `request_id` bằng `contextvars.ContextVar`, mọi hàm ở mọi độ sâu (kể cả trong `asyncio.gather` con) log ra đúng `request_id` của request mình mà **không nhận nó qua tham số**.
- **DoD:** chạy 10 request đồng thời, log không bao giờ lẫn request_id giữa các request.

### Nâng cao (tùy chọn)
- Viết một event loop tối giản chỉ bằng generator (`send`/`yield`) chạy được 2 "coroutine" xen kẽ — hiểu tận gốc cơ chế.
- Benchmark asyncio vs `uvloop` cho bài 1.1, ghi số liệu vào `NOTES.md`.

## Đọc source
- `asyncio/taskgroups.py` trong CPython — cách TaskGroup xử lý exception + cancellation.
- Source `starlette/middleware/base.py` — so với bài 1.4 của bạn.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. asyncio chạy trên **một thread** — vậy tại sao 50 request vẫn "chạy cùng lúc" được? Điều gì thực sự xảy ra tại mỗi từ khóa `await`? (Gợi ý kiểm chứng: vì sao `time.sleep(1)` trong coroutine là bug còn `await asyncio.sleep(1)` thì không?)
2. Concurrency (asyncio) khác parallelism (threads/processes) chỗ nào? Task CPU-bound thì asyncio giúp được gì không — vì sao?
3. Tại sao phải giữ reference đến task tạo bởi `create_task`? Exception xảy ra trong một task không ai `await` sẽ đi đâu?
4. Khi một task bị cancel, `CancelledError` được "ném vào" ở đâu trong coroutine? Vì sao khối `finally` vẫn chạy, và vì sao điều đó quan trọng với việc đóng connection/file?
5. Backpressure là gì? Giải thích bằng chính pipeline bài 1.3: nếu `Queue` không có `maxsize`, chuyện gì xảy ra khi producer nhanh hơn writer 100 lần?
6. `Semaphore` giới hạn concurrency bằng cơ chế gì bên trong? Nó khác `Lock` thế nào — vì sao bài 1.1 dùng Semaphore chứ không phải Lock?
7. Vì sao `contextvars` giữ đúng giá trị xuyên qua `await` và qua các task con, còn `threading.local` thì không? (Đây là nền của OpenTelemetry ở module 05 — trả lời được câu này thì module 05 sẽ nhẹ nhàng.)
8. Mô hình "onion" của middleware (bài 1.4): vì sao phần *after* chạy **ngược** thứ tự phần *before*? Điều đó là hệ quả tự nhiên của cái gì trong cách compose hàm?
