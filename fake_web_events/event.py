from fake_web_events import select_random, get_pages_weights
import json
import random
from datetime import timedelta


class Event:
    """
    Creates events and keeps tracks of sessions
    """

    def __init__(self, current_timestamp, user, batch_size):
        self.previous_page = None
        self.current_page = select_random('landing_pages')
        self.user = user.asdict()
        self.batch_size = batch_size
        self.current_timestamp = self.randomize_timestamp(current_timestamp)
        self.is_new_page = True

    def randomize_timestamp(self, timestamp):
        """
        Randomize timestamps so not all events come with the same timestamp value
        """
        range_milliseconds = int(self.batch_size * 0.3 * 1000)
        random_interval = random.randrange(-range_milliseconds, range_milliseconds)
        return timestamp + timedelta(milliseconds=random_interval)

    def get_next_page(self):
        """
        Calculate which one should be the next page
        """
        pages, weights = get_pages_weights(self.current_page)
        self.current_page = random.choices(pages, weights=weights)[0]

    def asdict(self):
        """
        Return the event as a dictionary
        """
        return {
            'event_timestamp': self.current_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'event_type': 'pageview',
            'page_url': f'http://www.dummywebsite.com/{self.current_page}',
            'page_url_path': f'/{self.current_page}',
            **self.user
        }

    def is_active(self):
        """
        Check if session is currently active
        """
        return self.current_page != 'session_end'

    def update(self, timestamp):
        """
        Update state / Change pages
        """
        if self.is_active():
            self.current_timestamp = self.randomize_timestamp(timestamp)
            self.previous_page = self.current_page
            self.get_next_page()
            self.is_new_page = self.current_page != self.previous_page

    def __str__(self):
        """
        Human readable event
        """
        return json.dumps(self.asdict(), indent=4, ensure_ascii=False)
