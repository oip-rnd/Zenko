from collections import OrderedDict, namedtuple
from itertools import chain
from .util.mapping import recursivelyUpdateDict

TESTS = OrderedDict()
CHECKS = OrderedDict()

class Operation:
    _kwargs = []

    def __init__(self, name, func, required = [], **kwargs):
        self.name = name
        self.func = func
        self._kwargs = required
        self._default_kwargs = kwargs

    @property
    def kwargs(self):
        return list(chain(self._kwargs, self._default_kwargs))

    def set_kwargs(self, **kwargs):
        self._passed_kwargs = kwargs

    def __call__(self, bucket, objs):
        kwargs = recursivelyUpdateDict(self._default_kwargs,
                                        self._passed_kwargs)
        return self.func(bucket, objs, **kwargs)



def _register(resource_type, name, func, *args, **kwargs):
    resource_type[name] = (func, args, kwargs)
    return func

def register_test(name, *args, **kwargs):
    def inner(f):
        return _register(TESTS, name, f, *args, **kwargs)
    return inner

def register_check(name, *args, **kwargs):
    def inner(f):
        return _register(CHECKS, name, f, *args, **kwargs)
    return inner

def get_test(name):
    return TESTS.get(name)

def get_check(name):
    return CHECKS.get(name)
