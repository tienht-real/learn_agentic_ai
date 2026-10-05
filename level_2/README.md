# Level 2 — AI Engineer (Mid) *(đang ở dạng khung)*

**Mục tiêu:** hệ thống agent đạt chuẩn production — multi-agent, MCP, observability, eval tự động, guardrails, deploy cloud.
**Ứng tuyển được:** AI Engineer / Agentic AI Engineer Mid-level.

> Level này sẽ được chi tiết hoá (thêm thời lượng, sắp lại thứ tự, bổ sung module mới) khi bạn hoàn thành Level 1. Các module dưới đây được chuyển từ lộ trình cũ và **đã có nội dung đầy đủ** — học được ngay nếu muốn đi trước.

## Module hiện có

| # | Module | Nội dung |
|---|---|---|
| 01 | [Async nâng cao](01_async_advanced/README.md) | Event bus, middleware chain (onion model), `contextvars` |
| 02 | [Agent harness](02_agent_harness/README.md) | Tự xây coding agent: tool surface, context management, safety, tự chấm harness |
| 03 | [Frameworks & MCP](03_frameworks_mcp/README.md) | LangGraph nâng cao + framework thứ hai, **tự viết MCP server/client**, multi-agent supervisor |
| 04 | [Observability](04_observability/README.md) | OpenTelemetry, GenAI semantic conventions, Jaeger, instrument SDK bên thứ ba |
| 05 | [Evaluation](05_evaluation/README.md) | Eval harness cho agent, LLM-as-judge có calibration, pass@k, regression gate trong CI |
| 06 | [Guardrails](06_guardrails/README.md) | Middleware cho agent, policy engine, PII redaction, chống prompt injection, plugin system |

## Module dự kiến bổ sung
Theo [ma trận kỹ năng](../ROADMAP_VN.md#ma-trận-kỹ-năng) — ưu tiên những gì công ty nước ngoài/toàn cầu đòi mà Level 1 mới ở mức 🟢:
- **Reliability**: idempotency, queue, checkpoint & resume agent, job chạy lâu
- **System design ứng dụng LLM** (mức Mid): ràng buộc token cost, latency, eval gate
- **TypeScript + Next.js + Vercel AI SDK**: frontend và agent bằng TS (~7/12 JD toàn cầu)
- **Advanced RAG**: reranking, query rewriting, parent–child chunk, document AI/OCR sâu, GraphRAG
- **Cloud & production**: Azure OpenAI / AWS Bedrock / GCP Vertex, Kubernetes cơ bản, caching, tối ưu chi phí
- **Bảo mật & compliance**: phân quyền tool, nhận biết GDPR / EU AI Act (bổ sung cho module 06)
- **Học qua**: fine-tuning LoRA, DSPy, self-host vLLM/Ollama, data platform (Spark, Databricks)

## Lưu ý khi đọc các module cũ
Các README trong level này được viết cho lộ trình cũ nên:
- Gọi API bằng **Anthropic SDK**. Repo hiện dùng API tương thích OpenAI (`shared/client.py`) — chuyển đổi tương tự bài 5.1 Level 1, hoặc dùng Anthropic key.
- Nhắc đến số module/bài cũ. Bảng tra:

| Số cũ | Vị trí mới |
|---|---|
| module `01` (bài 1.1, 1.3) | [Level 1 / 01](../level_1/01_python_foundations/README.md) |
| module `01` (bài 1.2, 1.4, 1.5) | Level 2 / 01 |
| module `02` | [Level 1 / 03](../level_1/03_llm_api_prompt/README.md) (bài 2.1, 2.2, 2.4, 2.5) và [Level 1 / 05](../level_1/05_agent_basics/README.md) (bài 2.3) |
| module `03` | Level 2 / 02 (bài 3.1 đã có phiên bản ở Level 1 / 05 bài 5.2) |
| module `04` | Level 2 / 03 |
| module `05` | Level 2 / 04 |
| module `06` | Level 2 / 05 |
| module `07`, `08` | [Level 3 / 01, 02](../level_3/README.md) |
| module `09` | Level 2 / 06 |
| module `10` | Level 3 / 03 |
