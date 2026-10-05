# Level 3 — Senior / Lead *(đang ở dạng khung)*

**Mục tiêu:** thiết kế hệ thống AI ở scale, tối ưu chi phí/độ trễ, làm chủ model mở (fine-tune, serving), LLMOps, dẫn dắt kỹ thuật.
**Ứng tuyển được:** Senior / Lead / Staff AI Engineer.

> Sẽ chi tiết hoá khi hoàn thành Level 2.

## Phần lõi (dự kiến)
- System design cho ứng dụng AI: multi-tenant, queue, caching, rate limit, fallback giữa nhiều provider
- Tối ưu latency/cost ở scale; capacity planning
- Fine-tuning (LoRA/QLoRA) & serving model mở trong production (vLLM, TensorRT-LLM)
- LLMOps / MLOps: versioning prompt/model/dataset, monitoring drift, A/B test
- Bảo mật, quản trị dữ liệu, compliance
- Dẫn dắt kỹ thuật: design review, mentoring, viết RFC

## Nhánh chuyên sâu tuỳ chọn — Core libraries cho agent (theo JD NVIDIA)

Nhánh dành cho vị trí kiểu *"Software Engineer, Core Libraries for Agentic Applications"* — **xây thư viện/công cụ cho agent**, không chỉ dùng agent. Hầu như không xuất hiện trong JD trong nước, nhưng là lợi thế lớn với công ty sản phẩm/hạ tầng AI toàn cầu.

| # | Module | Nội dung |
|---|---|---|
| 01 | [Rust core](01_rust_core/README.md) | Rust cơ bản → async Rust (Tokio), serde, thiết kế API library |
| 02 | [Rust ↔ Python bindings](02_rust_python_bindings/README.md) | PyO3, maturin, đo overhead qua ranh giới ngôn ngữ |
| 03 | [Capstone `agentlens`](03_capstone_agent_toolkit/README.md) | Thư viện tracing + evals + guardrails, core Rust, chuẩn open source |

Nhánh này xây trên Level 2 (module 01–06). Các README dùng số module cũ — tra bảng ở [Level 2](../level_2/README.md#lưu-ý-khi-đọc-các-module-cũ).

### JD gốc → nhóm kỹ năng

| Yêu cầu trong JD NVIDIA | Nhóm kỹ năng | Ở đâu |
|---|---|---|
| "asynchronous programming, callbacks, request lifecycles, event-driven systems" | Async & event-driven | L1/01, L2/01 |
| "LLM applications, agent workflows, tool calls, model-provider APIs" | LLM API & tool calling | L1/03, L1/05 |
| "agent architectures, agent frameworks and agent harnesses" | Agent harness + framework | L2/02, L2/03 |
| "OpenTelemetry, tracing, structured events, exporters…" | Observability | L2/04 |
| "evaluation/benchmarking systems for agent workflows" | Evals & benchmark | L2/05 |
| "Rust systems work, async Rust, Tokio, serde… PyO3, maturin" | Rust + bindings | L3/01, L3/02 |
| "Middleware, plugin systems, guardrails, policy engines" | Middleware & guardrails | L2/06 |
| "maintaining open-source libraries, SDKs" | Tổng hợp | L3/03 |
