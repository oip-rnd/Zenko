import boto3
from botocore.handlers import set_list_objects_encoding_type_url
from .constant import BackendType, REPLICATION_TMPL
import uuid



def build_client_generic(backend, **kwargs):
    return Session(aws_access_key_id = backend.access_key,
                    aws_secret_access_key=backend.secret_key
                ).resource('s3', **kwargs)



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
    BackendType.ZENKO: build_client_generic,
}


def build_client(backend, **kwargs):
    return _TYPE_HANDLERS[backend.type](backend, **kwargs)


static_role = 'arn:aws:iam::root:role/s3-replication-role'
static_arn = 'arn:aws:s3:::zenko-bucket'
def create_bucket(resource, name):
    if '"' in name:
        name = name.replace('"', '')
        warnings.warn('`"` found in bucket name! silently stripping')
    if BUCKET_NAME_FORMAT.fullmatch(name) is None:
        raise RuntimeError('%s is an invalid bucket name!')
    return resource.Bucket(name)

def setup_replication(bucket, *args, prefix = '')
    kwargs = dict(Bucket=bucket)
    repl_config = dict(Role=static_role)
    rules = [
        dict(Status='Enabled', Prefix=prefix, Destination=dict('Bucket'=static_arn, StorageClass=dest)) for dest in args
    ]
