import os
import yaml
import random


def _get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_config():
    with open(_get_abs_path('config.yml'), 'r') as f:
        return yaml.safe_load(f)


config = load_config()


def select_random(property_name):
    keys = [key for key in config.get(property_name).keys()]
    weights = config.get(property_name).values()
    return random.choices(keys, weights=weights)[0]


