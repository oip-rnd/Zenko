from pipewrench import BaseFitting, PipeFitting

from . import s3
from .obj.environment import Environment

MainPipeline = BaseFitting()
# MainPipeline = PipeFitting()

OperationPipeline = BaseFitting()
# OperationPipeline = PipeFitting()

def Execute():
    env = Environment(zenko=s3.build_client_zenko())
    MainPipeline.Invoke(env)
