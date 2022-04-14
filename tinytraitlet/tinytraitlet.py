from functools import wraps
from typing import Any


class Model:
    default_value = None
    __is_trait__ = True
    model_type: Any

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        try:
            res = getattr(obj, self.private_name)
        except AttributeError:
            res = self.default_value
        return res

    def __set__(self, obj, value):
        self.validate(value)
        try:
            obj.validators[self.public_name](obj, value)
        except KeyError:
            pass
        setattr(obj, self.private_name, value)

    def validate(self, value):
        if not isinstance(value, self.model_type):
            raise TraitError("Wrong type")


class String(Model):
    default_value = ""
    model_type = str


def kwarg_setter(func):
    @wraps(func)
    def inner(obj, *args, **kwargs):
        to_pop = []
        for name in kwargs:
            clsdict = obj.__class__.__dict__
            if name in clsdict:
                if hasattr(clsdict[name], "__is_trait__"):
                    if clsdict[name].__is_trait__:
                        setattr(obj, name, kwargs[name])
                        to_pop.append(name)
        for ele in to_pop:
            kwargs.pop(ele)
        return func(obj, *args, **kwargs)
    return inner


class Traitful:
    validators = {}

    def __init_subclass__(cls):
        setattr(cls, "__init__", kwarg_setter(getattr(cls, "__init__")))

    @classmethod
    def validate(cls, name):
        def outer(func):
            cls.validators[name] = func
            @wraps(func)
            def inner(*args, **kwargs):
                return func(*args, **kwargs)
            return inner
        return outer


class TraitError(Exception): ...


validate = Traitful.validate
