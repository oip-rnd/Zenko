from ..error import RequiredKeyError


def assert_key(mapping, key, target = 'mapping'):
    if key not in mapping:
        raise RequiredKeyError(key, target)
    return True
