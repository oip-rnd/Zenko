from .util import log
from .util.conf import config
import sys

__version__ = '0.0.1'

log.setupLogging('Oppenheimer', __version__, **config.logging._asdict())

# This is need to cause the stages, test, and checks to autoregister
from . import check, stages, test
