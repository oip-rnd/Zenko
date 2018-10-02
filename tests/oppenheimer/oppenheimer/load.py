from .obj import backend, secret, scenario
from .util import yaml, schema
from .util.log import Log

_log = Log('load')


def load_secrets():
    data = yaml.load_yaml('secrets.yaml')
    schema.assert_key(data, 'secrets')
    return len(list(map(secret.load_secret, data['secrets'])))

def load_backends():
    data = yaml.load_yaml('backends.yaml')
    schema.assert_key(data, 'backends')
    return len(list(map(backend.load_backend, data['backends'])))

def load_scenarios():
    data = yaml.load_yaml('scenarios.yaml')
    schema.assert_key(data, 'scenarios')
    return len(list(map(scenario.load_scenario, data['scenarios'])))

def load():
    secrets = load_secrets()
    backends = load_backends()
    scenarios = load_scenarios()
    _log.info('Loaded %s secrets, %s backends, %s scenarios'%(secrets, backends, scenarios))
