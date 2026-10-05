"""Bài 1.1 — Concurrent fetcher.

Yêu cầu:
- Tải nhiều URL đồng thời, giới hạn số request chạy song song bằng Semaphore.
- Timeout mỗi request (asyncio.timeout).
- Retry với exponential backoff + jitter cho lỗi mạng / HTTP 5xx (không retry 4xx).
- Một URL lỗi hẳn (hết retry) trả về FetchResult(error=...) thay vì làm sập batch.
- Kết quả giữ đúng thứ tự của danh sách URL đầu vào.

Chạy: uv add httpx && uv run ex01_concurrent_fetcher.py

────────────────────────────────────────────────────────────────────
GIẢI THÍCH THIẾT KẾ (đọc trước khi code — và tự hỏi: bỏ đi thì sao?)
────────────────────────────────────────────────────────────────────
Mỗi lựa chọn trong skeleton này đều có lý do. Sau khi làm xong, bạn phải
diễn đạt lại được từng ý dưới đây mà không nhìn file.
"""

import asyncio
import time
from dataclasses import dataclass

import httpx


# WHY dataclass thay vì raise exception?
# Đây là bài toán BATCH: 1 URL hỏng không được phép giết 49 URL còn lại.
# Nếu fetch_one raise, exception sẽ thoát ra khỏi gather và cả batch sập
# (hoặc bạn phải dùng return_exceptions=True rồi phân loại lộn xộn).
# Trả về "kết quả lỗi" như một GIÁ TRỊ biến lỗi thành dữ liệu — người gọi
# xử lý đồng nhất mọi phần tử. (Rust bắt buộc kiểu tư duy này với Result<T, E>
# — bạn sẽ gặp lại ở module 07.)
@dataclass
class FetchResult:
    url: str
    status: int | None = None
    elapsed_ms: float | None = None
    error: str | None = None


# WHY nhận `client` và `sem` từ ngoài vào (dependency injection) thay vì tự tạo?
# - client: httpx.AsyncClient giữ CONNECTION POOL. Tạo client mới mỗi request
#   = bắt tay TCP/TLS lại từ đầu mỗi lần, mất luôn lợi ích keep-alive.
#   Một client dùng chung cho cả batch là pattern chuẩn.
# - sem: Semaphore phải là MỘT object dùng chung thì mới giới hạn được tổng
#   concurrency. Mỗi coroutine tự tạo semaphore riêng thì ai cũng "còn slot".
async def fetch_one(
    client: httpx.AsyncClient,
    url: str,
    sem: asyncio.Semaphore,
    *,
    timeout_s: float = 10.0,
    max_retries: int = 3,
) -> FetchResult:
    # TODO:
    # 1. async with sem: giới hạn concurrency
    #    WHY đặt sem Ở ĐÂY (trong fetch_one) chứ không quanh gather?
    #    gather phải TẠO đủ 50 task ngay để giữ đúng thứ tự kết quả;
    #    thứ bị giới hạn là số task đang thực sự chạy I/O — tức là đoạn
    #    code này. 40 task còn lại "tồn tại nhưng ngủ" ở dòng async with.
    #
    # 2. vòng retry: for attempt in range(max_retries + 1)
    #
    # 3. asyncio.timeout(timeout_s) bao quanh client.get(url)
    #    WHY cần timeout riêng khi httpx đã có timeout? Để bạn tự tay dùng
    #    asyncio.timeout và hiểu nó cancel coroutine bên trong thế nào —
    #    CancelledError được ném vào đúng chỗ đang await.
    #
    # 4. 5xx hoặc lỗi mạng -> backoff = base * 2**attempt + random jitter, rồi retry
    #    WHY exponential? Server đang quá tải — dồn dập retry đều đặn chỉ làm
    #    nó chết hẳn. WHY jitter? 50 client cùng fail lúc t=0 và cùng retry
    #    lúc t=1s, t=2s... sẽ tạo "thundering herd" — sóng request đập cùng
    #    nhịp. Jitter phá vỡ sự đồng pha đó.
    #
    # 5. 4xx -> trả về ngay, không retry
    #    WHY? 4xx nghĩa là REQUEST SAI (lỗi của mình): gửi lại y nguyên thì
    #    vẫn sai y nguyên. Chỉ retry lỗi TẠM THỜI (mạng, 5xx, timeout).
    #    Retry 404 ba lần = đốt thời gian + spam server.
    #
    # 6. hết retry -> FetchResult(url, error=...)
    raise NotImplementedError


async def fetch_all(urls: list[str], max_concurrency: int = 10) -> list[FetchResult]:
    # TODO: tạo Semaphore + httpx.AsyncClient (async with — WHY? để pool được
    # đóng tử tế kể cả khi có exception), chạy fetch_one cho mọi URL bằng
    # asyncio.gather (hoặc TaskGroup).
    #
    # WHY gather giữ đúng thứ tự? gather trả kết quả theo THỨ TỰ TASK ĐƯỢC
    # TRUYỀN VÀO, không phải thứ tự hoàn thành. URL thứ 3 xong cuối cùng thì
    # kết quả của nó vẫn nằm ở index 3. (So sánh: asyncio.as_completed thì
    # trả theo thứ tự xong trước — dùng khi muốn xử lý sớm nhất có thể.)
    raise NotImplementedError


async def main() -> None:
    urls = [f"https://httpbin.org/delay/{i % 3}" for i in range(20)]
    urls.insert(5, "https://httpbin.org/status/500")   # sẽ retry rồi fail
    urls.insert(10, "https://httpbin.org/status/404")  # fail ngay, không retry

    # WHY time.perf_counter chứ không time.time?
    # perf_counter là đồng hồ đơn điệu (monotonic) độ phân giải cao, sinh ra
    # để đo khoảng thời gian; time.time có thể bị NTP/chỉnh giờ kéo lùi.
    t0 = time.perf_counter()
    results = await fetch_all(urls, max_concurrency=10)
    total = time.perf_counter() - t0

    ok = sum(1 for r in results if r.error is None)
    print(f"{ok}/{len(results)} OK trong {total:.1f}s")
    for r in results:
        print(f"  {r.url}  status={r.status}  error={r.error}")

    # TỰ KIỂM TRA sau khi chạy được:
    # - Đặt max_concurrency=1 rồi 20: tổng thời gian đổi thế nào? Giải thích
    #   con số bằng miệng (20 URL delay 0/1/2s, chạy tuần tự = ? giây).
    # - Nếu bạn quên `await` trong `async with sem`, bug biểu hiện ra sao?


if __name__ == "__main__":
    asyncio.run(main())
