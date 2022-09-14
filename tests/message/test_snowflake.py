import random

from pytoolkit.message.snowflake import Snowflake


def test_snowflake():
    msgs = []
    count = random.randint(100, 1000)
    generate = Snowflake().generate
    for _ in range(count):
        msgs.append(generate())
    assert len(msgs) == len(set(msgs))
