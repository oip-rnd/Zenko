import random
import os

prng = random.Random()

# Seed our prng with data from /dev/urandom
prng.seed(os.urandom(8))
