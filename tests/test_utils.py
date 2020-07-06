from fake_web_events.utils import WeightedRandom
import random
import pytest


@pytest.mark.parametrize('property_name,expected', [
    ('operating_systems', 'iOS'),
    ('landing_pages', 'product_a'),
    ('utm_sources', 'mailchimp'),
    ('ads', 'ad_5'),
    ('campaigns', 'campaign_2'),
    ('utm_mediums', 'social'),
    ('browsers', 'Safari'),
])
def test_weighted_random_select(property_name, expected):
    random.seed(0)
    assert WeightedRandom().select(property_name) == expected


@pytest.mark.parametrize('pages,expected', [
    ('home', (['home', 'product_a', 'product_b', 'session_end'], [0.45, 0.17, 0.12, 0.26])),
    ('product_a', (['product_a', 'home', 'cart', 'session_end'], [0.5, 0.18, 0.12, 0.2])),
    ('product_b', (['product_b', 'home', 'cart', 'session_end'], [0.4, 0.22, 0.14, 0.24])),
    ('cart', (['cart', 'payment', 'home', 'session_end'], [0.25, 0.5, 0.15, 0.1])),
    ('payment', (['payment', 'confirmation', 'cart', 'session_end'], [0.45, 0.4, 0.1, 0.05])),
    ('confirmation', (['confirmation', 'session_end'], [0.4, 0.6])),
])
def test_weighted_get_pages(pages, expected):
    assert WeightedRandom().get_pages(pages) == expected