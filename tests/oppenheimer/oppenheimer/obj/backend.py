from collections import defaultdict, namedtuple

from .. import constant
from ..error import DuplicateBackendError, InvalidBackendFormatError
from .secret import get_secret
from ..util.log import Log
from ..util import schema

_log = Log('obj.backend')

Backend = namedtuple('Backend', ['name', 'type', 'bucket', 'access_key', 'secret_key'])


BACKENDS = defaultdict(dict)

def get_backend(backend_type, name):
    return BACKENDS.get(backend_type, {}).get(name)

def register_backend(backend):
    BACKENDS[backend.type][backend.name] = backend


def load_backend(data):
    schema.assert_key(data, 'name')
    try:
        btype = constant.BackendType.to_constant(data.get('type'))
        _log.debug('Loading backend %s type: %s'%(data['name'], btype.repr()))
        if btype is None or btype not in _TYPE_HANDLERS:
            raise InvalidBackendFormatError(data.get('name'))
        return _TYPE_HANDLERS[btype](**data)
    except:
        raise InvalidBackendFormatError(data.get('name'))


def load_generic(type, name, bucket, secret):
    btype = constant.BackendType.to_constant(type)
    if name in BACKENDS[btype]:
        raise DuplicateBackendError(name)
    sdata = get_secret(constant.SecretType.KEY, secret)
    if not sdata:
        raise InvalidBackendFormatError(name)
    backend = Backend(name, btype, bucket, sdata.data['access_key'], sdata.data['secret_key'])
    register_backend(backend)
    return backend


def load_azure(type, name, bucket, secret):
    pass


def load_sproxyd(type, name, bucket, secret):
    pass


_TYPE_HANDLERS = {
    constant.BackendType.AWS: load_generic,
    constant.BackendType.GCP: load_generic,
    constant.BackendType.AZR: load_azure,
    constant.BackendType.S3C: load_generic,
    constant.BackendType.SPD: load_sproxyd,
}
