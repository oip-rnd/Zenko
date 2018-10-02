from pipewrench import PipeFitting, BaseFitting
from .obj.environment import Environment

ExecutionPipeline = BaseFitting()

def Execute():
    env = Environment()
    ExecutionPipeline.Invoke(env)
