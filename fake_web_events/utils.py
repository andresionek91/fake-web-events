import os
import yaml
import random
import sys
import logging

from typing import Tuple, List


def _get_abs_path(path: str) -> str:
    __location__ = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(__location__, path)


def load_config() -> dict:
    """
    Load config file. If not found, then load the template
    """
    try:
        with open(os.path.join(sys.path[0], 'config.yml'), 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.info('config.yml not found, loading default template.')
        with open(_get_abs_path('config.template.yml'), 'r') as f:
            return yaml.safe_load(f)


class WeightedRandom:

    config = load_config()

    def select(self, property_name: str) -> str:
        """
        Select a weighted random value from a property defined in config file
        :param property_name: a property name defined in config file
        :return:
        """
        keys = [key for key in self.config.get(property_name).keys()]
        weights = self.config.get(property_name).values()
        return random.choices(keys, weights=weights)[0]

    def get_pages(self, page: str) -> Tuple[List[str], List[float]]:
        """
        Returns list of pages and weights from config
        """
        pages = [page for page in self.config['pages'].get(page).keys()]
        weights = list(self.config['pages'].get(page).values())
        return pages, weights
