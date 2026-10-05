# L1.02 — ML & Deep Learning nền tảng (1.5 tuần)

> JD VN: một phần tin (ngân hàng, tập đoàn lớn) vẫn ghi *"PyTorch, TensorFlow, scikit-learn"*.

Mục tiêu **không phải** để train model. Mục tiêu là (1) qua vòng lọc CV và câu hỏi phỏng vấn nền tảng, (2) hiểu embedding và metric — hai thứ dùng trực tiếp ở RAG (phase 04) và eval (phase 07). Phase này phần lớn là 🟢 — học đủ, đừng sa đà.

## Kiến thức cần học

| Mức | Chủ đề |
|---|---|
| 🟡 | Vector, dot product, **cosine similarity** — nền tảng của embedding search |
| 🟡 | Metric: accuracy, precision, recall, F1, confusion matrix — dùng lại để đo retrieval và eval |
| 🟡 | `numpy`, `pandas` cơ bản: đọc CSV, lọc, group, thống kê |
| 🟢 | Khái niệm ML: supervised / unsupervised, train/val/test, overfitting / underfitting |
| 🟢 | `scikit-learn`: train một classifier, đánh giá bằng F1 |
| 🟢 | Neural network: neuron, layer, loss, gradient descent, backprop — mức trực giác |
| 🟢 | Transformer & LLM: attention, pre-training vs fine-tuning, LLM "đoán token tiếp theo" nghĩa là gì |
| 🟢 | `PyTorch`: tensor, một training loop nhỏ |

**Tài liệu:**
- [3Blue1Brown — Neural Networks](https://www.3blue1brown.com/topics/neural-networks) (bao gồm 2 video về Transformer)
- Andrej Karpathy — *Intro to Large Language Models* (YouTube, ~1 giờ)
- [scikit-learn — Getting started](https://scikit-learn.org/stable/getting_started.html)
- [PyTorch — Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)

## Bài tập

### Bài 2.1 — Phân loại văn bản tiếng Việt
Notebook: phân loại review tiếng Việt (tích cực/tiêu cực) bằng scikit-learn — `TfidfVectorizer` + `LogisticRegression`. Chia train/test, báo cáo precision/recall/F1 và confusion matrix.
- **DoD:** F1 trên tập test; giải thích được 3 ví dụ bị phân loại sai và vì sao.

### Bài 2.2 — Cosine similarity bằng tay
Lấy embedding của 6 câu (2 nhóm chủ đề khác nhau) qua API embedding (hoặc `sentence-transformers` local). Tự viết hàm cosine similarity bằng numpy, in ma trận 6×6.
- **DoD:** các câu cùng chủ đề có similarity cao hơn rõ rệt; giải thích vì sao dùng cosine chứ không dùng khoảng cách Euclid thuần.
- Có thể làm sau phase 03 khi đã quen gọi API.

### Bài 2.3 — PyTorch hello world (🟢)
Theo tutorial "Learn the Basics": train một mạng nhỏ trên FashionMNIST.
- **DoD:** chạy được; giải thích được 4 bước của một training loop (forward → loss → backward → step).

## Câu hỏi diễn giải

1. Precision khác recall thế nào? Hệ thống RAG nên ưu tiên cái nào khi lấy tài liệu — vì sao?
2. Overfitting là gì? Vì sao cần tập test tách riêng?
3. Embedding là gì? Vì sao hai câu khác chữ nhưng cùng nghĩa lại có vector gần nhau?
4. LLM "đoán token tiếp theo" — vậy tại sao nó trả lời được câu hỏi? Hallucination sinh ra từ đâu trong cơ chế này?
5. Pre-training, fine-tuning, và RAG khác nhau thế nào? Khi nào chọn cái nào?
