import re

FILESIZE_SUFFIXES = {
    'B': 1,
    'K': 1024,
    'M': 1024 ** 2,
    'G': 1024 ** 3,
}

FILESIZE_REGEX = re.compile(r'^[0-9]+[BKMG]$')
BUCKET_NAME_REGEX = re.compile(r'^[a-zA-Z0-9.\-_]{1,255}$')

# Base class for all constants
class Constant:
    @classmethod
    def repr(cls):
        return cls.__name__

# Base class for all constant containers, provides predefined convenience classes
class Container:
    # Returns True if _ROOT is a parent of constant
    _ROOT = None
    @classmethod
    def is_cls(cls, constant):
        try:
            return cls._ROOT in constant.__bases__
        except:
            return False

    # Maps constants to integers for use in config files
    _MAP = {}
    @classmethod
    def to_constant(cls, i):
        if isinstance(i, list):
            return [cls._MAP.get(x) for x in i]
        return cls._MAP.get(i)


# Base class for all backends to inherit from
class Backend(Constant):
    pass

class AWSBackend(Backend):
    pass

class GCPBackend(Backend):
    pass

class AZRBackend(Backend):
    pass

class S3CBackend(Backend):
    pass

class SPDBackend(Backend):
    pass

class ZNKBackend(Backend):
    pass

# Container to hold all backend types
class BackendType(Container):
    AWS = AWSBackend
    GCP = GCPBackend
    AZR = AZRBackend
    S3C = S3CBackend
    SPD = SPDBackend
    ZNK = ZNKBackend

    _ROOT = Backend
    _MAP = {
        1: AWSBackend,
        2: GCPBackend,
        3: AZRBackend,
        4: S3CBackend,
        5: SPDBackend,
        6: ZNKBackend,
    }

# Base class for all secret types to inherit from
class Secret(Constant):
    pass

class KEYSecret(Secret):
    pass

# Container for all secret types
class SecretType(Container):
    KEY = KEYSecret

    _ROOT = Secret
    _MAP = {
        1: KEYSecret,
    }


REPLICATION_TMPL = '''{{"Role": "{role}",
    "Rules": [
      {{
        "Prefix": "{prefix}",
        "Status": "Enabled",
        "Destination": {{
          "Bucket": "{dest}",
          "StorageClass": "{backends}"
        }}
      }}
    ]
  }}'''

EXPIRY_TMPL = {
    'Rules': [{
        'Expiration': {
            'Date': None,
        },
        'Status': 'Enabled',
        'Filter': {
            'Prefix': ''
        }
    }]
}
