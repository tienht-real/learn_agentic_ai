# L1.05 — Tool calling & Agent cơ bản (2.5 tuần)

> JD VN: *"tích hợp API, tool use, function calling, agent orchestration"*, *"LangChain, LangGraph"*, *"thiết kế logic hoạt động của Agent theo workflow thực tế doanh nghiệp (không chỉ chatbot hỏi–đáp)"*.

Mô hình tư duy cốt lõi phải "ngấm" từ phase này:

> **Model không chạy tool.** Model chỉ sinh ra JSON nói "tôi muốn gọi tool X với input Y". Người chạy tool là **bạn** (harness). Bạn nhét kết quả ngược vào hội thoại và gọi API lần nữa. Vòng lặp là nghĩa vụ của bạn — API không tự lặp.

**Vì sao tự viết trước, framework sau:** JD VN ghi LangChain/LangGraph nhiều, nhưng vòng phỏng vấn ở công ty nước ngoài/toàn cầu thường là **take-home "xây một agent"** — có nơi yêu cầu rõ *không dùng LangChain*. Bài 5.1–5.3 chính là bài luyện cho vòng đó; bài 5.4 phủ yêu cầu framework của JD VN.

## Kiến thức cần học

| Mức | Chủ đề |
|---|---|
| 🔴 | Function/tool calling (format OpenAI-compatible): khai báo `tools=[{"type": "function", "function": {name, description, parameters}}]`; response có `message.tool_calls` (mỗi cái có `id`); trả kết quả bằng message `role: "tool"` + `tool_call_id`; nhiều tool call trong một response |
| 🔴 | **Tự viết agent loop**: gọi model → có `tool_calls` thì chạy → append kết quả → lặp đến khi `finish_reason == "stop"`; `max_steps`; lỗi tool → trả thông báo lỗi cho model tự xử lý |
| 🔴 | Thiết kế tool: tên, description, JSON schema input chặt chẽ, validate input (Pydantic), trả lỗi có ích cho model |
| 🟡 | **Workflow vs agent**: luồng cố định (LLM ở từng bước) vs LLM tự quyết bước tiếp — khi nào dùng cái nào |
| 🟡 | Memory ngắn hạn: lịch sử hội thoại, cắt/tóm tắt khi gần đầy context |
| 🟡 | **LangGraph cơ bản**: `StateGraph`, node, edge, conditional edge, prebuilt ReAct agent |
| 🟡 | LangChain: khai báo tool, gắn tool vào chat model |
| 🟢 | MCP (Model Context Protocol): giải quyết vấn đề gì; dùng thử một MCP server có sẵn |
| 🟢 | Multi-agent: orchestrator–worker; CrewAI, AutoGen, OpenAI Agents SDK, Google ADK |
| 🟢 | Low-code: n8n, Dify, Flowise — một số tin "AI automation" ở VN yêu cầu |

> Kiểm tra model trên NVIDIA catalog có hỗ trợ tool calling không (xem trang model trên build.nvidia.com). Nếu không, chọn model khác có hỗ trợ.

**Tài liệu:**
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — đọc kỹ phần workflow vs agent
- [OpenAI — Function calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Academy — Introduction to LangGraph](https://academy.langchain.com/) (miễn phí)
- [modelcontextprotocol.io](https://modelcontextprotocol.io/)

## Bài tập

### Bài 5.1 — Tool-calling loop thủ công (có skeleton: `exercises/ex03_tool_loop.py`)
3 tools: `calculator`, `get_time`, `read_file`. Xử lý: nhiều tool call trong một response, tool lỗi (trả nội dung lỗi cho model), `finish_reason == "length"`, `max_steps` chống lặp vô hạn.
- **Lưu ý:** skeleton được viết cho Anthropic SDK (`tool_use` / `tool_result`). Chuyển sang format OpenAI-compatible (`tool_calls` / `role: "tool"`) dùng `get_client()` — việc chuyển đổi này chính là bài tập hiểu sâu: hai format khác tên nhưng cùng cơ chế.
- **DoD:** hỏi *"Đọc file X, đếm số dòng rồi nhân với 7"* → model chain 2 tools ra đúng kết quả; file không tồn tại → model nhận biết và trả lời hợp lý.

### Bài 5.2 — Tool registry tự sinh schema
Decorator `@tool` sinh JSON schema từ type hints + docstring (hoặc từ một Pydantic model input). Registry có `schemas()` (đưa cho API) và `dispatch(name, args_json) -> str` (validate input, chạy, exception → chuỗi lỗi).
- **DoD:** test cho mapping kiểu (`str→string`, `int→integer`, tham số có default → không required); `dispatch` với input sai trả lỗi rõ ràng thay vì crash.

### Bài 5.3 — Agent nghiệp vụ ⭐
Dùng registry 5.2, agent có 3 tool: (1) `search_docs` — gọi RAG phase 04; (2) một API thật (tỷ giá, thời tiết, hoặc API công khai bất kỳ); (3) `calculate`. System prompt mô tả vai trò và quy tắc dùng tool. In trace từng bước: `→ search_docs(query=...)`, kết quả rút gọn, câu trả lời.
- Câu hỏi mẫu: *"Theo quy chế, nhân viên được nghỉ phép bao nhiêu ngày một năm? Với lương 15 triệu/tháng thì mỗi ngày phép tương đương bao nhiêu tiền?"*
- **DoD:** agent tự chọn đúng tool theo câu hỏi (không gọi RAG cho câu chỉ cần tính toán); tool lỗi/timeout không làm sập agent; lưu phiên thành JSON để xem lại.

### Bài 5.4 — Viết lại bằng LangGraph
Làm lại 5.3 bằng LangGraph (thử cả prebuilt ReAct agent lẫn tự vẽ graph với conditional edge). Thêm một nhánh workflow cố định: nếu câu hỏi thuộc loại "tra cứu chính sách" thì luôn qua RAG trước.
- **DoD:** cùng bộ 10 câu hỏi cho cả bản tự viết và bản LangGraph; `NOTES.md` so sánh: số dòng code, mức kiểm soát, độ dễ debug, chỗ bạn thấy framework tiện/vướng.

### Bài 5.5 — Dùng thử MCP (🟢)
Kết nối một MCP server có sẵn (ví dụ filesystem server) với một client hỗ trợ MCP (Claude Desktop, Claude Code, VS Code…). Gọi được ít nhất 1 tool.
- **DoD:** 5 dòng trong `NOTES.md`: MCP giải quyết vấn đề gì, khác gì việc tự viết tool như bài 5.2. (Tự viết MCP server ở Level 2.)

## Câu hỏi diễn giải

1. Trong tool calling, model có *chạy* tool không? Vì sao thiết kế "model sinh JSON, harness thực thi" lại an toàn và linh hoạt?
2. Vì sao message kết quả tool phải khớp đúng `tool_call_id`? Nếu model gọi 3 tool mà bạn chỉ trả 2 kết quả thì sao?
3. Agent của bạn dừng khi nào? Nếu không có `max_steps` thì kịch bản xấu nhất là gì (cả về kỹ thuật lẫn chi phí)?
4. Vì sao tool lỗi nên trả **chuỗi lỗi cho model đọc** thay vì raise exception làm sập loop?
5. Tool description mơ hồ thì model hỏng theo kiểu nào — gọi sai lúc, sai tham số, hay không gọi? Cho ví dụ từ bài 5.3.
6. Workflow khác agent thế nào? Cho một ví dụ nghiệp vụ nên dùng workflow cố định thay vì agent — vì sao?
7. LangGraph mô hình hoá agent thành graph có state. Được gì và mất gì so với loop tự viết?

> Phần agent harness đầy đủ (coding agent, context management, chấm điểm harness), MCP server, multi-agent nằm ở [Level 2](../../level_2/README.md).
