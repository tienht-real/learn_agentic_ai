# L1.08 — Capstone Level 1 (2 tuần)

## Trợ lý hỏi đáp tài liệu nội bộ tiếng Việt

Gom phase 03 → 07 thành **một repo GitHub riêng, hoàn chỉnh** — project bạn đem đi phỏng vấn và ghi vào CV.

Thiết kế để phủ được cả 3 nhóm nhà tuyển dụng: chức năng đáp ứng JD VN (RAG, agent, FastAPI, Docker); cách làm đáp ứng chuẩn công ty nước ngoài/toàn cầu (eval, test, CI, giải thích quyết định thiết kế bằng tiếng Anh).

## Yêu cầu chức năng
- Upload tài liệu (PDF/DOCX) → tự index ở background
- Hỏi đáp có **trích dẫn nguồn**; từ chối khi tài liệu không có thông tin
- Agent **tự viết** (không framework) có ít nhất 3 tool, trong đó một tool là RAG hybrid search
- Hội thoại nhiều lượt, lưu lịch sử
- UI Streamlit/Gradio có streaming

## Yêu cầu kỹ thuật
- FastAPI + Pydantic; `docker compose up` chạy toàn bộ
- Test: unit test cho chunking, tool registry, endpoint chính (LLM được mock)
- **CI** (GitHub Actions): lint + test mỗi PR
- **Eval**: `run_eval.py` + golden set ≥ 30 câu; báo cáo so sánh ít nhất 2 cấu hình; bảng nhóm lỗi từ phân tích transcript
- Log token/chi phí/latency mỗi request
- Không có secret trong repo; có `.env.example`
- Tuỳ chọn (🟢): gửi trace lên Langfuse

## Tài liệu trong repo — viết bằng tiếng Anh
**`README.md`**
1. Demo (GIF hoặc video ngắn)
2. Sơ đồ kiến trúc
3. Cách chạy trong ≤ 5 lệnh
4. Kết quả eval (bảng số)
5. Hạn chế đã biết & hướng cải thiện

**`DECISIONS.md`** — mỗi quyết định thiết kế một mục: bối cảnh → các lựa chọn → chọn gì → vì sao → đánh đổi. Ít nhất: embedding model, chunking, vector store, hybrid search, tự viết agent loop vs LangGraph, model LLM, cách chấm eval. File này là thứ người phỏng vấn nước ngoài muốn đọc nhất.

## DoD
- Người lạ đọc README chạy được trong 10 phút
- CI xanh; eval chạy được bằng một lệnh
- Trình bày kiến trúc trong 5 phút (một lần tiếng Việt, một lần tiếng Anh) và trả lời được "tại sao chọn X thay vì Y" cho mọi thành phần
- Trả lời trôi chảy 10 câu ở [tiêu chí hoàn thành Level 1](../README.md#tiêu-chí-hoàn-thành-level-1)
