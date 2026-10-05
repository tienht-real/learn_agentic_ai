# Lộ trình AI Engineer / Agentic AI Engineer — Việt Nam & Quốc tế

Lộ trình được xây từ **3 nhóm JD** (khảo sát tháng 9–10/2026) để cân bằng giữa "đi làm được ngay ở VN" và "đủ chuẩn ứng tuyển công ty nước ngoài":

| Nhóm | Ví dụ công ty | Nhấn mạnh |
|---|---|---|
| **A. Doanh nghiệp VN** | Sun Group, FPT, CMC, MB Bank, VinSmart, Innotech, MiTek VN… | RAG, LangChain/LangGraph, tool calling, FastAPI, Docker; một phần còn đòi PyTorch/scikit-learn, OCR |
| **B. Công ty nước ngoài tại VN** | EPAM, Bosch, Axon Active, NAB, Money Forward, Zalo, Katalon… | Giống A về framework, **cộng thêm**: sở hữu cả vòng đời agent trên production (prototype → eval → deploy → monitor → iterate), eval pipeline, bảo mật/compliance, observability, tiếng Anh, dùng AI coding tool hằng ngày |
| **C. Công ty toàn cầu** | Anthropic, OpenAI, Stripe, Databricks, Google, Sierra, startup YC… | **Eval** (~9/12 JD), kỹ năng software engineering vững (~11/12), **TypeScript** (~7/12), làm việc với khách hàng, tự viết agent thay vì phụ thuộc framework |

> Số đếm ở nhóm B, C là đếm tay trên ~12 JD mỗi nhóm — xem là tín hiệu, không phải thống kê. Nguồn ở [cuối file](#nguồn).

**Kết luận rút ra:**
1. Nhóm A quyết định **nền tảng** (RAG, agent, FastAPI) — học kỹ để đi làm được ở VN.
2. Nhóm B, C quyết định **độ sâu và cách làm**: mọi thứ phải đo được bằng eval, có test/CI, debug được, giải thích được bằng tiếng Anh.
3. Framework giống nhau ở cả 3 nhóm — thứ phân biệt ứng viên là **eval + kỹ năng engineering**, không phải biết thêm framework.

---

## Ký hiệu mức độ

| Ký hiệu | Mức độ | Bar kiểm tra |
|---|---|---|
| 🔴 | **Chuyên sâu** | Tự làm không cần tra; giải thích được *tại sao*; trả lời được câu hỏi phỏng vấn đào sâu 3 tầng |
| 🟡 | **Nắm vững** | Làm được trong dự án thật, tra doc khi cần chi tiết |
| 🟢 | **Học qua** | Nói được nó là gì, dùng khi nào, so sánh với lựa chọn khác trong 2–3 câu |

Mức độ là **theo level**: cùng một chủ đề có thể 🟢 ở Level 1 và 🔴 ở Level 2.

---

## Ma trận kỹ năng

Cột A/B/C: mức độ xuất hiện trong JD (●●● rất thường gặp · ●● hay gặp · ● thỉnh thoảng · – hiếm). Cột L1/L2/L3: mức độ cần đạt ở từng level.

| Kỹ năng | A | B | C | L1 | L2 | L3 |
|---|---|---|---|---|---|---|
| Python + Pydantic | ●●● | ●●● | ●●● | 🔴 | 🔴 | 🔴 |
| LLM API, prompt, structured output | ●●● | ●●● | ●●● | 🔴 | 🔴 | 🔴 |
| RAG (chunking, embedding, vector DB, hybrid) | ●●● | ●● | ●● | 🔴 | 🔴 | 🔴 |
| Tool calling, agent loop tự viết | ●●● | ●●● | ●●● | 🔴 | 🔴 | 🔴 |
| LangChain / LangGraph | ●●● | ●● | ● | 🟡 | 🔴 | 🟡 |
| **Eval** (golden set, LLM-as-judge, phân tích lỗi, regression) | ●● | ●● | ●●● | 🔴 | 🔴 | 🔴 |
| Test, CI/CD, code review, debug code lạ | ● | ●● | ●●● | 🟡 | 🔴 | 🔴 |
| FastAPI, Docker | ●●● | ●● | ●● | 🔴 / 🟡 | 🔴 | 🔴 |
| SQL / Postgres / pgvector | ●● | ●● | ●● | 🟡 | 🟡 | 🟡 |
| Tiếng Anh kỹ thuật | ● | ●● | ●●● | 🟡 | 🔴 | 🔴 |
| AI coding tool (Claude Code, Cursor) + review code AI sinh | ● | ●● | ●● | 🟡 | 🟡 | 🔴 |
| Observability / tracing (Langfuse, LangSmith, OpenTelemetry) | ● | ●● | ●● | 🟢 | 🔴 | 🔴 |
| Bảo mật LLM: prompt injection, guardrails, PII | ● | ●● | ●● | 🟢 | 🔴 | 🔴 |
| Tối ưu chi phí / độ trễ | ● | ●● | ●● | 🟢 | 🟡 | 🔴 |
| MCP, multi-agent | ●● | ●● | ● | 🟢 | 🔴 | 🔴 |
| Cloud (Azure / AWS / GCP), Kubernetes | ●● | ●● | ● | 🟢 | 🟡 | 🔴 |
| Reliability: retry, idempotency, queue, checkpoint, job chạy lâu | ● | ●● | ●● | 🟢 | 🔴 | 🔴 |
| System design cho ứng dụng LLM | ● | ●● | ●●● | – | 🟡 | 🔴 |
| TypeScript / Node / React (Vercel AI SDK) | – | ● | ●●● | 🟢 | 🟡 | 🟡 |
| ML nền tảng (scikit-learn, PyTorch) | ●● | ● | ● | 🟢 | 🟢 | 🟡 |
| OCR / document AI | ●● | ● | – | 🟢 | 🟡 | 🟡 |
| Fine-tuning (LoRA/SFT), DSPy | ● | ● | ● | – | 🟢 | 🟡 |
| Data platform (Spark, Databricks, BigQuery) | ● | ● | ● | – | 🟢 | 🟢 |
| Làm việc với khách hàng / dịch bài toán nghiệp vụ | ● | ● | ●● | 🟢 | 🟡 | 🔴 |

---

## Tổng quan các level

| Level | Mục tiêu | Ứng tuyển | Thời lượng (10–15h/tuần) |
|---|---|---|---|
| [**Level 1**](level_1/README.md) | RAG + agent tự viết + FastAPI + Docker + **eval** + test/CI cơ bản | Intern / Junior (A, B); new-grad (C) | ~17 tuần |
| [**Level 2**](level_2/README.md) | Production: multi-agent, MCP, observability, eval tự động trong CI, guardrails, reliability, cloud, TypeScript | Mid (A, B, C) | *(chi tiết hoá sau L1)* |
| [**Level 3**](level_3/README.md) | System design, cost/latency ở scale, model mở, LLMOps, dẫn dắt; nhánh core libraries | Senior / Lead | *(chi tiết hoá sau L2)* |

**Giới hạn phạm vi:** không lộ trình nào khớp mọi JD. Các mảng chuyên biệt (Computer Vision sâu, speech, recommender, nghiên cứu model) nằm ngoài lộ trình này.

---

## Level 1 — tóm tắt

Chi tiết từng phase (kiến thức, bài tập, DoD, câu hỏi diễn giải) nằm trong README của phase.

| # | Phase | Tuần | 🔴 Chuyên sâu ở phase này |
|---|---|---|---|
| 00 | [Setup](level_1/00_setup/README.md) | 0.5 | — |
| 01 | [Python cho AI Engineer](level_1/01_python_foundations/README.md) | 2 | Python core, Pydantic |
| 02 | [ML & DL nền tảng](level_1/02_ml_foundations/README.md) | 1.5 | — (chủ yếu 🟢, vài 🟡) |
| 03 | [LLM API & Prompt](level_1/03_llm_api_prompt/README.md) | 2 | Token & tham số, messages, prompt engineering, structured output |
| 04 | [Embeddings & RAG](level_1/04_rag/README.md) ⭐ | 3 | Embedding, chunking, vector store, pipeline RAG có trích dẫn |
| 05 | [Tool calling & Agent](level_1/05_agent_basics/README.md) | 2.5 | Tool calling, **agent loop tự viết**, thiết kế tool |
| 06 | [Backend & Deploy](level_1/06_backend_deploy/README.md) | 2 | FastAPI |
| 07 | [Eval & chất lượng](level_1/07_eval_basics/README.md) ⭐ | 1.5 | Golden set, rubric, **phân tích lỗi** |
| 08 | [Capstone](level_1/08_capstone/README.md) | 2 | Gom tất cả: eval + CI + `DECISIONS.md` + README tiếng Anh |

## Kỹ năng song hành (chạy suốt Level 1, không phải phase riêng)

Nhóm B, C lọc ứng viên bằng những thứ này — không học dồn được, phải tích luỹ đều.

| Mức (L1) | Kỹ năng | Cách luyện |
|---|---|---|
| 🟡 | **Tiếng Anh kỹ thuật** | Đọc docs gốc (không đọc bản dịch); viết `NOTES.md` của phase 05 trở đi bằng tiếng Anh; cuối mỗi phase tự nói 2 phút bằng tiếng Anh giải thích thứ mình vừa xây |
| 🟡 | **Engineering practice** | Mỗi phase làm trên branch riêng → mở PR → tự review diff trước khi merge; từ phase 04 mọi module có test |
| 🟡 | **AI coding tool có kiểm soát** | Dùng Claude Code/Cursor để *tăng tốc* sau khi đã tự hiểu; mỗi đoạn AI sinh ra phải review được từng dòng (xem quy trình Feynman trong [README](README.md)) |
| 🟡 | **Giải thuật** | 3–5 bài LeetCode/tuần (big tech và một số công ty VN vẫn có vòng này) |
| 🟢 | **TypeScript** | Đọc hiểu được code TS; biết Vercel AI SDK là gì. Học thật ở Level 2 |

## Phỏng vấn — điều cần chuẩn bị

Quy trình phổ biến ở nhóm B, C (theo các guide bên thứ ba, chưa kiểm chứng trực tiếp):
- **Take-home: xây một agent** (có nơi yêu cầu *không dùng LangChain*) → chuẩn bị bằng phase 05 bài 5.1–5.3
- **Eval methodology** — *"eval là system design mới"*: golden set, LLM-as-judge, phân nhóm lỗi → phase 07
- **System design ứng dụng LLM** với ràng buộc token cost, latency, eval gate → Level 2
- **Debug codebase lạ**, live coding tăng dần → kỹ năng song hành + phase 01
- **Tình huống khách hàng** (vị trí Forward Deployed / Applied AI) → Level 2
- **LeetCode** vẫn có ở big tech và một số công ty VN

## Lương tham khảo

| Nhóm | Junior | Mid | Senior |
|---|---|---|---|
| A. Doanh nghiệp VN | ~15–30 triệu/tháng | ~35–55 triệu | — |
| B. Nước ngoài tại VN | ~30–50 triệu *(chưa kiểm chứng)* | ~50–85 triệu *(chưa kiểm chứng)* | ~85–125 triệu; ~$3.5–6k/tháng |
| Remote cho công ty nước ngoài | | ~$2.5–7k/tháng *(chưa kiểm chứng)* | |
| C. Toàn cầu (Mỹ) | new-grad ~$150–180k/năm (Sierra) | ~$125–210k | ~$200–325k |

Số liệu nhóm A lấy từ tin tuyển dụng công khai; nhóm B chủ yếu từ trang tổng hợp lương, không phải tin của nhà tuyển dụng — chỉ dùng để định hướng.

---

## Level 2 — khung

Nâng 🟢/🟡 của Level 1 lên 🔴, và thêm:
- **Eval nâng cao**: eval cho agent nhiều bước (trajectory, tool selection), pass@k, regression gate trong CI; Promptfoo / Braintrust / LangSmith
- **Observability**: tracing với Langfuse / OpenTelemetry; dashboard chi phí, độ trễ, tỉ lệ tool thành công
- **Agent harness hoàn chỉnh**: context management, memory dài hạn, checkpoint & resume, job chạy lâu
- **Multi-agent, LangGraph nâng cao, tự viết MCP server/client**
- **Guardrails & bảo mật**: prompt injection, PII, phân quyền tool, policy; nhận biết GDPR / EU AI Act
- **Advanced RAG**: reranking, query rewriting, parent–child chunk, document AI
- **Cloud & production**: Azure OpenAI / Bedrock / Vertex, CI/CD, Kubernetes cơ bản, caching, tối ưu chi phí
- **TypeScript + Next.js + Vercel AI SDK**: xây frontend/agent bằng TS
- **System design ứng dụng LLM** (mức Mid)
- Học qua: fine-tuning LoRA, DSPy, self-host vLLM/Ollama, data platform

## Level 3 — khung

- System design ở scale; tối ưu latency/cost; multi-tenant; fallback nhiều provider
- Fine-tuning & serving model mở trong production; LLMOps / MLOps
- Bảo mật, quản trị dữ liệu, compliance
- Dẫn dắt kỹ thuật, làm việc trực tiếp với khách hàng, mentoring
- Nhánh tuỳ chọn: **Core libraries cho agent** (Rust, PyO3, thư viện OSS — theo JD NVIDIA)

---

## Nguồn

**A. Doanh nghiệp VN**
- [Indeed VN — AI Agent jobs](https://vn.indeed.com/q-ai-agent-vi%E1%BB%87c-l%C3%A0m.html)
- [CareerViet — AI Engineer jobs](https://careerviet.vn/viec-lam/ai-engineer-k-vi.html) · [Sài Gòn Stec](https://careerviet.vn/vi/tim-viec-lam/ai-engineer.35C6EEED.html)
- [ITviec — Innotech AI Engineer Intern](https://itviec.com/it-jobs/good-english-ai-engineer-intern-ai-agents-llm-rag-innotech-vietnam-corporation-3040) · [MiTek Senior AI Engineer](https://itviec.com/it-jobs/senior-ai-engineer-agentic-ai-mlops-mitek-vietnam-5058) · [LLM jobs](https://itviec.com/it-jobs/llm)

**B. Công ty nước ngoài tại VN**
- [EPAM — AI Engineer (LLM)](https://careers.epam.com/en/vacancy/ai-engineer-llm-blt4i4hdf4z0f1vvp3w_en)
- [Axon Active — AI Engineer](https://www.careers.axonactive.com/post/ai-engineer-td)
- [Bosch — R&D AI Engineer (AI Agent)](https://jobs.smartrecruiters.com/BoschGroup/744000129087789--r-d-ai-engineer-focus-ai-agent-) · [Bosch — AI Engineer Supply Chain](https://jobs.smartrecruiters.com/BoschGroup/744000136154462-ai-engineer-supply-chain) *(đã đóng)*
- [Zalo — (Lead) Senior AI Engineer LLM/Agent](https://zalo.careers/job/lead-senior-ai-engineer-llm-agent-n-laRXNoVpJYwhW9v1)
- [Money Forward VN](https://itviec.com/companies/money-forward-vietnam-co-ltd) *(tin đã hết hạn, chi tiết từ snippet)*
- [NAB — Senior AI Engineer](https://freehire.me/jobs/senior-ai-engineer-ai-platforms-nab-a4xcsiru) *(qua trang tổng hợp)*
- Lương: [Nucamp](https://www.nucamp.co/blog/coding-bootcamp-viet-nam-vnm-top-10-best-paid-tech-job-in-viet-nam-in-2025) · [Jesson Global](https://www.jessonglobal.com/insights/landed-cost-benchmarks-for-hiring-senior-ai-engineers-in-vietnam-for-singapore-enterprises-in-2026) · [VietnamDevs](https://vietnamdevs.com/blog/vietnam-software-developer-salaries-2026-guide-for-international-recruiters)

**C. Công ty toàn cầu**
- [OpenAI — SWE Applied Evals](https://openai.com/careers/software-engineer-applied-evals/) · [OpenAI — Forward Deployed Engineer](https://openai.com/careers/forward-deployed-engineer-(fde)-sf-san-francisco/)
- [Anthropic — Applied AI Engineer](https://jobs.generalcatalyst.com/companies/anthropic/jobs/70950856-applied-ai-engineer-startups) *(bản sao trên trang tổng hợp)*
- [Stripe — AI Engineer](https://stripe.com/careers/listing/ai-engineer/8044460)
- [Databricks — AI Engineer FDE](https://www.databricks.com/company/careers/professional-services-operations/ai-engineer---fde-forward-deployed-engineer-8546367002)
- [Google — SWE Agentic AI Infrastructure](https://jobs.anitab.org/companies/google-24698/jobs/76056040-software-engineer-agentic-ai-infrastructure)
- [Fieldguide — AI Engineer Quality](https://jobs.8vc.com/companies/fieldguide/jobs/68132699-ai-engineer-quality)
- [Sierra — Agent Engineer](https://jobs.ashbyhq.com/Sierra/1a0a0334-41f8-4c15-9ed8-615336855e5e)
- YC: [Vector Legal](https://www.workatastartup.com/jobs/95799) · [KelAI](https://www.workatastartup.com/jobs/99248) · [Voiceops](https://www.workatastartup.com/jobs/95123)
- Phỏng vấn: [AI Engineering Field Guide — interview process](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/01-interview-process.md) · [Sierra FDE interview](https://vibeengines.com/handbook/fde-interview-sierra)

**So sánh title**
- [ODSC — AI Engineering vs Agentic Engineering](https://opendatascience.com/ai-engineering-and-agentic-engineering-what-separates-the-two/) · [AI Job Title Reference Guide 2026](https://www.ivanturkovic.com/the-ai-job-title-reference-guide-2026/) · [Agentic AI Job Titles Explained](https://agenticengineeringjobs.com/guides/agentic-ai-job-titles-explained)
