"""Bài 2.3 — Tool-calling loop thủ công.

Tự viết agentic loop để hiểu cơ chế (SDK có tool_runner làm sẵn việc này,
nhưng ở đây mục tiêu là hiểu — thư viện bạn xây sau này chính là thứ nằm
giữa loop này và người dùng).

Chạy: uv add anthropic && uv run ex03_tool_loop.py

────────────────────────────────────────────────────────────────────
GIẢI THÍCH THIẾT KẾ — mô hình tư duy cốt lõi của tool calling
────────────────────────────────────────────────────────────────────
Điều quan trọng nhất phải "ngấm" từ bài này:

    MODEL KHÔNG CHẠY TOOL. Model chỉ SINH RA một cục JSON nói
    "tôi muốn gọi tool X với input Y". Người chạy tool là BẠN (harness).
    Sau đó bạn NHÉT KẾT QUẢ NGƯỢC VÀO HỘI THOẠI và gọi API lần nữa.

Vì sao thiết kế vậy? (1) An toàn — model không bao giờ chạm vào máy bạn,
mọi side effect đều qua tay harness nên chặn/ghi log/hỏi xác nhận được
(module 09 xây đúng chỗ này). (2) Tool của bạn nằm sau firewall, provider
không cần và không thể với tới. (3) API stateless — "trạng thái" của agent
chính là cái list `messages`, không có gì huyền bí hơn.

Hệ quả trực tiếp: vòng lặp là NGHĨA VỤ của bạn. API không tự lặp.
"""

import asyncio
import datetime
import json
from pathlib import Path

import anthropic

MODEL = "claude-opus-4-8"

# WHY schema mô tả kỹ đến vậy?
# `description` là "UI" của tool đối với model — model quyết định GỌI HAY
# KHÔNG và ĐIỀN INPUT GÌ hoàn toàn dựa trên name/description/schema.
# Description mơ hồ = model gọi sai lúc hoặc điền sai tham số, và bug đó
# không nằm trong code Python nào để bạn debug cả.
TOOLS = [
    {
        "name": "calculator",
        "description": "Tính một biểu thức số học. Dùng khi cần tính toán chính xác.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Ví dụ: '12 * 7 + 3'"}
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_time",
        "description": "Lấy ngày giờ hiện tại (ISO 8601).",
        # WHY vẫn cần schema dù không có tham số? Contract là contract —
        # model luôn cần biết "tool này nhận input hình dạng gì", kể cả rỗng.
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "read_file",
        "description": "Đọc nội dung một file văn bản theo đường dẫn.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]


# WHY trả về str và để exception thoát ra ngoài?
# Tách bạch trách nhiệm: execute_tool chỉ biết CHẠY. Việc "lỗi thì đóng gói
# thành tool_result is_error=True" là chính sách của LOOP — vì lỗi tool
# không phải điểm dừng, nó là THÔNG TIN cho model ("file không tồn tại")
# để model tự đổi hướng. Nuốt lỗi ở đây thì loop không phân biệt được
# "tool trả về chuỗi rỗng" với "tool nổ".
async def execute_tool(name: str, tool_input: dict) -> str:
    """Chạy 1 tool. Exception ở đây sẽ được loop chuyển thành is_error=True."""
    if name == "calculator":
        # eval() chỉ dùng cho bài học — module 09 sẽ dạy bạn chặn thứ này bằng guardrail
        return str(eval(tool_input["expression"], {"__builtins__": {}}, {}))
    if name == "get_time":
        return datetime.datetime.now().isoformat()
    if name == "read_file":
        return Path(tool_input["path"]).read_text()
    raise ValueError(f"Unknown tool: {name}")


async def agent_loop(user_message: str, max_iterations: int = 10) -> str:
    client = anthropic.AsyncAnthropic()

    # WHY messages là MỘT list được append dần?
    # API stateless: mỗi request gửi lại TOÀN BỘ lịch sử. List này chính là
    # "bộ nhớ" của agent. Quên append một mảnh (vd assistant content) là
    # model "mất trí nhớ" mảnh đó ở lượt sau — API còn reject vì tool_result
    # không khớp với tool_use nào.
    messages: list[dict] = [{"role": "user", "content": user_message}]

    # WHY for chứ không while True?
    # max_iterations là cầu chì. Model có thể lặp gọi tool mãi (tool trả lỗi
    # → model thử lại → lỗi → thử lại...). Không có cầu chì = treo + đốt tiền.
    for _ in range(max_iterations):
        response = await client.messages.create(
            model=MODEL, max_tokens=4096, tools=TOOLS, messages=messages
        )

        # TODO 1: nếu stop_reason == "end_turn" -> trả về text cuối cùng
        #
        # TODO 2: nếu stop_reason == "pause_turn" -> append assistant content rồi continue
        #
        # TODO 3: nếu stop_reason == "tool_use":
        #   a) append {"role": "assistant", "content": response.content}
        #      WHY append NGUYÊN response.content chứ không chỉ phần text?
        #      Trong đó có các block tool_use (mang id). Lượt sau API đối
        #      chiếu tool_result.tool_use_id với đúng các block này —
        #      thiếu chúng là request bị reject.
        #
        #   b) gom các block .type == "tool_use"
        #
        #   c) chạy TẤT CẢ bằng asyncio.gather (bọc execute_tool, bắt exception
        #      -> {"is_error": True, "content": str(e)})
        #      WHY gather? Model đã quyết 3 tool này ĐỘC LẬP với nhau (nó xin
        #      cả 3 trong cùng một response) — chạy tuần tự chỉ phí thời gian.
        #      Đây là lý do bạn học module 01 trước module này.
        #
        #   d) append MỘT user message chứa list tool_result blocks
        #      WHY role "user"? Lượt nói của hội thoại phải xen kẽ; kết quả
        #      tool là "thế giới bên ngoài trả lời model" — nó đi vào lượt
        #      user. WHY MỘT message chứa cả 3 result? Tách thành 3 message
        #      là dạy model rằng "mỗi lần chỉ nên xin 1 tool" — nó sẽ dần
        #      bỏ parallel calls (điều bạn KHÔNG muốn).
        #
        # TODO 4: stop_reason == "max_tokens" -> xử lý (gợi ý: tăng max_tokens
        #      hoặc báo lỗi rõ ràng). WHY phải xử lý riêng? Response bị CẮT
        #      GIỮA CHỪNG — có thể đứt ngay giữa một tool_use block. Cứ thế
        #      append rồi đi tiếp là gửi lên một hội thoại sứt mẻ.
        raise NotImplementedError

    return "Đạt max_iterations mà chưa xong — kiểm tra lại loop."


async def main() -> None:
    Path("sample.txt").write_text("dòng 1\ndòng 2\ndòng 3\n")
    answer = await agent_loop(
        "Đọc file sample.txt, đếm số dòng, rồi lấy số dòng nhân với 7. "
        "Cho tôi biết cả thời gian hiện tại."
    )
    print("\n=== KẾT QUẢ ===\n", answer)

    # TỰ KIỂM TRA sau khi chạy được — trả lời không nhìn code:
    # 1. Vẽ lại chuỗi request/response của đúng phiên vừa chạy: bao nhiêu lần
    #    gọi API? Mỗi lần, messages chứa những gì?
    # 2. Xoá dòng append assistant content rồi chạy — API báo lỗi gì? Vì sao?
    # 3. Đổi read_file("sample.txt") thành file không tồn tại — model phản
    #    ứng thế nào với is_error? Nó có thử cách khác không?


if __name__ == "__main__":
    asyncio.run(main())
