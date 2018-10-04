import uuid

from pipewrench.errors import RetryError, StopProcessingError
from . import s3
from .execute import MainPipeline, OperationPipeline
from .obj.stage import Stage, SubStage
from .obj.environment import Environment
from .util.log import Log
from .util.prng import prng
from .util.mapping import get_keys
from .obj.scenario import Bucket
from .obj.object import ObjectProxy
from . import constant
from pprint import pprint
_log = Log('stages')

def register_stage(stage = None, pipeline = 'main'):
    def inner(cls):
        if pipeline == 'main':
            MainPipeline.Register(cls)
        elif pipeline == 'op':
            OperationPipeline.Register(cls)
        _log.debug('Registered stage %s to pipeline %s'%(cls.__name__, pipeline))
        return cls
    if stage is None:
        return inner
    else:
        return inner(stage)


# Picks the scenario to test
@register_stage
class PickScenarioStage(Stage):
    def Execute(self, env):
        env.scenario = prng.choice(list(self.scenarios.values()))
        self.logger.debug('%s scenario chosen for execution'%env.scenario.name)
        return env

# Picks the backends for use with the required buckets
@register_stage
class PickBackendStage(Stage):
    def Execute(self, env):
        for bucket_conf in env.scenario.required.buckets:
            # Gen a random name
            name = uuid.uuid4().hex
            # Choose the backend type
            if bucket_conf.transient: # Transient source requires a zenko bucket
                backend_type = constant.BackendType.ZNK
            else:
                available_backends = self.backends.types() if not bucket_conf.clouds else bucket_conf.clouds
                backend_type = prng.choice(available_backends)
            # Choose a backend of backend_type
            backend = prng.choice(self.backends.list_backends(backend_type=backend_type))
            # Build our client and create the bucket in Zenko
            bucket_client = s3.build_bucket(env.zenko, name)
            if not s3.create_bucket(bucket_client, backend):
                raise StopProcessingError
            # Update our conf and save it
            bucket = bucket_conf._replace(client=bucket_client, backend=backend, name=name)
            env.buckets.append(bucket)
            self.logger.debug('Created bucket %s with backend %s'%(bucket.name, backend.name))
        return env

# Picks the backends to be used for replication
@register_stage
class PickReplicationStage(Stage):
    def Execute(self, env):
        buckets = []
        for bucket in env.buckets:
            if bucket.replication is not None and bucket.replication is not False:
                if isinstance(bucket.replication, list):
                    available_types = bucket.replication
                else:
                    available_types = bucket.clouds
                # self.logger.debug(available_types)
                if not available_types:
                    raise StopProcessingError('Unable to enable replication for %s! No available backends!'%bucket.name)
                backend_type = prng.choice(available_types)
                replication_backend = prng.choice(self.backends.list_backends(
                                                    backend_type=backend_type,
                                                    ignore_name=bucket.backend.name))
                b = bucket._replace(replication=replication_backend)
                buckets.append(b)
            else:
                buckets.append(bucket)
        env.buckets = buckets
        return env

# Enables versioning if required or needed for replication
@register_stage
class EnableVersioningStage(Stage):
    def Execute(self, env):
        for bucket in env.buckets:
            if bucket.versioning or bucket.replication is not None:
                if bucket.backend.type == constant.BackendType.GCP or bucket.backend.type == constant.BackendType.AZR:
                    _log.warn('Versioning is not supported on GCP or Azure backends, skipping')
                    continue
                _log.debug('Enabling versiong for %s'%bucket.name)
                if not s3.enable_versioning(bucket.client):
                    raise StopProcessingError(
                        'Failed to enable versioning for %s'%bucket.name)
        return env

# Enable replication for buckets requiring it
@register_stage
class EnableReplicationStage(Stage):
    def Execute(self, env):
        for bucket in env.buckets:
            if bucket.replication is not None:
                if bucket.backend.type == constant.BackendType.GCP or bucket.backend.type == constant.BackendType.AZR:
                    raise StopProcessingError('GCP or Azure can not be replication sources as they do to not supporting versioning!')
                _log.debug('Enabling replication %s %s -> %s'%(bucket.name, bucket.backend.name, bucket.replication.name))
                if not s3.setup_replication(bucket.client, bucket.replication.name):
                    raise StopProcessingError(
                        'Failed to enable replication %s %s -> %s'%(bucket.name, bucket.backend.name, bucket.replication.name))
        return env

# Enable Lifecycle expiration for buckets requiring it
@register_stage
class EnableExpirationStage(Stage):
    pass

@register_stage
class ResolveObjectStage(Stage):
    def Execute(self, env):
        obj_conf = get_keys(env.scenario.kwargs, 'objects')
        print(obj_conf)
        for bucket in env.buckets:
            if obj_conf:
                env.objects.append(ObjectProxy(env.zenko, bucket.name,
                    **obj_conf['objects']._asdict()))
            else:
                env.objects.append(ObjectProxy())
        return env

# Add a sub pipeline for operation execution
@register_stage
class ExecuteTestsStage(SubStage):
    def Execute(self, env):
        for test in env.scenario.tests:
            test_env = Environment(
                            test=test,
                            buckets=env.buckets,
                            objects=env.objects,
                            scenario=env.scenario
                        )
            self.Route(test_env)
        return env

@register_stage(pipeline='op')
class BuildOperationStage(Stage):
    def Execute(self, env):
        func, args, kwargs = env.test
        for b, o in zip(env.buckets, env.objects):
            ret = func(b, o, *args, **kwargs)
        if not ret:
            raise StopProcessingError('Test %s failed to complete!'%(func))