from pipewrench import Message

from ..util.prng import prng


class Environment(Message):
    scenario = None
    buckets = []
    objects = []
