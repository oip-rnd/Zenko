from collections import namedtuple


def _createNamespaceList(lst, name = 'root'):
    data = []
    for item in lst:
        if isinstance(item, dict) or isinstance(item, list):
            data.append(createNamespace(item, str(lst.index(item))))
        else:
            data.append(item)
    return tuple(data)

def _createNamespaceDict(dikt, name = 'root'):
    data = {}
    for key, value in dikt.items():
        if isinstance(value, dict) or isinstance(value, list):
            data[key] = createNamespace(value, key)
        else:
            data[key] = value
    nt = namedtuple(name, list(data.keys()))
    return nt(**data)


def createNamespace(obj, name = 'root'):
    if isinstance(obj, list):
        return _createNamespaceList(obj, name)
    elif isinstance(obj, dict):
        return _createNamespaceDict(obj, name)
    return obj


def recursivelyUpdateDict(orig, new):
    updated = orig.copy()
    updateFrom = new.copy()
    for key, value in updated.items():
        if key in new:
            if not isinstance(value, dict):
                updated[key] = updateFrom.pop(key)
            else:
                updated[key] = recursivelyUpdateDict(value, updateFrom.pop(key))
    for key, value in updateFrom.items():
        updated[key] = value
    return updated
