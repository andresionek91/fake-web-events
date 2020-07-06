from fake_web_events.user import User, UserPool
from fake_web_events.event import Event
import pytest
from faker import Faker
import random
from datetime import datetime


@pytest.fixture()
def fake_event():
    random.seed(0)
    Faker.seed(0)
    return Event(datetime(2020, 7, 7, 0, 0, 0, 0), User(), 10)


class TestEvent:

    def test_randomize_timestamp(self, fake_event):
        actual = fake_event.randomize_timestamp(datetime(2020, 7, 7, 0, 0, 0, 0))
        expected = datetime(2020, 7, 7, 0, 0, 0, 904000)
        assert actual == expected

    def test_get_next_page(self, fake_event):
        assert fake_event.get_next_page() == 'session_end'

    def test_is_active(self, fake_event):
        assert fake_event.is_active()

    def test_update(self, fake_event):
        assert not fake_event.update(datetime(2020, 7, 7, 0, 0, 0, 0))

    def test_pageview(self, fake_event):
        assert fake_event.pageview() == {
            'event_timestamp': '2020-07-06 23:59:59.484000',
            'event_type': 'pageview',
            'page_url': 'http://www.dummywebsite.com/product_a',
            'page_url_path': '/product_a'
        }
