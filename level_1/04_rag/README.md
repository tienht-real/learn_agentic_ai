# L1.04 — Embeddings & RAG (3 tuần) ⭐ trọng tâm Level 1

> JD VN: *"Thiết kế và triển khai hệ thống Retrieval-Augmented Generation (RAG)"*, *"document parsing, embedding, vector search, data preprocessing"*.

RAG là kỹ năng **xuất hiện nhiều nhất** trong JD AI Engineer tại VN, và cũng là tool phổ biến nhất mà agent ngoài thực tế phải gọi. Phase dài nhất của Level 1.

Nguyên tắc: **tự xây không framework trước**, rồi mới dùng LangChain. Hiểu từng bước thì mới debug được khi framework trả kết quả sai.

## Kiến thức cần học

| Mức | Chủ đề |
|---|---|
| 🔴 | Embedding: là gì, chiều vector, chọn model **hỗ trợ tiếng Việt** (multilingual: `bge-m3`, `multilingual-e5`, hoặc embedding API của provider) |
| 🔴 | Load tài liệu: PDF (`pymupdf`/`pypdf`), DOCX (`python-docx`), HTML, Markdown → text sạch + metadata (tên file, trang, mục) |
| 🔴 | **Chunking**: fixed-size, recursive, theo heading/cấu trúc; chunk size & overlap ảnh hưởng gì |
| 🔴 | Vector store local (Chroma hoặc FAISS): insert, search top-k, **metadata filter** |
| 🔴 | Pipeline RAG: retrieve → nhét context vào prompt → generate; **trích dẫn nguồn**; trả lời "không có trong tài liệu" khi không tìm thấy |
| 🟡 | Hybrid search: BM25 (keyword) + vector, gộp kết quả (Reciprocal Rank Fusion) — quan trọng với tiếng Việt vì tên riêng, mã số, điều khoản |
| 🟡 | Đo retrieval: bộ câu hỏi có đáp án nằm ở chunk nào → hit rate / recall@k |
| 🟡 | LangChain cho RAG: document loader, text splitter, retriever |
| 🟢 | OCR cho tài liệu scan (phổ biến ở ngân hàng, doanh nghiệp VN): Tesseract, hoặc LLM có vision |
| 🟢 | Tách từ tiếng Việt (`underthesea`, `pyvi`) cho BM25 |
| 🟢 | Vector DB production: pgvector, Qdrant, Milvus, Elasticsearch — khác nhau ở đâu |
| 🟢 | LlamaIndex — lựa chọn thay thế LangChain cho RAG |
| 🟢 | Reranker (cross-encoder) — đào sâu ở Level 2 |

**Tài liệu:**
- [LangChain — Build a RAG app](https://python.langchain.com/docs/tutorials/rag/)
- [Chroma docs](https://docs.trychroma.com/)
- [sentence-transformers](https://www.sbert.net/) — chạy embedding model local
- [MTEB leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — so sánh embedding model (lọc ngôn ngữ đa ngữ)

## Chọn bộ dữ liệu
Chọn **một bộ tài liệu tiếng Việt thật**, 20–100 trang, dùng xuyên suốt phase này và capstone. Gợi ý: Bộ luật Lao động, quy chế/sổ tay nhân viên mẫu, FAQ + điều khoản của một sản phẩm ngân hàng/viễn thông, tài liệu hướng dẫn sử dụng phần mềm.

## Bài tập

### Bài 4.1 — RAG không framework ⭐
Tự viết từng bước: `load()` → `chunk()` → `embed()` (gọi song song có giới hạn — bài 1.1) → lưu Chroma kèm metadata → `search(query, k)` → `answer(query)` với prompt yêu cầu trích dẫn `[nguồn: file, trang]` và từ chối khi context không đủ.
- **DoD:** trả lời đúng có trích dẫn với câu hỏi có trong tài liệu; **từ chối** (không bịa) với 3 câu hỏi ngoài tài liệu; re-index không tạo chunk trùng.

### Bài 4.2 — Bộ test retrieval & thử cấu hình
Tự viết 20–30 câu hỏi, mỗi câu ghi lại đoạn tài liệu chứa đáp án. Viết script tính hit rate@k và recall@k. Thử 3 cách chunking (ví dụ 300/800 token, và theo heading) × 2 giá trị k (3, 8).
- **DoD:** bảng số liệu 6 cấu hình trong `NOTES.md`; kết luận cấu hình nào thắng và tại sao.

### Bài 4.3 — Hybrid search
Thêm BM25 (`rank_bm25`), thử có/không tách từ tiếng Việt. Gộp với vector search bằng Reciprocal Rank Fusion. Đo lại bằng bộ test 4.2.
- **DoD:** số liệu trước/sau; chỉ ra ít nhất 2 câu hỏi mà BM25 cứu được vector search (thường là câu có mã số, tên riêng, số điều luật).

### Bài 4.4 — Viết lại bằng LangChain
Cùng pipeline, dùng LangChain loader + splitter + retriever + Chroma integration.
- **DoD:** kết quả bộ test tương đương bản tự viết (±nhiễu); `NOTES.md` so sánh: số dòng code, chỗ nào framework tiện, chỗ nào khó tuỳ biến/khó debug.

### Nâng cao (tuỳ chọn)
- Thêm 1–2 file PDF scan, xử lý bằng OCR, đo chất lượng text trích ra.
- Thử 2 embedding model khác nhau trên cùng bộ test.

## Câu hỏi diễn giải

1. RAG giải quyết vấn đề gì mà fine-tuning không giải quyết được (và ngược lại)?
2. Chunk quá lớn và chunk quá nhỏ gây hậu quả gì — với retrieval và với câu trả lời? Overlap để làm gì?
3. Vì sao vector search hay trượt với câu hỏi chứa mã số, tên riêng, "Điều 113"? Hybrid search giải quyết thế nào?
4. Hệ thống trả lời sai — làm sao biết lỗi nằm ở **retrieval** (lấy sai đoạn) hay **generation** (lấy đúng nhưng model hiểu sai)?
5. Vì sao phải lưu metadata cùng chunk? Kể 2 tính năng không làm được nếu thiếu metadata.
6. Embedding model và LLM có cần cùng provider không? Đổi embedding model thì phải làm gì với dữ liệu đã index?
7. Giải thích recall@k bằng lời cho một người không biết kỹ thuật.
