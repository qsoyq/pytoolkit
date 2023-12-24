from typing import Any, Type


def singleton(cls: Type) -> Type:
    instance = None
    _new = cls.__new__

    def _init(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def get_instance(_cls: Type[Any], *args: Any, **kwargs: Any) -> object:
        nonlocal instance, _new, _init
        if instance is None:
            instance = _new(_cls, *args, **kwargs)
        else:
            setattr(instance.__class__, "__init__", _init)
        return instance

    cls.__new__ = get_instance  # type: ignore
    return cls


class SingletonMetaClass(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance
