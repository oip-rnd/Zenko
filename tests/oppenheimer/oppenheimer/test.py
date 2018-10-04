from .register import register_test

# Anatomy of a test function
# Arguements:
#   bucket - a boto3 S3.Bucket instance representing the target zenko bucket
#   objs - A iterable yielding objects to be PUT/GET/etc to the passed bucket
# Return: True/False
#   True - operations successfully completed
#   False - Unrecoverable error happended during operation



@register_test('put')
def put_objects(bucket, objs):
    for obj, data in objs:
        obj.upload_fileobj(data)
    return True

@register_test('get')
def get_objects(bucket, objs):
    pass

@register_test('mpu', objects=dict(size='100M'))
def put_mpu(bucket, objs):
    for obj, data in objs:
        obj.upload_fileobj(data)
    return True

@register_test('put-multibucket')
def put_multibucket(bucket, objs):
    pass
