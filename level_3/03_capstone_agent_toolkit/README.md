# 10 — Capstone: `agentlens` — thư viện quan sát & đánh giá agent

> 📍 **Level 3 / 03 — nhánh tuỳ chọn.** Số module cũ nhắc trong bài → tra [bảng ánh xạ](../../level_2/README.md#lưu-ý-khi-đọc-các-module-cũ).

> JD, phần "What you'll be doing": *"Develop open-source libraries and tools which accelerate and optimize agent harnesses and frameworks… backed by evaluations, benchmarking, and feedback loops."*

Capstone gom mọi thứ bạn đã xây thành **một thư viện open-source đúng nghĩa** — thứ bạn có thể đưa link GitHub vào CV và nói chuyện suốt buổi phỏng vấn. Tên gợi ý: `agentlens` (đặt tên khác tuỳ bạn).

## Sản phẩm

Một package Python (core nóng bằng Rust) làm được 3 việc cho **agent bất kỳ**:

```python
import agentlens

# 1. Instrument — một dòng, không sửa code agent
agentlens.install(exporters=["otlp", "jsonl"])

# 2. Guard — middleware + policy
agentlens.guard(policy="policy.yaml")

# 3. Eval — CLI
# $ agentlens eval tasks/ --agent "python my_agent.py" --runs 3 --report out.html
```

### Thành phần (map về các module)

| Thành phần | Từ module | Yêu cầu nâng lên mức thư viện |
|---|---|---|
| Auto-instrument SDK anthropic (+ 1 framework: LangGraph hoặc OpenAI SDK) | 05 | API `install()/uninstall()` sạch; GenAI semconv; test không-đổi-hành-vi |
| Structured events + exporters (OTLP, JSONL, SQLite) | 05 | Exporter interface public để người dùng tự viết exporter |
| Middleware + policy engine + guardrails có sẵn (redaction, tool allowlist) | 09 | Plugin qua entry points; policy YAML documented |
| Eval harness + regression gate + báo cáo HTML | 06 | CLI `agentlens eval`; chạy được với agent là **subprocess bất kỳ** (giao tiếp qua protocol đơn giản), không chỉ mini_agent |
| Hot path Rust: text chunking, token estimate, redaction regex engine, SSE parse | 07, 08 | Fallback pure-Python khi không có wheel; benchmark chứng minh con số |

## Yêu cầu chất lượng (đây mới là phần khó)

1. **API design** — public API nhỏ, đặt tên nhất quán, semver ngay từ 0.1; viết `DESIGN.md` giải thích các quyết định (JD: *"design or extend cross-language APIs with attention to consistency, usability, stability, and backwards compatibility"*).
2. **Tests** — coverage ≥ 80% cho core; test không-đổi-hành-vi cho instrumentation; eval regression gate tự ăn chính nó (dogfooding).
3. **CI (GitHub Actions)** — lint (ruff, clippy), test matrix 2 phiên bản Python, build wheel bằng maturin, benchmark job đăng số liệu vào PR comment.
4. **Docs** — README có GIF/demo 30 giây, quickstart ≤ 5 dòng code, trang docs cho từng thành phần, CHANGELOG.
5. **Benchmark công khai** — trang `BENCHMARKS.md`: overhead của instrumentation (% latency thêm vào mỗi LLM call — phải đo, và phải nhỏ), tốc độ chunker Rust vs Python, chi phí policy engine với 1000 rules.
6. **Publish** — đẩy lên TestPyPI (hoặc PyPI thật nếu tự tin); cài từ pip trên máy sạch phải chạy.

## Lộ trình 4–6 tuần

- **Tuần 1:** chốt scope + API design (viết `DESIGN.md` trước khi code — bắt buộc); dựng skeleton repo, CI, cấu trúc mixed Rust/Python.
- **Tuần 2–3:** port instrumentation + events + exporters; test không-đổi-hành-vi.
- **Tuần 3–4:** port middleware/policy/guardrails; eval CLI với subprocess protocol.
- **Tuần 5:** Rust hot paths + benchmark; hoàn thiện docs.
- **Tuần 6:** polish, publish, viết một bài blog/README dài kể câu chuyện (kiến trúc, số đo, trade-offs) — đây là "portfolio piece" của bạn.

## DoD cuối cùng

- [ ] Người lạ đọc README cài và chạy được quickstart trong < 10 phút.
- [ ] `agentlens.install()` instrument một script dùng SDK anthropic **chưa từng thấy** mà không sửa dòng nào.
- [ ] `agentlens eval` chấm được một agent bạn không viết (vd: agent LangGraph của bài 4.1).
- [ ] Có ít nhất 3 con số benchmark bạn tự tin bảo vệ trong phỏng vấn.
- [ ] CI xanh, wheel cài được, tag v0.1.0.

Xong capstone, quay lại đọc JD một lần nữa — bạn sẽ thấy mình có ví dụ cụ thể cho **từng gạch đầu dòng**.

## Câu hỏi diễn giải (chuẩn bị cho phỏng vấn — trả lời như đang bảo vệ thiết kế)

1. Vì sao public API càng nhỏ càng dễ giữ backwards compatibility? Cho ví dụ một thứ bạn **cố tình không** export trong `agentlens` và lý do.
2. Semver: đổi gì thì bump patch/minor/major? Đổi format của structured event JSON là loại thay đổi nào — vì sao (ai đang phụ thuộc vào nó)?
3. Overhead của instrumentation: bạn đo thế nào cho công bằng (cùng workload, warm-up, nhiều run)? Con số của bạn là bao nhiêu % và vì sao người dùng nên tin phép đo đó?
4. Thiết kế "fallback pure-Python khi không có Rust wheel": quyết định này đánh đổi gì? Làm sao test để hai đường chạy cho kết quả **giống hệt nhau**?
5. Eval CLI của bạn nói chuyện với agent qua subprocess protocol — vì sao chọn thiết kế đó thay vì import agent như Python object? (Gợi ý: agent viết bằng ngôn ngữ khác? framework khác? cách ly crash?)
6. Kể lại một quyết định thiết kế trong `DESIGN.md` mà bạn đã **đổi ý** giữa chừng: lý do ban đầu, cái gì làm bạn đổi, bài học. (Câu chuyện thật kiểu này ăn điểm phỏng vấn hơn mọi lý thuyết.)
