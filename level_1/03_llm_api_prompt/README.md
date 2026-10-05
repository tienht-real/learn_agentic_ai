# L1.03 — LLM API & Prompt Engineering (2 tuần)

> JD VN: *"hiểu về LLM và prompt engineering"*, *"triển khai, đánh giá và tối ưu LLM (gọi API hoặc self-hosted)"*.

Mục tiêu: hiểu LLM API **ở mức request/response thật**, không chỉ mức SDK, và viết prompt có phương pháp — đo được prompt nào tốt hơn thay vì cảm tính.

Repo dùng API **tương thích OpenAI** (Chat Completions) qua [`shared/client.py`](../../shared/client.py). Đây cũng là format phổ biến nhất trong JD VN (OpenAI, Azure OpenAI, vLLM, Ollama đều nói chung format này).

## Kiến thức cần học

| Mức | Chủ đề |
|---|---|
| 🔴 | Token, context window, `temperature`, `top_p`, `max_tokens`, `stop` — ảnh hưởng gì đến output và chi phí |
| 🔴 | `messages`: role `system` / `user` / `assistant`; API **stateless** — hội thoại nhiều lượt nghĩa là gửi lại toàn bộ lịch sử |
| 🔴 | `finish_reason`: `stop`, `length`, `tool_calls`, `content_filter` — code phải xử lý đủ, không chỉ happy path |
| 🔴 | Prompt engineering: chỉ dẫn rõ ràng & cụ thể, vai trò, few-shot, phân tách bằng delimiter/XML tag, yêu cầu suy luận từng bước, ràng buộc định dạng output |
| 🔴 | **Structured output**: JSON → validate bằng Pydantic → retry khi sai |
| 🟡 | Streaming (SSE): `data: {...}` từng chunk, `delta.content`, kết thúc bằng `data: [DONE]` |
| 🟡 | Trường `usage`, ước tính chi phí; 429/5xx → retry + backoff (dùng lại bài 1.1) |
| 🟡 | Hallucination: vì sao xảy ra, giảm bằng cách nào |
| 🟢 | Provider: OpenAI, Anthropic Claude, Google Gemini, model mở (Llama, Qwen, …); model hỗ trợ tiếng Việt tốt |
| 🟢 | `response_format` / JSON schema ở tầng API — tuỳ provider/model có hỗ trợ hay không |
| 🟢 | Prompt caching, Batch API — giảm chi phí ở scale (đào sâu ở Level 2) |

**Tài liệu:**
- [OpenAI — Text generation](https://platform.openai.com/docs/guides/text) & [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic — Prompt engineering overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — nguyên tắc dùng được cho mọi model
- [NVIDIA API catalog](https://build.nvidia.com) — danh sách model đang dùng được với key của bạn

## Bài tập

### Bài 3.1 — Gọi API bằng HTTP thuần (không SDK)
Dùng `httpx` gọi thẳng `POST {base_url}/chat/completions` với header `Authorization: Bearer <key>`. Sau đó bật `"stream": true` và **tự parse SSE**: đọc từng dòng `data: ...`, decode JSON, ghép `choices[0].delta.content`, dừng ở `[DONE]`.
- **DoD:** in được text hoàn chỉnh từ stream tự parse; `NOTES.md` mô tả một chunk trông thế nào và `finish_reason` xuất hiện ở chunk nào.

### Bài 3.2 — CLI chat streaming đa lượt
Dùng SDK `openai` + `get_client()`: chat CLI giữ lịch sử hội thoại, stream token ra màn hình, lệnh `/cost` in tổng token đã dùng trong phiên (gợi ý: `stream_options={"include_usage": True}` để nhận `usage` khi stream — kiểm tra provider có hỗ trợ không).
- **DoD:** hội thoại 5+ lượt vẫn nhớ ngữ cảnh; `/cost` khớp usage cộng dồn; thoát rồi mở lại vẫn còn lịch sử (lưu file JSON).

### Bài 3.3 — So sánh prompt có đo lường ⭐
Trích xuất 10 đoạn văn bản tiếng Việt (hoá đơn/đơn hàng tự soạn, có vài đoạn khó: thiếu trường, viết tắt, số tiền dạng "1tr2") vào model `Invoice` của bài 1.3. Viết 3 phiên bản prompt: (a) zero-shot, (b) few-shot 2 ví dụ, (c) few-shot + XML tag phân tách + hướng dẫn xử lý trường thiếu.
- **DoD:** bảng 3 prompt × 10 mẫu (đúng/sai từng trường); có retry khi JSON không hợp lệ hoặc validate fail (gửi lỗi Pydantic ngược lại cho model sửa); `NOTES.md` kết luận prompt nào thắng và **vì sao**.

### Bài 3.4 — Structured output: API vs prompt
Nếu model/provider của bạn hỗ trợ `response_format` (JSON schema), làm lại bài 3.3 bằng cách đó và đếm tỉ lệ parse fail so với cách "xin JSON trong prompt rồi `json.loads`". Nếu không hỗ trợ, thử với một provider khác (Ollama local cũng được) — hoặc ghi lại vì sao không làm được.
- **DoD:** số liệu so sánh trong `NOTES.md`.

### Bài 3.5 — Usage tracker
Class `UsageTracker` bọc quanh client: mỗi lần gọi API tự ghi `{timestamp, model, prompt_tokens, completion_tokens, latency_ms}` vào SQLite. Cuối phiên in báo cáo theo model.
- **DoD:** wrapper **không đổi hành vi** — code dùng client như bình thường vẫn chạy y hệt. Tracker này dùng lại ở phase 07 và capstone.

### Nâng cao (tuỳ chọn)
- Chạy cùng prompt bài 3.3 trên 2–3 model khác nhau (đổi tên model trong NVIDIA catalog, hoặc Ollama). So sánh độ chính xác, latency, chi phí ước tính.
- Thử `temperature` 0 / 0.7 / 1.2 trên cùng một prompt sáng tạo, chạy 5 lần mỗi mức, nhận xét độ đa dạng.

## Câu hỏi diễn giải

1. API là **stateless** — mỗi request gửi lại toàn bộ lịch sử. Vì sao provider thiết kế vậy? Hệ quả gì với chi phí khi hội thoại dài?
2. `temperature` cao/thấp dùng cho loại tác vụ nào? Trích xuất dữ liệu nên đặt bao nhiêu — vì sao?
3. Vì sao output dài mà không stream dễ bị timeout, và UX tệ? Streaming có làm tổng thời gian nhanh hơn không?
4. `finish_reason == "length"` nghĩa là gì và code của bạn phải xử lý thế nào? Vì sao chỉ xử lý `stop` là bug tiềm ẩn?
5. Few-shot thắng zero-shot ở bài 3.3 vì cơ chế gì? Khi nào few-shot lại phản tác dụng?
6. Vì sao structured output ở tầng API đáng tin hơn "xin JSON trong prompt"? Vẫn có trường hợp nào output đúng schema nhưng sai nội dung?
7. Kể 3 cách giảm hallucination bạn có thể áp dụng ngay ở tầng prompt.
