import time

from pytoolkit.sync.timer import LoopTimer


def test_loop_timer():
    n = 0

    def worker():
        nonlocal n
        n += 1

    t = LoopTimer(0.5, worker)
    t.start()
    time.sleep(2.1)
    t.cancel()
    time.sleep(1)
    assert n == 4, n
