from fake_web_events.utils import WeightedRandom
from fake_web_events.user import User
import json
import random
from datetime import timedelta, datetime


class Event(WeightedRandom):
    """
    Creates events and keeps tracks of sessions
    """

    def __init__(self, current_timestamp: datetime, user: User, batch_size: int):
        self.previous_page = None
        self.current_page = self.select('landing_pages')
        self.user = user.asdict()
        self.batch_size = batch_size
        self.current_timestamp = self.randomize_timestamp(current_timestamp)
        self.is_new_page = True

    def randomize_timestamp(self, timestamp: datetime) -> datetime:
        """
        Randomize timestamps so not all events come with the same timestamp value
        """
        range_milliseconds = int(self.batch_size * 0.3 * 1000)
        random_interval = random.randrange(-range_milliseconds, range_milliseconds)
        return timestamp + timedelta(milliseconds=random_interval)

    def get_next_page(self) -> str:
        """
        Calculate which one should be the next page
        """
        pages, weights = self.get_pages(self.current_page)
        self.current_page = random.choices(pages, weights=weights)[0]

        return self.current_page

    def pageview(self) -> dict:
        """
        Return the event information as a dictionary
        """
        return {
            'event_timestamp': self.current_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'event_type': 'pageview',
            'page_url': f'http://www.dummywebsite.com/{self.current_page}',
            'page_url_path': f'/{self.current_page}',
        }

    def asdict(self) -> dict:
        """
        Return the event + user as a dictionary
        """
        return {
            **self.pageview(),
            **self.user
        }

    def is_active(self) -> bool:
        """
        Check if session is currently active
        """
        return self.current_page != 'session_end'

    def update(self, timestamp: datetime) -> bool:
        """
        Update state / Change pages
        """
        if self.is_active():
            self.current_timestamp = self.randomize_timestamp(timestamp)
            self.previous_page = self.current_page
            self.get_next_page()
            self.is_new_page = self.current_page != self.previous_page

            return self.is_new_page

    def __str__(self) -> str:
        """
        Human readable event
        """
        return json.dumps(self.asdict(), indent=4, ensure_ascii=False)
