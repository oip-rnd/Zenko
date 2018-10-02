from .util import log

# This is need to cause the stages, test, and checks to autoregister
from . import stages, test, check

__version__ = '0.0.1'

log.setupLogging('Oppenheimer', __version__)
