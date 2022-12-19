from typing import Callable

from pytoolkit.utils.retry import retry


def test_retry():

    def add_one():
        nonlocal num
        num += 1

    num = 0

    @retry
    def always_error(cb: Callable, exception=BaseException) -> None:
        cb()
        raise exception()

    try:
        always_error(add_one, TypeError)
    except TypeError:
        pass

    assert num == 2


def test_retry_with_max_tries():

    def add_one():
        nonlocal num
        num += 1

    num = 0
    max_tries = 5

    @retry(max_tries=max_tries)
    def always_error(cb: Callable, exception=BaseException) -> None:
        cb()
        raise exception()

    try:
        always_error(add_one, TypeError)
    except TypeError:
        pass

    assert num == max_tries


def test_retry_with_exceptions():

    exceptions = (TypeError, ValueError)

    def add_one():
        nonlocal num
        num += 1

    num = 0
    max_tries = 3

    @retry(max_tries=max_tries)
    def always_error(cb: Callable, exception=BaseException) -> None:
        cb()
        raise exception()

    try:
        always_error(add_one, TypeError)
    except exceptions:
        assert num == max_tries
        num = 0

    try:
        always_error(add_one, IndexError)
    except exceptions:
        assert num == max_tries
        num = 0

    try:
        always_error(add_one, LookupError)
    except LookupError:
        assert num == 1
        num = 0
