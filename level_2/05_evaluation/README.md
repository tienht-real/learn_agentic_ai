# 06 — Evaluation & Benchmarking cho Agent

> 📍 **Level 2 / 05.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Experience building evaluation/benchmarking systems for agent workflows (metrics, regression, feedback loops)"* và *"Benchmark the latest agents to identify bottlenecks."*

Điểm "stand out" số một trong JD. Khác với eval một prompt đơn lẻ, eval **agent workflow** khó hơn nhiều: kết quả không deterministic, task nhiều bước, "đúng" có nhiều dạng. Bạn sẽ xây eval harness cho chính agent module 03 — thứ bạn đã chấm tay ở bài 3.5, giờ tự động hoá.

## Kiến thức cần học

1. **Các loại grader** — exact match / chương trình kiểm tra (chạy test, kiểm tra file tồn tại) / rubric + LLM-as-judge; ưu nhược từng loại.
2. **LLM-as-judge đúng cách** — rubric cụ thể từng tiêu chí (không "đánh giá chất lượng 1-10" chung chung), calibrate judge với label tay, bias của judge (thiên vị câu dài, thiên vị vị trí).
3. **Chỉ số cho agent** — pass rate, pass@k, số tool calls, tokens/task, latency (p50/p95), cost/task; vì sao phải chạy nhiều lần (variance của LLM).
4. **Regression testing** — baseline, so sánh có ý nghĩa thống kê ở mức đơn giản (nhiều run, khoảng tin cậy thô), gate trong CI.
5. **Feedback loop** — kết quả eval quay lại cải thiện prompt/tool description thế nào.

**Tài liệu:** bài viết "LLM-as-a-judge" của Hamel Husain; docs của `inspect-ai` (UK AISI) — framework eval có kiến trúc đáng học; đọc cách SWE-bench chấm điểm.

## Bài tập

### Bài 6.1 — Eval harness ⭐
Xây package `agent_eval`: đọc bộ task từ YAML, chạy agent trên từng task (song song, giới hạn concurrency — tái dùng kỹ năng bài 1.1), chấm bằng grader, xuất báo cáo.

```yaml
# tasks/fix_bug_01.yaml
id: fix_bug_01
setup: "git checkout -- . && git clean -fd"   # reset repo mẫu
prompt: "Sửa bug khiến hàm parse_date trả sai với năm nhuận"
graders:
  - type: command      # chạy pytest, exit 0 = pass
    cmd: "pytest tests/test_parse_date.py -q"
  - type: llm_judge
    rubric: "Diff chỉ sửa hàm parse_date, không sửa file test, không thêm dependency mới."
budget: {max_tool_calls: 30, max_tokens: 100000}
```

- **DoD:** chạy được 5 task của bài 3.5 hoàn toàn tự động; mỗi task chạy N lần (mặc định 3); báo cáo gồm pass rate, mean/p95 latency, tokens, cost, số tool calls; task vượt budget bị dừng và tính là fail có lý do.

### Bài 6.2 — LLM-as-judge + calibration
Implement grader `llm_judge`: nhận transcript + rubric, trả `{pass: bool, reasoning}`. Sau đó **calibrate**: tự tay label 20 transcript (pass/fail), đo agreement giữa judge và bạn.
- **DoD:** agreement ≥ 85%; nếu thấp hơn, sửa rubric/prompt của judge và ghi lại quá trình sửa trong `NOTES.md` — vòng lặp sửa này chính là "feedback loop" trong JD. Gợi ý: chạy eval hàng loạt có thể dùng model rẻ hơn cho judge, nhưng hãy đo agreement của từng model trước khi quyết.

### Bài 6.3 — Benchmark cấu hình
Dùng harness so sánh ít nhất 2 cặp cấu hình của mini_agent, ví dụ: có/không có context truncation (bài 3.4); 2 phiên bản system prompt; có/không prompt caching (đo latency + cost). Mỗi cấu hình chạy đủ số lần để kết luận không phải nhiễu (≥5 run/task).
- **DoD:** bảng kết quả + biểu đồ (matplotlib) trong `NOTES.md`; một kết luận rõ ràng dạng "config A giảm 30% cost, pass rate không đổi trong phạm vi nhiễu".

### Bài 6.4 — Regression gate trong CI
Script `eval_gate.py`: chạy bộ eval, so với `baseline.json` (commit trong repo); fail (exit 1) nếu pass rate giảm quá ngưỡng hoặc cost/task tăng quá X%. Gắn vào GitHub Actions của repo mini_agent.
- **DoD:** PR cố tình làm hỏng prompt → CI đỏ; PR vô hại → CI xanh; lệnh cập nhật baseline có chủ đích (`--update-baseline`), không tự động.

### Bài 6.5 — Tận dụng tracing cho benchmark
Nối module 05 và 06: harness đọc spans/events từ phiên chạy eval để tự động trả lời "bottleneck ở đâu" — thời gian chia cho LLM vs tool vs harness overhead; tool nào lỗi nhiều nhất.
- **DoD:** báo cáo eval có thêm mục "performance breakdown" sinh tự động từ trace data; chỉ ra được 1 bottleneck thật và đề xuất cách sửa.

### Nâng cao (tùy chọn)
- pass@k: cho agent chạy k lần mỗi task, tính pass@1 và pass@3, giải thích khi nào metric nào có ý nghĩa.
- Chạy agent của bạn trên một subset SWE-bench-lite (5–10 instance) và ghi lại kết quả — trải nghiệm benchmark "chuẩn công nghiệp".

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. Vì sao chạy mỗi task **một lần** rồi kết luận "config A tốt hơn B" là sai về phương pháp? Variance của agent đến từ những nguồn nào (model non-deterministic, thứ tự tool, môi trường)?
2. Ba loại grader (exact/command, rubric+LLM-judge, human) — mỗi loại mạnh yếu ở đâu? Vì sao "chạy pytest" là grader đáng tin nhất khi áp dụng được, và khi nào **không** áp dụng được?
3. LLM-as-judge có những bias nào (độ dài, vị trí, tự thiên vị văn phong giống mình)? Calibration với label tay giải quyết gì — và agreement 85% nghĩa là bạn được phép tin judge đến mức nào?
4. Vì sao rubric "chấm chất lượng 1–10" tệ hơn hẳn rubric "diff chỉ sửa hàm X, không đụng file test"? Nguyên tắc chung để viết rubric chấm được là gì?
5. pass@1 và pass@3 khác nhau về **ý nghĩa sản phẩm** thế nào? Sản phẩm nào cần pass@1 cao (agent tự động chạy nền) vs chấp nhận pass@3 (người dùng xem và chọn)?
6. Regression gate: vì sao baseline phải được commit vào repo và chỉ cập nhật **có chủ đích**? Nếu baseline tự cập nhật mỗi lần chạy thì gate còn ý nghĩa gì không?
7. "Feedback loop" trong JD nghĩa là gì qua trải nghiệm của bạn ở bài 6.2 — mô tả một vòng cụ thể: eval lộ ra vấn đề gì → bạn sửa gì (prompt? tool description? rubric?) → số đo thay đổi ra sao?
8. Từ bài 6.5: nếu tổng thời gian task là 60s mà LLM calls chiếm 50s, tối ưu harness code có đáng không? Bạn dùng dữ liệu trace nào để quyết định *nên* tối ưu cái gì?
