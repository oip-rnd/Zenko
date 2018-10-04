from pipewrench.pipeline import Filter, Router

from .backend import BackendsWrapper
from .scenario import SCENARIOS
from .secret import SECRETS
from ..register import CHECKS, TESTS
from ..execute import OperationPipeline


class Stage(Filter):
    secrets = SECRETS
    backends = BackendsWrapper
    scenarios = SCENARIOS
    tests = TESTS
    checks = CHECKS

class SubStage(Router):
    secrets = SECRETS
    backends = BackendsWrapper
    scenarios = SCENARIOS
    tests = TESTS
    checks = CHECKS
    def __init__(self):
        super().__init__(OperationPipeline)
