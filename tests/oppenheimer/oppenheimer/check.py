from .register import register_check



@register_check('get')
def get_objects():
    pass

@register_check('replication')
def check_replication():
    pass

@register_check('get-multibucket')
def check_multibucket():
    pass
