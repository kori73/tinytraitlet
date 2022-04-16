from functools import wraps
from typing import Any


class Model:
    default_value = None
    __is_trait__ = True
    model_type: Any

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
        owner.setup_trait(name)

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
        traits = [ele for ele in obj.traits if ele in kwargs]
        for name in traits:
            setattr(obj, name, kwargs[name])
            to_pop.append(name)
        for ele in to_pop:
            kwargs.pop(ele)
        return func(obj, *args, **kwargs)
    return inner


class Traitful:
    traits = set()
    validators = {}

    def __init_subclass__(cls):
        cls.traits = frozenset(cls.traits)
        cls.validators = cls.validators.copy()
        for _, value in cls.__dict__.items():
            try:
                value.trait_to_validate
                cls.validators[value.trait_to_validate] = value
            except AttributeError:
                pass
            
        setattr(cls, "__init__", kwarg_setter(getattr(cls, "__init__")))

    @classmethod
    def setup_trait(cls, name):
        try:
            traits = set(cls.traits)
            traits.add(name)
            cls.traits = traits
        except AttributeError:
            cls.traits = {name}


def validate(name):
    def outer(func):
        func.trait_to_validate = name
        @wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return outer


class TraitError(Exception): ...
