from .constant import FILESIZE_SUFFIXES

class OppenheimerError(Exception):
    _tmpl = None
    _msg = None
    def __init__(self, *args, **kwargs):
        msg = self._msg if self._msg else 'An error has occurred!'
        if self._tmpl is not None:
            if args:
                msg = self._tmpl%args
            elif kwargs:
                msg = self._tmpl.format(**kwargs)
        super().__init__(msg)

class UnknownError(OppenheimerError):
    _msg = 'An unknown error has occurred (probably in a catch all)'

class NoConfigError(OppenheimerError):
    _tmpl = 'Could not find path %s to load!'

class InvalidConfigError(OppenheimerError):
    _tmpl = '%s contains an invalid configuration!'

class InvalidFileSizeError(OppenheimerError):
    def __init__(self, value):
        super().__init__('%s is not a valid filesize! Valid suffixes are %s'%(value, ', '.join(FILESIZE_SUFFIXES.keys())))

class InvalidSecretFormatError(OppenheimerError):
    _tmpl = 'Secret %s is incorrectly formatted'

class DuplicateSecretError(OppenheimerError):
    _tmpl = 'A secret named %s is already registered!'

class InvalidBackendFormatError(OppenheimerError):
    _tmpl = 'Backend %s is incorrectly formatted'

class DuplicateBackendError(OppenheimerError):
    _tmpl = 'A backend named %s is already registered!'

class RequiredKeyError(OppenheimerError):
    _tmpl = 'Required key %s is not present in %s'

class InvalidScenarioFormatError(OppenheimerError):
    _tmpl = 'Scenario %s is incorrectly formatted'

class DuplicateScenarioError(OppenheimerError):
    _tmpl = 'A scenario named %s is already registered'


class TestDoesntExistError(OppenheimerError):
    _tmpl = "A test with the name %s doesn't exist!"

class CheckDoesntExistError(OppenheimerError):
    _tmpl = "A check with the name %s doesn't exists!"
