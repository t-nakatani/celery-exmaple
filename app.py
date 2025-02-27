import time
from tasks import add, long_task, process_data


def main():
    print("Starting Celery example application...")

    # 例1: 単純な足し算タスク
    run_addition_example()

    # 例2: 長時間実行タスク
    run_long_task_example()

    # 例3: データ処理タスク
    run_data_processing_example()

    print("\nAll tasks submitted. The application will now keep running...")
    print("You can see task execution in the worker logs.")
    print("Press Ctrl+C to exit.")

    # アプリケーションを実行し続ける
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Application stopped.")


def run_addition_example():
    print("\nSubmitting addition task...")
    result = add.delay(4, 4)
    print(f"Task ID: {result.id}")
    print("Waiting for result...")

    # 結果を待つためのシンプルなポーリング
    wait_for_task_completion(result)
    print(f"Result: {result.get()}")


def run_long_task_example():
    print("\nSubmitting long running task...")
    result = long_task.delay(3)
    print(f"Task ID: {result.id}")
    print("This task will take 3 seconds. Moving on without waiting...")


def run_data_processing_example():
    print("\nSubmitting data processing task...")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = process_data.delay(data)
    print(f"Task ID: {result.id}")
    print("Waiting for result...")

    # 結果を待つためのシンプルなポーリング
    wait_for_task_completion(result)
    print(f"Result: {result.get()}")


def wait_for_task_completion(result):
    while not result.ready():
        print("Task still running...")
        time.sleep(1)


if __name__ == "__main__":
    # ワーカーの起動を待つ
    print("Waiting for Celery worker to initialize...")
    time.sleep(5)
    main()
