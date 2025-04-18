from fastapi import FastAPI
import threading
import time

app = FastAPI()

stop_event = threading.Event()
threads = {}


@app.get("/hi")
def greet():
    return "Hello World"


def background_task(name: str, delay: float = 1.0):
    for i in range(1000):
        if stop_event.is_set():
            break
        time.sleep(delay)
        print(f"[{name}] 작업 {i + 1} 완료")



#스레드 시작
@app.get("/start-task")
def start_background_thread():
    name = "thread-worker " + str(len(threads) + 1)
    thread = threading.Thread(target=background_task, args=(name, 1),
                              name=name, daemon=True)
    threads[name] = thread
    thread.start()
    return {"status": "작업이 백그라운드에서 시작되었습니다."}

#모든 스레드 종료
@app.get("/stop-task")
def stop_background_thread():
    stop_event.set()
    return {"status": "task Stop"}

#실행중인 스레드 목록
@app.get("/workers")
def workers():
    return [
        {
            "name": name,
            "alive": t.is_alive(),
            "ident": t.ident
        }
        for name, t in threads.items()
        ]

# 중지된 스레드 제거
@app.get("/cleanup")
def clear_trash():
    dead_threads = [(name, t) for name, t in threads.items() if not t.is_alive()]

    for name, t, in dead_threads :
        del threads[name]

    return [
        {
            "name": name,
            "alive": t.is_alive(),
            "ident": t.ident
        }
        for name, t in dead_threads
    ]


# import pandas as pd
# import requests as requests
#
# url = "https://fapi.binance.com/fapi/v1/klines"
# params = {
#     "symbol": "BTCUSDT",
#     "interval": "1h",     # 1시간봉
#     "limit": 1000         # 최대 1000개
# }
#
# response = requests.get(url, params=params)
# data = response.json()
#
# # pandas로 정리
# df = pd.DataFrame(data, columns=[
#     "open_time", "open", "high", "low", "close", "volume",
#     "close_time", "quote_volume", "trades", "taker_base_vol",
#     "taker_quote_vol", "ignore"
# ])
#
# # 숫자로 변환
# df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
#
# # 시간 변환
# df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
# df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')
#
# print(df.head())
