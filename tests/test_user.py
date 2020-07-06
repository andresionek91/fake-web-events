from fake_web_events.user import User, UserPool
import pytest
from faker import Faker
import random


@pytest.fixture()
def mock_user():
    random.seed(0)
    Faker.seed(0)
    return User()


class TestUser:

    def test_geo(self, mock_user):
        assert mock_user.geo() == {
            'geo_latitude': '38.70734',
            'geo_longitude': '-77.02303',
            'geo_country': 'US',
            'geo_timezone': 'America/New_York',
            'geo_region_name': 'Fort Washington'
        }

    def test_ip(self, mock_user):
        assert mock_user.ip() == {
            'ip_address': '216.73.11.199'
        }

    def test_browser(self, mock_user):
        assert mock_user.browser() == {
            'browser_name': 'InternetExplorer',
            'browser_user_agent': 'Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 4.0; Trident/4.0)',
            'browser_language': 'fy_DE'
        }

    def test_operating_system(self, mock_user):
        assert mock_user.operating_system() == {
            'os': 'iPad; CPU iPad OS 12_4 like Mac OS X',
            'os_name': 'iOS',
            'os_timezone': 'America/New_York'}

    def test_device(self, mock_user):
        assert mock_user.device() == {
            'device_type': 'Mobile',
            'device_is_mobile': True
        }

    def test_user(self, mock_user):
        assert mock_user.user() == {
            'user_custom_id': 'nfisher@yahoo.com',
            'user_domain_id': 'd4713d60-c8a7-4639-ab11-67b367a9c378'
        }

    def test_referer(self, mock_user):
        assert mock_user.referer() == {
            'referer_url': 'www.facebook.com',
            'referer_url_scheme': 'http',
            'referer_url_port': '80',
            'referer_medium': 'internal'
        }

    def test_utm(self, mock_user):
        assert mock_user.utm() == {
            'utm_medium': 'organic',
            'utm_source': 'facebook',
            'utm_content': 'ad_3',
            'utm_campaign': 'campaign_1',
            'click_id': '0a5d2f34-6baa-4455-a3e7-0682c2094cac'
        }


@pytest.fixture()
def mock_user_pool():
    random.seed(0)
    Faker.seed(0)
    return UserPool(10)


class TestUserPool:

    def test_pool_size(self, mock_user_pool):
        assert len(mock_user_pool.pool) == 10

    def test_get_user(self, mock_user_pool):
        assert isinstance(mock_user_pool.get_user(), User)

    def test_pool_size_after_getting_user(self, mock_user_pool):
        mock_user_pool.get_user()
        assert len(mock_user_pool.pool) == 10
