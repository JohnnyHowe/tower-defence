import time

class _Clock:

    start_time: float
    last_frame_time: float
    dt: float       # seconds
    min_dt = 0.00001  # 1 ms

    def __init__(self):
        self.start_time = time.time()
        self.last_frame_time = self.start_time
        self.update()

    def update(self):
        now = time.time()
        self.dt = max(self.min_dt, now - self.last_frame_time)
        self.last_frame_time = now


Clock = _Clock()