from pipewrench.errors import RetryError, StopProcessingError

from .execute import ExecutionPipeline
from .obj.stage import Stage
from .util.log import Log
from .util.prng import prng
import uuid

_log = Log('stages')

def register_stage(stage):
    ExecutionPipeline.Register(stage)
    _log.debug('Registered stage %s'%stage.__name__)
    return stage


@register_stage
class PickScenarioStage(Stage):
    def Execute(self, env):
        env.scenario = prng.choice(list(self.scenarios.values()))
        self.logger.debug('%s scenario chosen for execution'%env.scenario.name)
        return env

@register_stage
class ResolveBucketStage(Stage):
    def Execute(self, env):
        for bucket in env.scenario.required.buckets:
            name = uuid.uuid4().hex
            # Choose the backend
            available_backends = list(filter(lambda b: not bucket.clouds or b in bucket.clouds, self.backends))
            backend = prng.choice(available)
