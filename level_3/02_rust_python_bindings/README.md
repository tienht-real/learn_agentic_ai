# 08 — Rust ↔ Python: PyO3, maturin, đo overhead FFI

> 📍 **Level 3 / 02 — nhánh tuỳ chọn.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../../level_2/README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"…and/or Python native extension experience with PyO3, maturin, or Python/Rust bindings"* và *"Profiling or optimizing runtime/library overhead across language boundaries, async execution, native bindings, serialization."*

Đây chính là hình hài kỹ thuật của công việc trong JD: thư viện Python cho agent developer, hot path bằng Rust. Module này dạy bạn cả hai chiều: **làm** binding và **đo** xem binding có đáng không (FFI có chi phí — đôi khi pure Python thắng!).

## Kiến thức cần học

1. **PyO3 cơ bản** — `#[pyfunction]`, `#[pyclass]`, `#[pymodule]`; chuyển đổi kiểu (str/int/list/dict ↔ Rust types) và chi phí của mỗi lần chuyển; map lỗi Rust → Python exception.
2. **maturin** — `maturin develop` (build + cài vào venv), `maturin build --release`, cấu trúc project mixed Rust/Python, abi3 wheels.
3. **GIL** — khi nào Rust code giữ GIL, `py.allow_threads()` để nhả GIL cho tính toán dài, hệ quả với multithreading.
4. **Async bridging** — `pyo3-async-runtimes`: expose async fn Rust thành awaitable cho asyncio; hiểu 2 event loop (Tokio + asyncio) nói chuyện với nhau qua đâu.
5. **Đo lường** — `pytest-benchmark` phía Python, `criterion` phía Rust; tách "thời gian tính toán" khỏi "thời gian qua boundary" (conversion + GIL).

**Tài liệu:** PyO3 user guide (đọc hết phần Types và GIL); maturin docs; đọc source `pydantic-core` hoặc `tokenizers` (HuggingFace) — hai ví dụ sản phẩm thật của pattern này.

## Bài tập

### Bài 8.1 — Text chunker tốc độ cao ⭐
Viết crate `fastchunk` expose sang Python: `chunk_text(text, max_tokens, overlap) -> list[Chunk]` — cắt văn bản theo câu/đoạn với ước lượng token (đủ dùng: word-piece heuristic). Viết bản pure Python tương đương rồi benchmark cả hai trên file 10MB.
- **DoD:** `pip install -e .` (qua maturin) xong là `from fastchunk import chunk_text` chạy; benchmark bằng `pytest-benchmark` cho thấy chênh lệch (kỳ vọng 10–100x trên input lớn); bảng kết quả 3 cỡ input (1KB/1MB/10MB) trong `NOTES.md` — chú ý input nhỏ có khi Python thắng vì chi phí conversion, giải thích tại sao.

### Bài 8.2 — Wrap `rate_limiter` (module 07) cho Python
Expose crate rate_limiter thành package Python: API sync (`limiter.acquire()` block) **và** async (`await limiter.acquire_async()` — dùng pyo3-async-runtimes). Rồi tích hợp thật: dùng nó trong `mini_agent` để giới hạn tốc độ gọi LLM API.
- **DoD:** cả hai API hoạt động; test async chứng minh không block event loop của asyncio khi chờ quota (task khác vẫn chạy); mini_agent chạy eval (module 06) với rate limit 2 rps mà không lỗi 429.

### Bài 8.3 — Đo overhead qua ranh giới ngôn ngữ
Thí nghiệm có kiểm soát, mỗi case đo bằng benchmark tử tế:
1. Gọi hàm Rust rỗng từ Python vs gọi hàm Python rỗng (chi phí thuần FFI).
2. Truyền `list[str]` 100k phần tử vào Rust (chi phí conversion) vs truyền 1 string lớn nối sẵn.
3. Trả về dict lồng nhau (Rust build `PyDict`) vs trả JSON string rồi `json.loads` phía Python — cái nào nhanh hơn, và từ cỡ nào?
4. Hàm tính toán 100ms: có vs không `py.allow_threads()` — đo throughput khi 4 thread Python cùng gọi.
- **DoD:** bảng số liệu + kết luận thực dụng trong `NOTES.md` dạng "chỉ đưa xuống Rust khi X; batch data qua boundary thay vì gọi lắt nhắt vì Y ns/call". Bài này là câu chuyện phỏng vấn ăn tiền cho đúng gạch đầu dòng "profiling overhead across language boundaries".

### Nâng cao (tùy chọn)
- Viết SSE parser (bài 7.4) thành binding Python, benchmark với parser pure Python của bài 2.1 trên response capture thật.
- Build abi3 wheel cho 2 phiên bản Python, thử cài trên máy/venv khác không có Rust toolchain.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. GIL là gì và bảo vệ cái gì? Vì sao Rust extension được phép **nhả** GIL (`py.allow_threads`) khi tính toán, còn pure Python code thì không bao giờ nhả được giữa chừng? Nhả GIL lúc đang cầm reference tới object Python thì thảm hoạ gì xảy ra?
2. Chi phí đi qua boundary Python↔Rust gồm những phần nào (conversion mỗi phần tử, cấp phát, GIL)? Từ số đo bài 8.3 của bạn: một lần gọi FFI "rỗng" tốn ~bao nhiêu ns, và từ đó suy ra quy tắc "batch qua boundary" thế nào?
3. Vì sao với input nhỏ, bản pure Python có thể **thắng** bản Rust binding? Vẽ đường cong chi phí: điểm hoà vốn nằm ở đâu với chunker của bạn?
4. Từ thí nghiệm 8.3.3: trả về dict lồng nhau build bằng PyO3 vs trả JSON string rồi `json.loads` — kết quả của bạn ra sao và giải thích *tại sao* (ai đang cấp phát object Python, bao nhiêu lần)?
5. Async bridging: khi Python `await` một hàm async Rust, có **hai** event loop (asyncio và Tokio) — cái gì làm cầu nối, và tại sao không thể "chạy Tokio bên trong asyncio" một cách ngây thơ?
6. abi3 wheel là gì, vì sao nó cho phép một wheel chạy trên nhiều phiên bản Python? Trade-off của abi3 so với wheel build riêng từng phiên bản?
7. Nhìn lại `pydantic-core` hoặc `tokenizers`: vì sao họ chọn đúng những phần đó để đưa xuống Rust mà không phải toàn bộ thư viện? Rút ra tiêu chí chọn "hot path đáng đưa xuống Rust" cho capstone của bạn.
