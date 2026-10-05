# Level 1 — Nền tảng & Junior-ready (~17 tuần)

**Mục tiêu:** tự xây được ứng dụng RAG + agent, đóng gói thành API, chạy bằng Docker, đo được chất lượng bằng eval, có test và CI.
**Ứng tuyển được:** Intern / Fresher / Junior AI Engineer ở doanh nghiệp VN và công ty nước ngoài tại VN; vị trí new-grad ở công ty toàn cầu (cần thêm tiếng Anh tốt).
**Đầu ra:** repo capstone *Trợ lý hỏi đáp tài liệu nội bộ tiếng Việt*.

Ký hiệu mức độ (🔴 chuyên sâu · 🟡 nắm vững · 🟢 học qua) — xem [ROADMAP_VN.md](../ROADMAP_VN.md#ký-hiệu-mức-độ).

| # | Phase | Thời lượng | Trọng tâm |
|---|---|---|---|
| 00 | [Setup](00_setup/README.md) | 0.5 tuần | uv, Git, Docker, API key |
| 01 | [Python cho AI Engineer](01_python_foundations/README.md) | 2 tuần | Pydantic, async, giải thuật |
| 02 | [ML & DL nền tảng](02_ml_foundations/README.md) | 1.5 tuần | Embedding, metric, PyTorch (học qua) |
| 03 | [LLM API & Prompt Engineering](03_llm_api_prompt/README.md) | 2 tuần | Messages, streaming, structured output, prompt có đo lường |
| 04 | [Embeddings & RAG](04_rag/README.md) ⭐ | 3 tuần | Chunking, vector DB, hybrid search, đo retrieval |
| 05 | [Tool calling & Agent cơ bản](05_agent_basics/README.md) | 2.5 tuần | Agent loop tự viết, tool registry, LangGraph |
| 06 | [Backend & Deploy](06_backend_deploy/README.md) | 2 tuần | FastAPI, Docker Compose, Postgres, CI |
| 07 | [Eval & chất lượng](07_eval_basics/README.md) ⭐ | 1.5 tuần | Phân tích lỗi, golden set, LLM-as-judge, prompt injection |
| 08 | [Capstone](08_capstone/README.md) | 2 tuần | Project portfolio + `DECISIONS.md` + README tiếng Anh |

**Song song suốt Level 1** (không phải phase riêng): tiếng Anh kỹ thuật, Git/PR/test, dùng AI coding tool có kiểm soát, giải thuật — xem [Kỹ năng song hành](../ROADMAP_VN.md#kỹ-năng-song-hành-chạy-suốt-level-1-không-phải-phase-riêng).

Các phase nối tiếp nhau: model `Invoice` (01) → trích xuất bằng LLM (03); RAG (04) → thành tool của agent (05) → bọc API (06) → được đo (07) → capstone (08). Giữ code trong một repo để tái sử dụng.

Cách học mỗi phase: theo quy trình "hiểu và diễn đạt lại" trong [README chính](../README.md#quy-trình-hiểu-và-diễn-đạt-lại-kiểu-feynman). Code chạy được chưa phải là xong — trả lời được **Câu hỏi diễn giải** cuối mỗi README mới là xong.

## Tiêu chí hoàn thành Level 1

Trả lời trôi chảy, không xem tài liệu:

1. Token là gì? Context window giới hạn điều gì? `temperature` cao/thấp dùng khi nào?
2. RAG giải quyết vấn đề gì mà fine-tuning không giải quyết (và ngược lại)?
3. Chunk quá lớn / quá nhỏ gây hậu quả gì? Bạn chọn chunk size bằng cách nào?
4. Vì sao cần hybrid search với tài liệu tiếng Việt?
5. Agent khác workflow thế nào? Cho ví dụ nên dùng workflow thay vì agent.
6. Agent loop của bạn dừng khi nào? Tool lỗi thì chuyện gì xảy ra?
7. Làm sao biết thay đổi prompt làm hệ thống tốt lên hay tệ đi?
8. Giảm hallucination trong hệ thống của bạn bằng những cách nào?
9. Precision và recall khác nhau thế nào? Áp vào retrieval ra sao?
10. Một request đi qua hệ thống của bạn từ lúc user gõ đến lúc nhận câu trả lời — mô tả từng bước.

Đạt 10 câu + capstone hoàn chỉnh → sẵn sàng ứng tuyển và chuyển sang [Level 2](../level_2/README.md).
