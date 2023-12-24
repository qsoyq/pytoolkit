import threading
import time

from typing import Tuple

TIMESTAMP_BIT_COUNT = 41
WORKID_BIT_COUNT = 10
SEQUENCE_BIT_COUNT = 12

WORKID_LEFT_MOVE = SEQUENCE_BIT_COUNT
TIMESTAMP_LEFT_MOVE = WORKID_LEFT_MOVE + WORKID_BIT_COUNT

MAX_WORKID_NUM = 1 << WORKID_BIT_COUNT
MAX_SEQUENCE_NUM = 1 << SEQUENCE_BIT_COUNT


def get_time_ms() -> int:
    return int(time.time() * 1000)


def get_next_time_ms(ms: int) -> int:
    now = get_time_ms()
    while now <= ms:
        now = get_time_ms()
    return now


class Snowflake:
    MUTEX: threading.Lock = threading.Lock()
    TIMESTAMP = get_time_ms()
    SEQUENCE = 0

    def __init__(self, *, workid: int = 0):
        assert 0 <= workid < 1024
        self._workid = workid

    def generate(self) -> int:
        with self.MUTEX:
            now = get_time_ms()
            if now == self.__class__.TIMESTAMP:
                self.__class__.SEQUENCE += 1
                if self.__class__.SEQUENCE >= MAX_SEQUENCE_NUM:
                    self.__class__.TIMESTAMP = get_next_time_ms(now)
                    self.__class__.SEQUENCE = 0

            elif now > self.__class__.TIMESTAMP:
                self.__class__.SEQUENCE = 0
                self.__class__.TIMESTAMP = now

            else:
                raise ValueError("时间戳错误")
            return (
                self.__class__.TIMESTAMP << TIMESTAMP_LEFT_MOVE
                | self._workid << WORKID_LEFT_MOVE
                | self.__class__.SEQUENCE
            )

    def split(self, uid: int) -> Tuple[int, int, int]:
        timestamp = uid >> TIMESTAMP_LEFT_MOVE
        workid = (uid >> WORKID_LEFT_MOVE) & (MAX_WORKID_NUM - 1)
        sequence = uid & (MAX_WORKID_NUM - 1)
        return timestamp, workid, sequence
