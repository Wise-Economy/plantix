import json
import random
import string


def generate_payload(n: int, clique: bool):
    possible_plant_topics = [id_generator() for i in range(10)]
    for node in range(n):
        pass


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


