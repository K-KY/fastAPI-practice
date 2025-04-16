from fastapi import FastAPI
import threading
import time

app = FastAPI()

stop_event = threading.Event()

@app.get("/hi")
def greet():
    return "Hello World"


def background_task(name: str, delay: float = 1.0):
    for i in range(1000):
        if stop_event.is_set():
            break
        time.sleep(delay)
        print(f"[{name}] 작업 {i + 1} 완료")


@app.get("/start-task")
def start_background_thread():
    thread = threading.Thread(target=background_task, args=("백그라운드 작업", 1), daemon=True)
    thread.start()
    return {"status": "작업이 백그라운드에서 시작되었습니다."}


@app.get("/stop-task")
def stop_background_thread():
    stop_event.set()
    return {"status" : "task Stop"}
