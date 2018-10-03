import uuid
import warnings

from boto3 import Session
from botocore.handlers import set_list_objects_encoding_type_url

from .constant import REPLICATION_TMPL, BackendType, BUCKET_NAME_REGEX
from .util.conf import config
from .util.log import Log

from pprint import pprint


_log = Log('s3')

def build_client_generic(backend, **kwargs):
    return Session(aws_access_key_id = backend.access_key,
                    aws_secret_access_key=backend.secret_key
                ).resource('s3', **kwargs)

def build_client_zenko():
    return build_client_generic(config.zenko, endpoint_url=config.zenko.host)


def build_client_gcp(backend, **kwargs):
    sesh = Session(aws_access_key_id = backend.access_key,
                    aws_secret_access_key=backend.secret_key)
    sesh.events.unregister(
        'before-parameter-build.s3.ListObjects',
        set_list_objects_encoding_type_url)
    return sesh.resource('s3', endpoint_url='https://storage.googleapis.com')


def build_client_sproxyd(backend, **kwargs):
    raise NotImplementedError

def build_client_azure(backend, **kwargs):
    raise NotImplementedError

_TYPE_HANDLERS = {
    BackendType.AWS: build_client_generic,
    BackendType.GCP: build_client_gcp,
    BackendType.AZR: build_client_azure,
    BackendType.S3C: build_client_generic,
    BackendType.SPD: build_client_sproxyd,
}


def build_client(backend, **kwargs):
    return _TYPE_HANDLERS[backend.type](backend, **kwargs)



def build_bucket(resource, name):
    if '"' in name:
        name = name.replace('"', '')
        warnings.warn('`"` found in bucket name! silently stripping')
    if BUCKET_NAME_REGEX.fullmatch(name) is None:
        raise RuntimeError('%s is an invalid bucket name!')
    return resource.Bucket(name)


def create_bucket(bucket, backend):
    try:
        _log.debug('Creating bucket %s loc:%s'%(bucket.name, backend.name))
        bucket.create(CreateBucketConfiguration=dict(LocationConstraint=backend.name))
    except Exception as e:
        _log.error('Error creating bucket %s'%(bucket.name))
        _log.exception(e)
        return False
    return True

def enable_versioning(bucket):
    try:
        bucket.Versioning().enable()
        return True
    except Exception as e:
        _log.error('Error enabling versioning for bucket %s'%bucket.name)
        _log.exception(e)
        return False

static_role = 'arn:aws:iam::root:role/s3-replication-role'
static_arn = 'arn:aws:s3:::zenko-bucket'
def setup_replication(bucket, *args, prefix = ''):
    try:
        kwargs = dict(Bucket=bucket.name)
        repl_config = dict(Role=static_role)
        repl_config['Rules'] = [dict(
                ID=uuid.uuid4().hex,
                Status='Enabled',
                Prefix=prefix,
                Destination=dict(
                    Bucket=static_arn,
                    StorageClass=dest)) for dest in args]
        kwargs['ReplicationConfiguration'] = repl_config
        bucket.meta.client.put_bucket_replication(**kwargs)
    except Exception as e:
        _log.error('Failed to enable replication on bucket:%s backends:%s'%(bucket.name, ', '.join(args)))
        _log.exception(e)
        return False
    return True
