import threading
from typing import Callable

global_lock = threading.Lock()


def deamon_thread(task: Callable):
    """
    Run this task in a deamon thread.

    :param task: a callable object
    :return: a function object that will launch the given task in a deamon thread when it is called
    """

    def threaded_task(*args, **kwargs):
        thread = threading.Thread(target=task, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    return threaded_task


if __name__ == "__main__":
    import time

    @deamon_thread
    class Test:
        def __init__(self, _id: str):
            self.id = _id
            self.__timed_loop__(wait=0.5)

        def __timed_loop__(self, wait: float):
            while True:
                with global_lock:
                    print(f"Hello from {self.id}!")
                time.sleep(wait)

    Test("Bob")
    Test("Alice")
    time.sleep(1)
