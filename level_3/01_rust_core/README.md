# 07 — Rust: từ cơ bản đến Async (Tokio) & thiết kế library

> 📍 **Level 3 / 01 — nhánh tuỳ chọn.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../../level_2/README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD: *"Rust systems work, especially async Rust, Tokio, serde, API design, or runtime state management."*

Rust là điểm "stand out" lớn nhất của JD (được nhắc riêng một gạch đầu dòng). Mục tiêu module này không phải "biết Rust" mà là **viết được library Rust có API tử tế** — vì module 08 sẽ expose nó sang Python, và capstone dùng nó làm hot path.

## Kiến thức cần học

Giai đoạn 1 (tuần 1–2): **The Rust Book** các chương 1–13, 15 (bỏ qua được 14, 16 đọc sau) — ownership/borrowing, structs/enums, pattern matching, traits & generics, error handling (`Result`, `?`), collections, closures, iterators, smart pointers.

Giai đoạn 2 (tuần 2–3): hệ sinh thái library — `serde` (derive, custom serialize), `thiserror`/`anyhow` (lỗi cho library vs application), `clap` (CLI), module system & visibility, doc comments + doctests, `cargo clippy` như thói quen.

Giai đoạn 3 (tuần 3–4): **async Rust** — `Future` là gì (poll-based, khác callback-based của JS và coroutine của Python thế nào — viết ra so sánh này, phỏng vấn rất hay hỏi), Tokio runtime, `spawn`, `join!`/`select!`, channels (`mpsc`, `oneshot`, `broadcast`), `Arc<Mutex<T>>` vs message passing, cancellation qua drop.

**Tài liệu:** The Rust Book; Tokio tutorial (làm hết, kể cả mini-redis); "Rust for Rustaceans" chương API design nếu có điều kiện.

## Bài tập

### Bài 7.1 — CLI todo (khởi động)
CLI quản lý việc cần làm: `todo add/list/done/rm`, lưu JSON bằng serde, parse args bằng clap. Mọi lỗi qua `Result` + `thiserror` — không `unwrap()` trong logic chính.
- **DoD:** `cargo clippy -- -D warnings` sạch; có unit test cho logic; file JSON hỏng → thông báo lỗi tử tế, không panic.

### Bài 7.2 — Library `rate-limiter` ⭐
Viết crate `rate_limiter`: token bucket + sliding window, dùng được cả sync lẫn async (`acquire()` async chờ đến khi có quota). Đây là bài **API design**: builder pattern (`RateLimiter::builder().rps(10).burst(20).build()`), doc comments có ví dụ chạy được (doctests), không leak chi tiết nội bộ ra public API.
- **DoD:** doctest + unit test pass (`cargo test`); test chứng minh đúng ngữ nghĩa: 10 rps với burst 20 → 20 request đầu qua ngay, sau đó ~10/giây; README của crate viết như crate thật trên crates.io. Crate này sẽ được wrap sang Python ở module 08.

### Bài 7.3 — Async fetcher (bản Rust của bài 1.1)
Tải N URL đồng thời bằng Tokio + `reqwest`: giới hạn concurrency bằng `Semaphore`, timeout, retry backoff. So sánh trực tiếp code + hành vi với bản Python của bạn.
- **DoD:** chạy đúng như bản Python; trong `NOTES.md` viết so sánh: cancellation ở Rust (drop future) khác `CancelledError` của Python thế nào; lỗi được ép xử lý ở đâu mà Python cho phép lờ đi.

### Bài 7.4 — SSE stream parser
Viết parser Server-Sent Events async: nhận `impl AsyncRead` (hoặc stream of bytes), yield ra từng event `{event_type, data}` — đúng format streaming của Messages API (bài 2.1). Xử lý event bị cắt giữa 2 chunk mạng, comment lines, CRLF.
- **DoD:** unit test với chunk boundaries ác ý (cắt giữa `data:`, giữa JSON); parse đúng file capture từ một response streaming thật (lưu từ bài 2.1); zero-copy được chỗ nào thì làm (dùng `bytes::Bytes`).

### Bài 7.5 — Event bus với Tokio (bản Rust của bài 1.2)
`EventBus` dùng `tokio::sync::broadcast`: subscriber theo topic, publisher không bị chặn bởi subscriber chậm (hiểu ngữ nghĩa "lagged" của broadcast channel).
- **DoD:** test 2 subscriber cùng nhận; subscriber chậm bị lag được xử lý rõ ràng; ghi chú so sánh với EventBus Python — ai giữ state, ai copy data.

### Nâng cao (tùy chọn)
- Benchmark `rate_limiter` bằng `criterion`, tối ưu contention (thử `parking_lot`, atomics).
- Đọc source `tokio::sync::Semaphore` — hiểu waker và poll hoạt động thật.

## Câu hỏi diễn giải (phải tự trả lời được trước khi rời module)

1. Ownership giải quyết vấn đề gì mà cả GC (Python/Go) lẫn manual malloc/free (C) đều không giải quyết trọn? Chi phí phải trả là gì (thời gian compile? độ khó viết?)?
2. Vì sao borrow checker cấm "1 mutable reference + N immutable reference cùng lúc"? Cho một ví dụ bug cụ thể (iterator invalidation, data race) mà luật này chặn được ngay lúc compile.
3. `Result<T, E>` + `?` khác exception (Python) ở triết lý nào? Vì sao library nên dùng `thiserror` (lỗi có kiểu) còn application dùng `anyhow` (lỗi mờ)? Người **gọi** thư viện của bạn được gì từ lỗi có kiểu?
4. `Future` của Rust là **poll-based và lazy** — khác gì callback của JS và coroutine của Python (chạy ngay khi await)? Vì sao Rust cần runtime ngoài (Tokio) còn Python có sẵn asyncio trong stdlib — thiết kế "zero-cost" liên quan gì?
5. Cancellation ở Rust = **drop cái future**. So với `CancelledError` được ném vào coroutine của Python: bên nào cleanup dễ hơn, bên nào dễ gây bug "việc đang làm dở bị biến mất không dấu vết"? Liên hệ với `select!` — nhánh thua bị gì?
6. Khi nào dùng `Arc<Mutex<T>>` (shared state) vs channel (message passing)? Bài 7.5 bạn chọn gì cho EventBus — vì sao? Ngữ nghĩa "lagged" của `broadcast` channel là trade-off của quyết định nào?
7. Builder pattern trong bài 7.2: vì sao thư viện Rust chuộng builder thay vì hàm nhiều tham số Option? Nó liên quan gì đến backwards compatibility (thêm option mới không vỡ API cũ)?
8. Doctest là gì và vì sao nó "ăn hai chim một mũi tên" cho library author (docs không bao giờ outdated so với code)?
