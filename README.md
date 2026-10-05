# Learn Agentic AI — Lộ trình AI Engineer / Agentic AI Engineer

Repo lộ trình + bài tập thực hành, chia theo **3 level**. Nội dung bám theo JD tuyển dụng thực tế — xem phân tích và bảng mức độ trong [ROADMAP_VN.md](ROADMAP_VN.md).

## Cấu trúc

```
learn_agentic_ai/
├── ROADMAP_VN.md        # phân tích JD, ký hiệu mức độ, tổng quan các level
├── shared/              # client gọi LLM dùng chung (API tương thích OpenAI)
├── level_1/             # Nền tảng & Junior-ready (~16 tuần)  ← bắt đầu ở đây
│   ├── 00_setup/
│   ├── 01_python_foundations/
│   ├── 02_ml_foundations/
│   ├── 03_llm_api_prompt/
│   ├── 04_rag/
│   ├── 05_agent_basics/
│   ├── 06_backend_deploy/
│   ├── 07_eval_basics/
│   └── 08_capstone/
├── level_2/             # AI Engineer Mid — production (khung + module có sẵn)
└── level_3/             # Senior/Lead + nhánh chuyên sâu core libraries (khung)
```

| Level | Mục tiêu | Ứng tuyển |
|---|---|---|
| [Level 1](level_1/README.md) | RAG + agent + FastAPI + Docker + eval cơ bản | Intern / Junior |
| [Level 2](level_2/README.md) | Multi-agent, MCP, observability, eval tự động, guardrails, cloud | Mid |
| [Level 3](level_3/README.md) | System design, model mở, LLMOps, dẫn dắt kỹ thuật | Senior / Lead |

Bắt đầu: [`level_1/00_setup/README.md`](level_1/00_setup/README.md).

## Cấu trúc mỗi module

```
XX_ten_module/
├── README.md        # mục tiêu, kiến thức (có mức độ 🔴🟡🟢), bài tập + DoD, câu hỏi diễn giải
├── exercises/       # bài tập (một số có sẵn skeleton, còn lại bạn tự tạo file)
└── NOTES.md         # bạn tự viết: điều học được, quyết định thiết kế, số đo
```

## Nguyên tắc học

1. **Làm theo thứ tự trong level.** Phase sau tái sử dụng code phase trước — bạn có một codebase tiến hoá liên tục thay vì các bài tập rời rạc.
2. **Mỗi bài tập có "Definition of Done" (DoD).** Chưa đạt DoD thì chưa chuyển bài. DoD luôn gồm code chạy được + một đoạn ghi chú ngắn trong `NOTES.md`.
3. **Đẩy lên GitHub từ ngày đầu.** Commit thường xuyên, viết README cho từng bài như thể người khác sẽ dùng — đây là portfolio của bạn.
4. **Đo, đừng đoán.** Từ phase 03 trở đi, mọi kết luận "cách A tốt hơn cách B" phải kèm số liệu.
5. **Hiểu được và diễn đạt lại được — mới tính là xong.** Xem quy trình bên dưới.

## Quy trình "hiểu và diễn đạt lại" (kiểu Feynman)

Code chạy được **chưa phải** là xong. Mỗi module có mục **"Câu hỏi diễn giải"** ở cuối README — đó là bar thật sự của module. Quy trình cho mỗi bài tập:

1. **Trước khi code** — đọc phần "Kiến thức cần học", lướt qua câu hỏi diễn giải và thử đoán câu trả lời. Đoán sai không sao; não đã được "mồi" đúng chỗ.
2. **Trong khi code** — mỗi khi copy một pattern (Semaphore, `gather`, `tool_call_id`...) mà không giải thích được *vì sao pattern này chứ không phải cái khác*, dừng lại tra cho ra trước khi đi tiếp.
3. **Sau khi code** — gập code lại, trả lời các câu hỏi diễn giải **bằng lời của mình** (nói miệng 1–2 phút/câu, hoặc viết vào `NOTES.md`). Chỗ nào ấp úng chính là chỗ chưa hiểu — quay lại đó.
4. **Dùng AI làm người hỏi vặn, không phải người giải thích hộ.** Cách dùng đúng:
   - ✅ *"Đây là code tôi vừa viết. Đừng giải thích gì cả — hãy hỏi vặn tôi 5 câu 'tại sao' về nó, chờ tôi trả lời từng câu, rồi chấm và chỉ ra chỗ tôi hiểu sai."*
   - ✅ *"Tôi sẽ giải thích đoạn này theo cách tôi hiểu. Nghe xong hãy chỉ ra chỗ nào tôi nói sai hoặc nói mơ hồ."*
   - ✅ Khi bí thật sự: hỏi *"tại sao dòng X cần thiết, nếu bỏ đi thì chuyện gì xảy ra?"* — câu trả lời dạng "bỏ đi thì hỏng thế nào" bám vào đầu lâu hơn định nghĩa suông.
   - ❌ *"Giải thích file này cho tôi"* rồi đọc lướt và gật gù — cảm giác hiểu, không phải hiểu.
5. **Bài kiểm tra cuối module:** giả lập phỏng vấn — nhờ AI đóng vai interviewer hỏi về đúng những gì bạn vừa xây. Trả lời trôi chảy → qua module.
