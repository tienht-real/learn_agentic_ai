# 03 — Xây Agent Harness từ đầu (mini coding agent)

> 📍 **Level 2 / 02.** Bài 3.1 (tool registry) đã có phiên bản ở [Level 1 / 05 bài 5.2](../../level_1/05_agent_basics/README.md) — tái sử dụng code đó. Số module cũ trong bài → tra [bảng ở Level 2](../README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Hands-on experience with evolving agent architectures, multiple agents frameworks and agent harnesses."*

Module quan trọng nhất của nửa đầu lộ trình. Bạn sẽ tự xây một **coding agent CLI** (phiên bản thu nhỏ của Claude Code / Codex CLI): agent có tools đọc/ghi file, chạy lệnh, và tự hoàn thành task nhiều bước. "Harness" = mọi thứ bao quanh model: agent loop, tool dispatch, quản lý context, safety. Hiểu harness từ bên trong là điều kiện để sau này **xây thư viện cho harness** — đúng vị trí JD tuyển.

Đặt tên project: `mini_agent/` (package Python đàng hoàng, có `pyproject.toml`, test bằng pytest). Code này sẽ được tái sử dụng ở module 05, 06, 09, 10.

## Kiến thức cần học

1. **Kiến trúc harness** — agent loop, tool registry, system prompt, conversation state; ranh giới giữa "model quyết định" và "harness thực thi".
2. **Thiết kế tool surface** — khi nào dùng bash chung chung vs tool chuyên biệt (`edit` tool chặn được ghi đè file đã đổi; bash thì không); tool description quyết định model có gọi đúng lúc không.
3. **Context management** — đếm token, cắt bớt tool result cũ, tóm tắt lịch sử khi gần đầy context.
4. **Safety cơ bản** — confirm trước lệnh nguy hiểm, timeout cho bash, giới hạn đường dẫn trong workspace (path traversal!).

## Bài tập (xây dần thành một project)

### Bài 3.1 — Tool registry
Viết decorator `@tool` tự sinh JSON Schema từ signature + docstring của hàm Python:

```python
@tool
def read_file(path: str, max_lines: int = 500) -> str:
    """Đọc nội dung file văn bản.

    Args:
        path: Đường dẫn tương đối trong workspace.
        max_lines: Số dòng tối đa.
    """
```

Registry có `get_schemas()` (trả list schema cho API) và `dispatch(name, input) -> str` (chạy tool, exception → chuỗi lỗi).
- **DoD:** schema sinh ra đúng chuẩn (type mapping `str→string`, `int→integer`, default → không required); test cho dispatch cả case thành công lẫn lỗi.

### Bài 3.2 — Bộ tools của coding agent
Implement: `read_file`, `write_file`, `edit_file` (thay thế exact string, lỗi nếu match 0 hoặc >1 lần — giống Claude Code), `list_dir`, `grep` (dùng subprocess gọi `rg` hoặc tự viết), `run_bash` (timeout 30s, trả cả stdout+stderr+exit code, **hỏi xác nhận y/n** trước khi chạy).
- **DoD:** mọi path đều được resolve và kiểm tra nằm trong workspace root (test với `../../etc/passwd` phải bị chặn); `edit_file` từ chối khi old_string xuất hiện 2 lần; `run_bash` bị timeout không treo agent.

### Bài 3.3 — Agent loop + CLI
Ghép registry + tools + loop (từ bài 2.3) thành CLI: `mini-agent "sửa bug trong file X"`. System prompt mô tả vai trò + quy tắc dùng tool. Stream text của model ra màn hình, in gọn mỗi tool call (`→ read_file(path=...)`).
- **DoD:** agent hoàn thành được task 2–3 bước trên repo thật (vd: "tìm hàm X đang được gọi ở đâu và thêm docstring cho nó"); phiên làm việc được lưu lại thành JSON để xem lại.

### Bài 3.4 — Context management
Thêm: (a) đếm token mỗi turn bằng API `count_tokens` (hoặc ước lượng); (b) khi vượt ngưỡng (vd 50k), **cắt bớt tool_result cũ** (thay bằng `"[truncated]"`) trước, nếu vẫn vượt thì **tóm tắt** nửa đầu hội thoại bằng một lời gọi LLM riêng rồi thay thế.
- **DoD:** chạy task dài 20+ tool calls không vỡ context; log cho thấy thời điểm truncate/summarize; agent sau khi tóm tắt vẫn nhớ mục tiêu ban đầu (test bằng task cụ thể).

### Bài 3.5 — Chấm điểm harness của chính mình
Tạo 5 task cố định trên một repo mẫu (tự tạo repo nhỏ có bug): sửa bug, viết test, thêm feature nhỏ, refactor, trả lời câu hỏi về code. Chạy mỗi task 3 lần, ghi lại: thành công/thất bại, số tool calls, tokens, thời gian.
- **DoD:** bảng kết quả trong `NOTES.md` + 3 nhận xét về điểm yếu của harness (đây là input cho module 06 — bạn sẽ tự động hoá việc chấm này).

### Nâng cao (tùy chọn)
- **Subagent**: tool `spawn_agent(task)` tạo agent con với context riêng, trả về kết quả tóm tắt — hiểu vì sao subagent giúp tiết kiệm context của agent chính.
- **Memory file**: agent đọc/ghi `MEMORY.md` giữa các phiên.

## Đọc source
- Claude Code system prompt & tool descriptions (nhiều bản dump trên GitHub) — chú ý cách viết description và các quy tắc trong system prompt.
- `sweagent` (Princeton) — một harness nghiên cứu có kiến trúc rõ ràng, dễ đọc.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. Định nghĩa "agent harness" bằng lời của bạn trong 3 câu. Ranh giới "model quyết định / harness thực thi" nằm ở đâu — cho ví dụ cụ thể một quyết định thuộc model và một quyết định thuộc harness trong chính `mini_agent` của bạn.
2. Tại sao `edit_file` yêu cầu old_string khớp **chính xác một lần** và fail nếu 0 hoặc >1 match? Nếu cho phép match nhiều chỗ thì rủi ro gì? So sánh với việc bảo model "ghi lại cả file".
3. Tại sao tool description quan trọng ngang code của tool? Chuyện gì xảy ra nếu description mơ hồ — model sẽ hỏng theo kiểu nào (gọi sai lúc? sai tham số? không gọi?)?
4. Context window đầy thì API trả gì? Giải thích chiến lược của bạn ở bài 3.4: vì sao **cắt tool_result cũ trước**, tóm tắt sau — thứ tự ngược lại thì tệ hơn ở điểm nào (chi phí? mất thông tin?)?
5. Path traversal: chỉ check `path.startswith(workspace)` trên **chuỗi** thì bị bypass thế nào (nghĩ về `..`, symlink, đường dẫn tuyệt đối)? Vì sao phải `resolve()` trước rồi mới so?
6. Vì sao `run_bash` cần timeout *và* cần hỏi xác nhận, còn `read_file` thì không? Từ đó suy ra nguyên tắc chung: tool thế nào thì cần gate?
7. Khi nào nên cho agent một tool chuyên biệt (`grep`, `edit_file`) thay vì để nó tự làm mọi thứ qua `run_bash` — dù bash làm được hết? (Gợi ý: harness *thấy* được gì ở mỗi kiểu?)
8. Ở bài 3.5, giữa các lần chạy cùng một task kết quả khác nhau — variance đó đến từ đâu, và nó ảnh hưởng thế nào đến cách bạn kết luận "harness A tốt hơn B"?
