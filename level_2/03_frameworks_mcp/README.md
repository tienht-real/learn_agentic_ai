# 04 — Agent Frameworks & MCP

> 📍 **Level 2 / 03.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Hands-on experience with … multiple agents frameworks"* và *"Track and understand evolving agent development patterns across NVIDIA and the broader ecosystem."*

Sau khi tự xây harness ở module 03, giờ bạn khảo sát cách các framework lớn giải cùng bài toán — với con mắt của người **đánh giá và xây tooling cho framework**, không phải người dùng thuần. Với mỗi framework, câu hỏi luôn là: agent loop nằm ở đâu trong source? state được quản lý thế nào? can thiệp (intercept) vào giữa loop bằng cách nào?

## Kiến thức cần học

1. **LangGraph** — agent như state machine/graph; nodes, edges, checkpointing, human-in-the-loop.
2. **Một framework thứ hai** (chọn 1: Pydantic AI, OpenAI Agents SDK, CrewAI) — để có góc so sánh.
3. **MCP (Model Context Protocol)** — chuẩn mở kết nối tool/data vào agent: tools, resources, prompts; transports (stdio, streamable HTTP); lifecycle của một MCP session. MCP là "USB port của agent" — người xây core libraries bắt buộc phải thạo.
4. **Multi-agent patterns** — supervisor/orchestrator, handoff, parallel fan-out; trade-off chia sẻ context giữa các agent.

**Tài liệu:** LangGraph docs (làm hết phần tutorials cơ bản); https://modelcontextprotocol.io (đọc spec + quickstart); docs framework thứ hai bạn chọn.

## Bài tập

### Bài 4.1 — Rebuild agent bằng 2 framework
Xây lại coding agent của module 03 (cùng bộ tools — tái sử dụng code tools cũ) bằng **LangGraph** và **một framework khác**. Chạy lại 5 task đánh giá của bài 3.5 trên cả hai.
- **DoD:** bảng so sánh trong `NOTES.md` với các cột: số dòng code, mức kiểm soát loop (can thiệp được vào đâu?), cách quản lý state/context, tokens & latency trên cùng bộ task, điểm đau khi debug. Kết luận: nếu phải xây thư viện instrument cả hai, chỗ móc (hook point) của mỗi framework nằm ở đâu?

### Bài 4.2 — Viết MCP server ⭐
Dùng `mcp` Python SDK viết server expose 3 tools: `query_db` (SQLite có sẵn data mẫu), `fetch_url` (tải + trích text một trang web), `todo` (thêm/xem việc cần làm, lưu file). Chạy qua stdio transport.
- **DoD:** kết nối được từ một MCP client thật (Claude Code/Claude Desktop hoặc client tự viết bằng SDK); cả 3 tools gọi được end-to-end; server xử lý input xấu không crash.

### Bài 4.3 — MCP client + gắn vào mini_agent
Viết MCP **client** trong `mini_agent` (module 03): lúc khởi động, connect tới server của bài 4.2, list tools, merge vào tool registry — agent của bạn giờ dùng được tool từ bất kỳ MCP server nào.
- **DoD:** `mini-agent --mcp-server "python my_server.py"` dùng được `query_db` trong hội thoại; tool MCP lỗi được xử lý như tool thường (is_error).

### Bài 4.4 — Multi-agent supervisor
Xây bằng LangGraph: supervisor nhận yêu cầu nghiên cứu, điều phối 2 worker (`researcher` — có tool tìm/đọc, `writer` — tổng hợp thành báo cáo). Supervisor quyết định gọi ai, khi nào xong.
- **DoD:** với yêu cầu "so sánh ưu nhược của X và Y", trace cho thấy researcher chạy trước, writer tổng hợp sau; kết quả cuối là một báo cáo mạch lạc; có cơ chế chặn vòng lặp supervisor-worker vô hạn.

### Bài 4.5 — Đọc source một framework, viết architecture note
Chọn LangGraph hoặc framework thứ hai, đọc source phần lõi (executor/loop), viết note 1–2 trang: sơ đồ luồng một request từ `invoke()` đến khi trả kết quả, những extension point chính thức (callbacks/hooks), và một điểm thiết kế bạn cho là dở + vì sao.
- **DoD:** note trong `NOTES.md`, có sơ đồ (mermaid hoặc ASCII). Kỹ năng này chính là câu "track and understand evolving agent patterns" trong JD — luyện thành thói quen.

### Nâng cao (tùy chọn)
- Viết MCP server bằng streamable HTTP transport thay vì stdio, thêm auth đơn giản.
- Thử A2A hoặc một protocol multi-agent mới, so sánh với MCP trong note.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. LangGraph mô hình hoá agent thành **graph có state** thay vì while-loop. Được gì (checkpoint? rẽ nhánh? human-in-the-loop?) và mất gì (độ trong suốt? kiểm soát?) so với loop tự viết của bạn ở module 03? Trả lời bằng ví dụ cụ thể từ bài 4.1.
2. MCP giải quyết bài toán gì? Giải thích bằng phép tính M×N: M ứng dụng agent × N nguồn tool — không có protocol chung thì cần bao nhiêu tích hợp, có thì bao nhiêu?
3. Vì sao MCP là **protocol** chứ không phải library? Điều đó cho phép gì mà một Python package không làm được (nghĩ về ngôn ngữ khác, process khác, quyền sở hữu code)?
4. stdio transport và streamable HTTP transport khác nhau gì về deployment và trust model? Server chạy local của công cụ CLI nên dùng cái nào, server chạy cho nhiều người dùng nên dùng cái nào — vì sao?
5. Trong multi-agent supervisor: vì sao **không** cho worker chia sẻ toàn bộ context với nhau và với supervisor? Chia sẻ hết thì hỏng gì (token? nhiễu? trách nhiệm)?
6. Sau bài 4.1: nếu phải viết thư viện tracing gắn được vào cả mini_agent lẫn LangGraph, hook point của mỗi bên nằm ở đâu? Framework "khó instrument" là framework thiếu cái gì?
7. Diễn đạt lại kiến trúc framework bạn đọc ở bài 4.5 cho một người chưa từng dùng nó — trong 2 phút, không nhìn note.
