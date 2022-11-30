import inspect
import uuid

from pytoolkit.utils.singleton import SingletonMetaClass, singleton


@singleton
class _Class:

    def __init__(self):
        self.val = uuid.uuid4().hex


class __Class(metaclass=SingletonMetaClass):

    def __init__(self):
        self.val = uuid.uuid4().hex


def test_singleton():
    var = _Class()
    newVar = _Class()

    assert var == newVar
    assert var.val == newVar.val
    assert id(var) == id(newVar)

    assert _Class().val == var.val
    assert var.val == _Class().val
    assert id(var) == id(_Class())

    assert inspect.isclass(_Class)


def test_singleton_metaclass():
    _Class = __Class
    var = _Class()
    newVar = _Class()

    assert var == newVar
    assert var.val == newVar.val
    assert id(var) == id(newVar)

    assert _Class().val == var.val
    assert var.val == _Class().val
    assert id(var) == id(_Class())

    assert inspect.isclass(_Class)
