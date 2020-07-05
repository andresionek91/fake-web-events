import os
import yaml
import random
import sys


def _get_abs_path(path):
    __location__ = sys.path[0]
    return os.path.join(__location__, path)


def load_config():
    try:
        with open(_get_abs_path('config.yml'), 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(e, 'Could not find a config.yml in the same '
                                'directory as the script that runs the simulation. '
                                'Please create a config file following the template.')


config = load_config()


def select_random(property_name):
    keys = [key for key in config.get(property_name).keys()]
    weights = config.get(property_name).values()
    return random.choices(keys, weights=weights)[0]

