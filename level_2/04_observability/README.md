# 05 — Observability: OpenTelemetry & Tracing cho Agent

> 📍 **Level 2 / 04.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Instrumenting third-party frameworks without changing user-visible behavior. Knowledge of OpenTelemetry, tracing, structured events, exporters, or observability pipelines are a plus."*

Đây là một trong hai mục "ways to stand out" kỹ thuật nhất của JD (cùng với Rust). Mục tiêu: instrument agent của module 03 bằng OpenTelemetry chuẩn chỉnh, rồi tiến tới kỹ năng khó hơn — instrument **thư viện của người khác** mà không sửa code họ, không đổi hành vi.

## Kiến thức cần học

1. **OTel concepts** — trace / span / span attributes / events / status; context propagation (nhớ lại `contextvars` bài 1.5 — OTel Python dùng đúng cơ chế đó); TracerProvider, Processor, Exporter.
2. **OTel Python SDK** — `tracer.start_as_current_span`, span tự nest theo context; batch vs simple processor; OTLP exporter.
3. **GenAI semantic conventions** — chuẩn đặt tên attribute cho LLM: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`… (đọc trong OTel semconv repo). Dùng chuẩn thay vì tự bịa tên.
4. **Kỹ thuật instrument không xâm lấn** — wrapper class, monkey-patching (`wrapt`), vì sao patch phải giữ nguyên signature/return/exception để "không đổi hành vi người dùng thấy".
5. **Structured events** — log dạng JSON có schema, phân biệt với span khi nào dùng cái nào.

**Tài liệu:** OpenTelemetry Python docs; repo `openinference` hoặc `opentelemetry-instrumentation-*` (xem cách người ta instrument thư viện bên thứ ba).

## Bài tập

### Bài 5.1 — Instrument mini_agent bằng OTel
Thêm vào agent module 03: 1 root span cho mỗi phiên, con là span mỗi turn, con nữa là span mỗi LLM request và mỗi tool call. Attributes theo GenAI semconv: model, input/output tokens, stop_reason, tool name, tool duration, cost.
- **DoD:** console exporter in ra cây span đúng cấp bậc (session > turn > llm_call/tool_call); tokens và cost xuất hiện trong attributes; span tool lỗi có status ERROR + exception được record.

### Bài 5.2 — Jaeger
Chạy Jaeger bằng docker (`jaegertracing/all-in-one`), đổi sang OTLP exporter, chạy một phiên agent dài, mở UI xem trace.
- **DoD:** screenshot trace trong Jaeger lưu vào `NOTES.md`; chỉ ra được từ waterfall: bước nào tốn thời gian nhất, LLM call chiếm bao nhiêu % tổng thời gian (đây là kỹ năng "benchmark agents to identify bottlenecks" trong JD).

### Bài 5.3 — `@traced` decorator + context propagation qua async
Viết decorator `@traced` (nhận tên span + extractor attributes) dùng được cho cả hàm sync lẫn async. Chứng minh context propagate đúng qua `asyncio.gather` (các tool call song song đều là con của đúng turn span).
- **DoD:** test khẳng định cây span đúng khi 3 tool chạy song song; decorator không nuốt exception, không đổi return value, giữ nguyên `functools.wraps`.

### Bài 5.4 — Instrument SDK bên thứ ba không sửa code ⭐
Viết package `instrument_anthropic`: gọi `instrument_anthropic.install()` một lần là **mọi** lời gọi `client.messages.create` / `messages.stream` trong process (kể cả từ code không phải của bạn) tự sinh span + structured event — bằng monkey-patching. Yêu cầu khắt khe: giữ nguyên signature, return value, exception, hỗ trợ cả sync lẫn async client, và có `uninstall()`.
- **DoD:** chạy lại nguyên xi code bài 2.2 (không sửa 1 dòng) sau khi `install()` → trace xuất hiện đầy đủ; test chứng minh behavior không đổi (cùng input → cùng output, exception vẫn ném ra đúng loại); streaming vẫn stream bình thường (span kết thúc khi stream đóng, không phải khi hàm return).

### Bài 5.5 — Structured event log song song với spans
Thêm kênh event JSON-lines (`events.jsonl`): mỗi tool call / llm call ghi một event có schema cố định (`event_type`, `trace_id`, `span_id`, `timestamp`, payload). `trace_id` phải khớp với span tương ứng để đối chiếu chéo được.
- **DoD:** từ một `trace_id` trong Jaeger tra ngược ra được các event JSON của đúng phiên đó; viết script nhỏ tổng hợp events → bảng "tool nào được gọi nhiều nhất, tỉ lệ lỗi bao nhiêu".

### Nâng cao (tùy chọn)
- Viết custom SpanExporter ghi vào SQLite + trang HTML tĩnh hiển thị timeline — hiểu exporter interface từ bên trong.
- Instrument thêm LangGraph agent (bài 4.1) bằng đúng package của bạn → bạn vừa có "instrument nhiều framework", điểm cộng lớn khi phỏng vấn.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. Span khác log line ở chỗ nào? Vì sao "có duration + có quan hệ cha-con" lại thay đổi hẳn loại câu hỏi bạn trả lời được (so sánh: tìm bottleneck bằng grep log vs nhìn waterfall)?
2. Context propagation: khi bạn gọi `start_as_current_span` trong một hàm, span con sinh ra ở hàm khác **tự biết** cha nó là ai — cơ chế nào làm được điều đó trong Python? (Bạn đã xây thủ công thứ này ở bài 1.5 — nối hai thứ lại.)
3. Vì sao 3 tool calls chạy song song bằng `gather` vẫn nhận đúng cha là turn span, không lẫn sang turn khác? Nếu OTel dùng biến global thay vì contextvars thì hỏng thế nào?
4. "Instrument mà không đổi hành vi người dùng thấy" — liệt kê cụ thể những thứ **phải giữ nguyên** khi monkey-patch (signature? return? exception type? timing của stream?). Ở bài 5.4, case nào khó nhất — vì sao streaming đặc biệt rắc rối (span kết thúc khi nào)?
5. Vì sao production dùng BatchSpanProcessor chứ không phải SimpleSpanProcessor? Trade-off là gì (mất span khi crash? latency?)?
6. Semantic conventions (`gen_ai.*`): tại sao đặt tên attribute theo chuẩn chung quan trọng đến thế với một **thư viện** (nghĩ về dashboard, về việc trace của bạn nằm cạnh trace của thư viện khác)?
7. Span vs structured event (bài 5.5): cùng một tool call ghi cả hai — mỗi bên trả lời loại câu hỏi gì mà bên kia dở? Khi nào chỉ cần một trong hai?
8. Nếu ai đó `install()` package của bạn hai lần, hoặc quên `uninstall()` trong test — chuyện gì xảy ra và bạn thiết kế chống đỡ thế nào? (Idempotency — câu hỏi phỏng vấn kinh điển cho instrumentation.)
