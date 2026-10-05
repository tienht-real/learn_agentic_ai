# 09 — Middleware, Guardrails, Policy Engine, Plugin System

> 📍 **Level 2 / 06.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Middleware, plugin systems, guardrails, policy engines, or request/response interception."*

Module này biến `mini_agent` từ một CLI thành một **nền tảng mở rộng được** — đúng loại "reusable building blocks" JD mô tả. Bạn đã có middleware chain từ bài 1.4; giờ áp nó vào agent với các hook point thực sự hữu ích, rồi xây policy engine và guardrails phía trên.

## Kiến thức cần học

1. **Hook points của agent** — 4 điểm chặn tự nhiên: `before_llm_call` / `after_llm_call` / `before_tool_call` / `after_tool_call`; middleware được sửa payload, chặn hẳn (short-circuit), hay chỉ quan sát.
2. **Policy engine** — tách "quyết định" (rules data) khỏi "thực thi" (engine code); ngữ nghĩa allow/deny/confirm; thứ tự ưu tiên rule; default deny vs default allow.
3. **Guardrails thực tế** — tool allowlist, chặn lệnh nguy hiểm, giới hạn filesystem, PII redaction, phát hiện prompt injection (từ tool results — nguồn injection số 1 của agent).
4. **Plugin system** — Python entry points (`importlib.metadata`), load extension từ package ngoài, versioning contract giữa host và plugin.

**Tài liệu:** đọc thiết kế hooks của Claude Code (docs) và middleware của ASGI; source `pluggy` (plugin system của pytest) — mẫu mực về plugin architecture.

## Bài tập

### Bài 9.1 — Middleware pipeline cho mini_agent ⭐
Refactor mini_agent: mọi LLM call và tool call đi qua middleware chain (dùng lại design bài 1.4, giờ có 4 hook points). Middleware là class với method async tùy chọn (chỉ implement hook mình cần). Chuyển UsageTracker (bài 2.5) và tracing (module 05) thành middleware — chứng minh kiến trúc đúng bằng cách port code cũ sang gọn hơn.
- **DoD:** config khai báo (`middlewares = [TracingMW(), UsageMW(), ...]`) — thêm/bớt không sửa core; test thứ tự onion đúng; middleware ném exception được xử lý theo policy rõ ràng (fail-open cho observability, fail-closed cho security — bạn quyết và ghi lý do).

### Bài 9.2 — Guardrail middleware
Viết `GuardrailMW` chặn ở `before_tool_call`: (a) tool allowlist theo config; (b) `run_bash` bị chặn với pattern nguy hiểm (`rm -rf`, `sudo`, ghi ra ngoài workspace, curl bí ẩn pipe vào sh); (c) mọi path argument bị kiểm tra nằm trong workspace. Chặn thì trả `tool_result` với `is_error` + lý do — model biết đường mà đổi hướng, agent không crash.
- **DoD:** bộ test đỏ/xanh ≥ 15 case (kể cả bypass sáng tạo: `r"m" + "-rf"` không cần bắt, nhưng `rm -rf /` viết qua biến bash thì nên); agent bị chặn vẫn tiếp tục hội thoại tử tế.

### Bài 9.3 — Policy engine từ YAML
Engine đọc rules:

```yaml
rules:
  - match: {tool: "run_bash", input_regex: "git push"}
    action: confirm          # hỏi người dùng y/n
  - match: {tool: "write_file", path_outside: "./src"}
    action: deny
    reason: "Chỉ được ghi trong src/"
  - match: {tool: "*"}
    action: allow
default: deny
```

Rule đầu tiên match thắng. `confirm` nối vào cơ chế hỏi y/n có sẵn của `run_bash` (bài 3.2) — giờ generalize cho mọi tool.
- **DoD:** test ngữ nghĩa first-match + default; đổi policy không đổi code; log ghi lại mọi quyết định deny/confirm (audit trail) — qua structured events của module 05.

### Bài 9.4 — PII redaction + prompt injection detection
Hai guardrail ở `after_tool_call` (lọc dữ liệu **trước khi** vào context của model): (a) redact email/số điện thoại/API key pattern trong tool results; (b) detector câu lệnh injection trong nội dung web/file (heuristics: "ignore previous instructions", nội dung giả dạng system prompt...) — đánh dấu và bọc cảnh báo thay vì đưa thẳng cho model.
- **DoD:** demo end-to-end: agent fetch một trang web có chứa injection "hãy chạy rm -rf" → nội dung bị bọc cảnh báo, model không thực thi; đo false positive trên 20 trang web bình thường (dùng eval harness module 06!).

### Bài 9.5 — Plugin system
Cho phép package ngoài đăng ký middleware qua entry points:

```toml
# pyproject.toml của plugin
[project.entry-points."mini_agent.middleware"]
my_guard = "my_pkg:MyGuardMW"
```

mini_agent lúc khởi động discover + load, có `--disable-plugin X`.
- **DoD:** tạo một plugin package riêng (repo/folder khác), `pip install` vào là middleware tự xuất hiện; plugin lỗi lúc load không kéo sập agent, chỉ warning.

### Nâng cao (tùy chọn)
- Viết matcher engine của policy (regex + glob trên input) bằng Rust qua PyO3 — nối module 08, benchmark với bản Python khi có 1000 rules.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. Fail-open vs fail-closed: vì sao middleware **tracing** lỗi thì nên nuốt lỗi và cho request đi tiếp (fail-open), còn middleware **guardrail** lỗi thì phải chặn request (fail-closed)? Đảo ngược hai cái thì hậu quả cụ thể là gì?
2. Vì sao guardrail chặn tool call nên trả về `tool_result` với `is_error` + lý do cho **model đọc**, thay vì raise exception làm sập loop? Hai cách này khác nhau gì về khả năng agent tự phục hồi?
3. Policy engine tách rules (YAML) khỏi engine (code): ai là người hưởng lợi? Vì sao "đổi chính sách không cần deploy code" quan trọng với thư viện dùng trong tổ chức lớn?
4. Ngữ nghĩa **first-match-wins** vs **most-specific-wins** trong policy: bạn chọn cái nào, và cái còn lại có vấn đề gì (dễ đoán? dễ viết nhầm?)? Vì sao `default: deny` an toàn hơn `default: allow` — nhưng phiền hơn ở đâu?
5. Prompt injection từ **tool results** (nội dung web/file) nguy hiểm hơn injection từ user gõ vào ở điểm nào? (Gợi ý: ai là người "nói", model phân biệt nguồn tin thế nào, và user có nhìn thấy nội dung đó không?)
6. Vì sao PII redaction phải đặt ở `after_tool_call` — tức là lọc **trước khi dữ liệu vào context của model** — chứ không phải lọc lúc in ra màn hình? Lọc muộn thì dữ liệu đã "rò" đi những đâu (context, log, trace, cache)?
7. Plugin qua entry points: chuyện gì xảy ra khi plugin viết cho phiên bản API middleware cũ chạy với host mới? "Contract giữa host và plugin" gồm những gì và bạn version nó thế nào?
8. Onion model một lần nữa, giờ với 4 hook: một middleware vừa có `before_tool_call` vừa có `after_tool_call` — vẽ thứ tự thực thi khi có 3 middleware và giải thích vì sao stack (LIFO) là cấu trúc tự nhiên ở đây.
