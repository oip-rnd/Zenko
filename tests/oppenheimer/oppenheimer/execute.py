from pipewrench import BaseFitting, PipeFitting

from . import s3
from .obj.environment import Environment

ExecutionPipeline = BaseFitting()

def Execute():
    env = Environment(zenko=s3.build_client_zenko())
    ExecutionPipeline.Invoke(env)
