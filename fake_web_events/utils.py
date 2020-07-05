import os
import yaml
import random
import sys


def _get_abs_path(path):
    __location__ = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(__location__, path)


def load_config():
    try:
        with open(os.path.join(sys.path[0], 'config.yml'), 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        with open(_get_abs_path('config.template.yml'), 'r') as f:
            return yaml.safe_load(f)


config = load_config()


def select_random(property_name):
    keys = [key for key in config.get(property_name).keys()]
    weights = config.get(property_name).values()
    return random.choices(keys, weights=weights)[0]

