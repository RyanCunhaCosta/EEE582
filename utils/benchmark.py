import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def end(self):
        if self.start_time is None:
            raise ValueError("Benchmark não iniciado. Chame 'start' antes de 'end'.")

        self.end_time = time.perf_counter()
        elapsed_time = self.end_time - self.start_time

        print(f"\n\tTempo de execução: {elapsed_time * 1000:.6f} ms.")
