from pipewrench.pipeline import Filter

from .backend import BACKENDS
from .scenario import SCENARIOS
from .secret import SECRETS
from ..register import CHECKS, TESTS


class Stage(Filter):
    secrets = SECRETS
    backends = BACKENDS
    scenarios = SCENARIOS
    tests = TESTS
    checks = CHECKS
