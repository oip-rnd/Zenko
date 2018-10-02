from . import load
from .execute import Execute as ExecuteStages

def entry():
    load.load()
    ExecuteStages()
